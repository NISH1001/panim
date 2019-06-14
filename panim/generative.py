#!/usr/bin/env python3

from animator import AbstractAnimator
import matplotlib.pyplot as plt
from matplotlib import animation

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

def get_image_array(img, normalize=True):
    if len(img.shape)==2:
        if normalize:
            img = imnormalize(img)
        img = np.float32(img)
    if len(img.shape)==3 and img.shape[2]==3:
        img = np.uint8(img)
    return img
    # return Image.fromarray(img)


class GenerativeAnimator:
    def __init__(self, **args):
        self.images = []
        self.image_size = (2048,)*2
        self.r, self.a = meshgrid_polar(self.image_size)
        self.lr = np.log(1 + self.r)
        self.fig = plt.figure()
        self.factor = 1
        # im = np.sin(self.a*self.factor + np.sin(self.lr*4) + self.lr*2)
        # im = np.fmod((1+ im + self.lr), 1)
        # img = get_image_array(im)
        # # img = img.show()
        # plt.imshow(img)
        # plt.show()
        # print(img.shape)
        # img = plt.imshow(img)
        # self.images.append(img)

    def update(self, i):
        print(i)

    def update(self, n):
        factor = 5
        for i in range(n):
            print(i)
            factor += 0.5
            im = np.sin(self.a*factor + np.sin(self.lr*4) + self.lr*2)
            im = np.fmod((1+ im + self.lr), 1)
            img = get_image_array(im)
            img = plt.imshow(img, animated=True)
            self.images.append([img])

    def animate(self, num_frames=1000):
        self.num_frames = num_frames
        plt.axis('off')
        print(len(self.images))
        self.anim = animation.ArtistAnimation(
            self.fig, self.images,
            interval=50, blit=True
        )

    def save(self, filename="out/animation.mp4", fps=30, dpi=100):
        writer = animation.writers['ffmpeg'](fps=fps)
        # self.anim.save(filename, writer='imagemagick')
        self.anim.save(filename, writer=writer, dpi=dpi)
        print("Saving {} to {}".format(self.__class__.__name__, filename))



def main():
    animator = GenerativeAnimator()
    animator.update(50)
    animator.animate()
    animator.save("out/test.mp4")

if __name__ == "__main__":
    main()

