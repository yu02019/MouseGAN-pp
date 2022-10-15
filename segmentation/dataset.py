import torch
from torch.utils.data import Dataset
import numpy as np


class MouseDataset(Dataset):
    def __init__(self, image_dir, mask_dir, transform=None, ):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform
        self.images = np.load(image_dir)
        self.images = self.images[200:]
        self.masks = np.load(mask_dir)
        self.masks = self.masks[200:]

        if self.images.ndim == 3:
            self.modality = 1
        elif self.images.ndim == 4:
            self.modality = self.images.shape[1]
        else:
            input('please check input data!')
        print('======== self.modality:', self.modality)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        image = self.images[index]
        mask = self.masks[index]

        if self.transform is not None:
            # for 1 mod
            if self.modality == 1:
                augmentations = self.transform(image=image, mask=mask)
                image = augmentations["image"]
                mask = augmentations["mask"]
            # for 2+ mod
            elif self.modality == 2:
                image, mask = self.two_mod_augmentation(image, mask)
            elif self.modality == 5:
                image, mask = self.five_mod_augmentation(image, mask)

        return image, mask

    def two_mod_augmentation(self, image, mask):
        augmentations = self.transform(image=image[0], image1=image[1], mask=mask)
        image = augmentations["image"]
        image1 = augmentations["image1"]
        image1 = torch.Tensor(image1)
        image1 = torch.unsqueeze(image1, 0)
        image_cat = torch.cat([image, image1], dim=0)
        mask = augmentations["mask"]

        return image_cat, mask

    def five_mod_augmentation(self, image, mask):
        augmentations = self.transform(image=image[0], image1=image[1], image2=image[2], image3=image[3], image4=image[4], mask=mask)
        image = augmentations["image"]
        image1 = augmentations["image1"]
        image1 = torch.Tensor(image1)
        image1 = torch.unsqueeze(image1, 0)

        image2 = torch.Tensor(augmentations["image2"])
        image2 = torch.unsqueeze(image2, 0)
        image3 = torch.Tensor(augmentations["image3"])
        image3 = torch.unsqueeze(image3, 0)
        image4 = torch.Tensor(augmentations["image4"])
        image4 = torch.unsqueeze(image4, 0)

        image_cat = torch.cat([image, image1, image2, image3, image4], dim=0)
        mask = augmentations["mask"]

        return image_cat, mask


class MouseDataset_test(Dataset):
    def __init__(self, image_dir, mask_dir, transform=None):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform
        self.images = np.load(image_dir)
        self.images = self.images[:135*4]
        self.masks = np.load(mask_dir)
        self.masks = self.masks[:135*4]

        if self.images.ndim == 3:
            self.modality = 1
        elif self.images.ndim == 4:
            self.modality = self.images.shape[1]
        else:
            input('please check input data!')
        print('======== self.modality:', self.modality)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        image = self.images[index]
        mask = self.masks[index]

        if self.transform is not None:
            # for 1 mod
            if self.modality == 1:
                augmentations = self.transform(image=image, mask=mask)
                image = augmentations["image"]
                mask = augmentations["mask"]
            # for 2+ mod
            elif self.modality == 2:
                image, mask = self.two_mod_augmentation(image, mask)
            elif self.modality == 5:
                image, mask = self.five_mod_augmentation(image, mask)

        return image, mask

    def two_mod_augmentation(self, image, mask):
        augmentations = self.transform(image=image[0], image1=image[1], mask=mask)
        image = augmentations["image"]
        image1 = augmentations["image1"]
        image1 = torch.Tensor(image1)
        image1 = torch.unsqueeze(image1, 0)
        image_cat = torch.cat([image, image1], dim=0)
        mask = augmentations["mask"]

        return image_cat, mask

    def five_mod_augmentation(self, image, mask):
        augmentations = self.transform(image=image[0], image1=image[1], image2=image[2], image3=image[3], image4=image[4], mask=mask)
        image = augmentations["image"]
        image1 = augmentations["image1"]
        image1 = torch.Tensor(image1)
        image1 = torch.unsqueeze(image1, 0)

        image2 = torch.Tensor(augmentations["image2"])
        image2 = torch.unsqueeze(image2, 0)
        image3 = torch.Tensor(augmentations["image3"])
        image3 = torch.unsqueeze(image3, 0)
        image4 = torch.Tensor(augmentations["image4"])
        image4 = torch.unsqueeze(image4, 0)

        image_cat = torch.cat([image, image1, image2, image3, image4], dim=0)
        mask = augmentations["mask"]

        return image_cat, mask


from torch.utils.data import DataLoader


def get_loaders(
        train_dir,
        train_maskdir,
        val_dir,
        val_maskdir,
        batch_size,
        train_transform,
        val_transform,
        num_workers=4,
        pin_memory=True,
):
    train_ds = MouseDataset(
        image_dir=train_dir,
        mask_dir=train_maskdir,
        transform=train_transform,
    )

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=pin_memory,
        shuffle=True,
    )

    val_ds = MouseDataset_test(
        image_dir=val_dir,
        mask_dir=val_maskdir,
        transform=val_transform,
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=pin_memory,
        shuffle=False,
    )

    return train_loader, val_loader
