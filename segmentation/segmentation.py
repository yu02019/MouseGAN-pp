import torch
from .model import Segmentor  # final_my_unet
from utils import load_checkpoint
from dataset import get_loaders
import albumentations as A
from albumentations.pytorch import ToTensorV2

LEARNING_RATE = 1e-4
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 5
NUM_EPOCHS = 1
NUM_WORKERS = 2
IMAGE_HEIGHT = 224
IMAGE_WIDTH = 160
PIN_MEMORY = True
# LOAD_MODEL = False
Data_dir = r''

TRAIN_IMG_DIR = Data_dir + ''
TRAIN_MASK_DIR = Data_dir + ''
VAL_IMG_DIR = Data_dir + ''
VAL_MASK_DIR = Data_dir + ''



Input_dim = 2
Modality = 2
Save_weight_name = 'weight/2mod_ep10_ft_augment_onlyShift.pth.tar'
Load_weight_name = Save_weight_name
csv_name = '2mod_ep10_ft_augment_onlyShift_temp'

train_transform = A.Compose(
    [
        A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),
        A.Rotate(limit=35, p=1.0),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.1),
        A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0, rotate_limit=0, p=1.0),

        # for RGB 3 channel
        # A.Normalize(
        #     mean=[0.0, 0.0, 0.0],
        #     std=[1.0, 1.0, 1.0],
        #     max_pixel_value=255.0,
        # ),
        # for gray 1 channel
        A.Normalize(
            mean=[0.0],
            std=[1.0],
            max_pixel_value=1.0,
        ),
        ToTensorV2(),
    ],
    additional_targets={'channel2': 'channel', 'channel3': 'channel'}  # https://albumentations.ai/docs/examples/example_multi_target/
)

val_transforms = A.Compose(
    [
        A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),

        A.Normalize(
            mean=[0.0],
            std=[1.0],
            max_pixel_value=1.0,
        ),
        ToTensorV2(),
    ],
    additional_targets={'channel2': 'channel', 'channel3': 'channel'}
)

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



if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt

    model = Segmentor(input_dim=Input_dim, output_dim=51).to('cuda')
    load_checkpoint(torch.load(Load_weight_name), model)
    model.eval()

    total_preds = []
    total_y = []

    for idx, (x, y) in enumerate(val_loader):
        x = x.to(device='cuda')
        with torch.no_grad():

            if Modality != Input_dim:
                x = torch.cat([x, x], dim=1)

            preds = model(x)
            preds = torch.argmax(preds, dim=1).to('cpu')
            total_preds.append(preds)
            total_y.append(y)


    gt_volumes = total_y.pop(0)
    for i in total_y:
        gt_volumes = np.concatenate((gt_volumes, i), 0)
    print(gt_volumes.shape)

    seg_volumes = total_preds.pop(0)
    for i in total_preds:
        seg_volumes = np.concatenate((seg_volumes, i), 0)
    print(seg_volumes.shape)


    ''' save to nii '''

    import os
    from utils.read_all_data_from_nii_pipe import save_pred_to_nii

    reshape_volumes = seg_volumes

    save_folder_path = r'xxx/{}/'.format(csv_name)
    if not os.path.exists(save_folder_path):
        os.mkdir(save_folder_path)

    save_pred_to_nii(reshape_volumes, need_rotate=False,
                     save_path=save_folder_path,
                     ref_path=r'xxx/*')

