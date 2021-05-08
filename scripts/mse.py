#!/usr/bin/env python3

import numpy as np
import imageio
import sys


def getMSE(img1, img2):  # MSE of 2 images
    return (np.sum(np.square(img1 - img2))) / img1.size


# if len(sys.argv) != 3:
#    print('usage')
#    sys.exit(1)

# load images
image1 = imageio.imread(sys.argv[1])
image2 = imageio.imread(sys.argv[2])

image1 = image1.astype(dtype=np.uint8)
image2 = image2.astype(dtype=np.uint8)

print("The MSE between", sys.argv[1], "and", sys.argv[2], "is:", getMSE(image1, image2))

# return getMSE(image1, image2)
