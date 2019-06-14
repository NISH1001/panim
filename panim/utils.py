#!/usr/bin/env python3

import numpy as np
from PIL import Image

def L1(x1,x2):
    return np.abs(x1)+np.abs(x2)

def L2(x1,x2):
    return np.sqrt(x1**2+x2**2)

def Linf(x1,x2):
    return np.maximum(np.abs(x1), np.abs(x2))

def meshgrid_euclidean(shape):
    return np.meshgrid(*map(range, shape))

def meshgrid_polar(shape, center=None, dist=L2):
    y, x = meshgrid_euclidean(shape)
    if center is None:
        center = np.array(shape)/2
    y, x = y-center[0], x-center[1]
    return dist(x, y), np.arctan2(x, y)

def imnormalize(im):
    im-=np.min(im)
    M=np.max(im)
    if M>0: im=im*255/M
    return im

def imshow(im,normalize=True):
    if len(im.shape)==2:
        if normalize: im=imnormalize(im)
        im=np.float32(im)
    if len(im.shape)==3 and im.shape[2]==3:
        im=np.uint8(im)
    im=Image.fromarray(im)
    im.show()


def main():
    pass

if __name__ == "__main__":
    main()

