"""
model
"""

import torch
import torch.nn as nn
import torchvision.transforms.functional as TF

import segmentation.networks as networks


class DoubleConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(DoubleConv, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, 1, 1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.conv(x)

class Segmentor(nn.Module):
    def __init__(self, input_dim=3, output_dim=51):
        super(Segmentor, self).__init__()

        self.net = networks.enc_c_gen(input_dim, output_dim)

    def forward(self, x):
        x = self.net(x)
        return x

if __name__ == "__main__":

    pass

