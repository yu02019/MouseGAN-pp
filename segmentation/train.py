import torch
import albumentations as A
from albumentations.pytorch import ToTensorV2
from tqdm import tqdm
import torch.nn as nn
import torch.optim as optim
from .model import Segmentor
from utils import (
    load_checkpoint,
    save_checkpoint,
    # get_loaders,
    check_accuracy,
    save_predictions_as_imgs,
)
from my_dataset import get_loaders

# Hyperparameters etc.
LEARNING_RATE = 1e-4
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 32
NUM_EPOCHS = 50
NUM_WORKERS = 2
IMAGE_HEIGHT = 224
IMAGE_WIDTH = 160
PIN_MEMORY = True
LOAD_MODEL = 'weight/xxx'

Data_dir = r'xxx'
TRAIN_IMG_DIR = Data_dir + 'xxx'
TRAIN_MASK_DIR = Data_dir + 'xxx'
VAL_IMG_DIR = Data_dir + 'xxx'
VAL_MASK_DIR = Data_dir + 'xxx'

Input_dim = 1
Save_weight_name = 'weight/xxx'
Load_weight_name = ''
Load_pretrained_weight = False
Save_freq = 10

def train_fn(loader, model, optimizer, loss_fn, scaler):
    loop = tqdm(loader)

    for batch_idx, (data, targets) in enumerate(loop):
        data = data.to(device=DEVICE)
        targets = targets.long().to(device=DEVICE)

        predictions = model(data)
        loss = loss_fn(predictions, targets)

        # backward
        optimizer.zero_grad()
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        # update tqdm loop
        loop.set_postfix(loss=loss.item())


def main():
    train_transform = A.Compose(
        [
            A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),

            A.Rotate(limit=35, p=1.0),
            # A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.1),
            A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0, rotate_limit=0, p=1.0),

            A.Normalize(
                mean=[0.0,],
                std=[1.0,],
                max_pixel_value=1.0,
            ),
            ToTensorV2(),
        ],
        additional_targets={'channel2': 'channel', 'channel3': 'channel', 'channel4': 'channel', 'channel5': 'channel'}
    )

    val_transforms = A.Compose(
        [
            A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),

            A.Normalize(
                mean=[0.0, ],
                std=[1.0, ],
                max_pixel_value=1.0,
            ),
            ToTensorV2(),
        ],
        additional_targets={'channel2': 'channel', 'channel3': 'channel', 'channel4': 'channel', 'channel5': 'channel'}
    )

    model = Segmentor(input_dim=Input_dim, output_dim=51).to(DEVICE)

    freeze = Load_pretrained_weight
    if Load_pretrained_weight:
        # GAN pretrained weight
        pre_train_net_state_dict = torch.load(
            r'xxx')
        pre_train_enc_c_state_dict = pre_train_net_state_dict['enc_c']
        new_model_dict = model.state_dict()
        update_dict = {k: v for k, v in new_model_dict.items() if k.replace('net.', '') in pre_train_enc_c_state_dict.keys()}
        if freeze:
            for k, v in update_dict.items():
                v.requires_grad = False
                print(k, v.requires_grad)

        new_model_dict.update(update_dict)
        for k, v in new_model_dict.items():
            print(k, v.requires_grad)
        model.load_state_dict(new_model_dict)

    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    train_loader, val_loader = get_loaders(
        TRAIN_IMG_DIR,
        TRAIN_MASK_DIR,
        VAL_IMG_DIR,
        VAL_MASK_DIR,
        BATCH_SIZE,
        train_transform,
        val_transforms,
        NUM_WORKERS,
        PIN_MEMORY,
    )

    if LOAD_MODEL:
        load_checkpoint(torch.load(LOAD_MODEL), model)

    scaler = torch.cuda.amp.GradScaler()

    for epoch in range(NUM_EPOCHS):
        train_fn(train_loader, model, optimizer, loss_fn, scaler)

        # save model
        if (epoch + 1) % 5 == 0:
            checkpoint = {
                "state_dict": model.state_dict(),
                "optimizer":optimizer.state_dict(),
            }
            save_checkpoint(checkpoint,
                            filename=Save_weight_name.replace('.pth.tar', '_ep{}.pth.tar'.format(epoch + 1)))

    if freeze:
        model_dict = model.state_dict()
        for k, v in model_dict.items():
            print(k, v.requires_grad)
        for k, v in model_dict.items():
            v.requires_grad = True
            print(k, v.requires_grad)

        for epoch in range(NUM_EPOCHS):
            train_fn(train_loader, model, optimizer, loss_fn, scaler)

            # save model
            if (epoch+1) % 5 == 0:
                checkpoint = {
                    "state_dict": model.state_dict(),
                    "optimizer":optimizer.state_dict(),
                }
                save_checkpoint(checkpoint,
                                filename=Save_weight_name.replace('.pth.tar', 'ft_ep{}.pth.tar'.format(epoch+1)))
        print('Done')

if __name__ == "__main__":
    main()