#!/usr/bin/env python3

import os

import time
import datetime
import calendar

import numpy as np
from PIL import Image


def L1(x1, x2):
    return np.abs(x1) + np.abs(x2)


def L2(x1, x2):
    return np.sqrt(x1 ** 2 + x2 ** 2)


def Linf(x1, x2):
    return np.maximum(np.abs(x1), np.abs(x2))


def meshgrid_euclidean(shape):
    return np.meshgrid(*map(range, shape))


def meshgrid_polar(shape, center=None, dist=L2):
    y, x = meshgrid_euclidean(shape)
    if center is None:
        center = np.array(shape) / 2
    y, x = y - center[0], x - center[1]
    return dist(x, y), np.arctan2(x, y)


def imnormalize(im):
    im -= np.min(im)
    M = np.max(im)
    if M > 0:
        im = im * 255 / M
    return im


def imshow(im, normalize=True):
    if len(im.shape) == 2:
        if normalize:
            im = imnormalize(im)
        im = np.float32(im)
    if len(im.shape) == 3 and im.shape[2] == 3:
        im = np.uint8(im)
    im = Image.fromarray(im)
    im.show()


def get_image_array(img, normalize=True):
    if len(img.shape) == 2:
        if normalize:
            img = imnormalize(img)
        img = np.float32(img)
    if len(img.shape) == 3 and img.shape[2] == 3:
        img = np.uint8(img)
    return img
    # return Image.fromarray(img)


def generate_random_color(normalize=True):
    c = np.random.random((3,))
    if not normalize:
        return c * 255.0
    return c


class IAmTime:
    def __init__(self):
        now = datetime.datetime.now()
        month = now.strftime("%m")
        day = now.strftime("%d")
        self.month = str(month.lower())
        self.year = now.year
        self.day = day
        self.hour = now.hour
        self.minute = now.minute
        self.second = now.second

    def __repr__(self) -> str:
        return f"(year={self.year}, month={self.month}, day={self.day}, hour={self.hour}, minute={self.minute}, second={self.second})"


def create_directory(path: str):
    if not os.path.exists(path):
        print(f"Creating directory = {path}")
        os.makedirs(path)


def main():
    iat = IAmTime()
    print(iat)


if __name__ == "__main__":
    main()
