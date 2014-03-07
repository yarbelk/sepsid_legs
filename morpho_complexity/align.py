#!/usr/bin/env python2
import sys
import numpy as np
import scipy
import scipy.signal
from scipy import ndimage, misc
import sys
from PIL import Image

from path import path

import argparse

import resize

def align(image_one, image_two):
    """
    Assume the images have been cropped
    run image 2 across image 1 untill you find the minimum difference
    """
    # Find the not white stuff.
    bool_one = image_one != 255
    bool_two = image_two != 255

    # make that not whie stuff a 1
    int_one = np.where(image_one == 0, 1, 0)
    int_two = np.where(image_two == 0, 1, 0)

    total_area = np.sum(np.where(bool_one, 1, 0)) + np.sum(np.where(bool_two, 1, 0))

    max_overlap = 0
    max_overlap_pos = (0,0)

    max_itterations = bool_one.size - bool_two.size

    convolution = scipy.signal.convolve2d(int_one, int_two, mode="full", boundary="fill", fillvalue=0)
    max_overlap_pos = np.argmax(convolution, axis=0)
    max_overlap_pos[0] += int_two.shape[0] /2
    max_overlap_pos[1] += int_two.shape[1] /2
    max_overlap = convolution.max()

    return {"overlap": max_overlap,
            "difference": total_area - (max_overlap * 2),
            "pos": max_overlap_pos}


def get_overlap(image_one, image_two):
    """get the AND of image_one and image_two at offset (where 0 == true)
    image_two is offset against image_one
    """
    C = np.logical_and(image_one, image_two)
    counter = np.where(C, 1, 0)
    return np.sum(counter)


if __name__ == '__main__':
    import cProfile, pstats, StringIO
    arg_parser = argparse.ArgumentParser(prog="align",
            description="Align two images to maximum overlap.  this runs a "
                        "2d convolution on the images, and will return the "
                        "value of a/the maximum overlap.  there may be more "
                        "than one configuration with a maximum overlap, and "
                        "this returns the first one.\noutput is the overlap "
                        "amount, the difference")
    arg_parser.add_argument('images',
            type=path,
            nargs="+",
            action="append",
            help="image1.png image2.png list of images.  must be an even number")
    arg_parser.add_argument('-o',dest='output',
            type=path,
            action="store",
            default=path('.').abspath(),
            help="where to save")

    args = arg_parser.parse_args(sys.argv[1:])

    images = args.images[0]
    if len(images) < 2 or len(images) % 2 != 0:
        print "\nNeed an even number of images\n\n\t", args.images
        arg_parser.print_help()
        sys.exit(1)

    for i, v in enumerate(images):
        if i % 2 != 0:
            continue
        image_one = misc.fromimage(Image.open(images[i]), flatten=1)
        image_two = misc.fromimage(Image.open(images[i + 1]), flatten=1)

        threshold_image_one = resize.threshold_image(image_one)
        threshold_image_two = resize.threshold_image(image_two)

        img_stats = align(threshold_image_one, threshold_image_two)
        print "{im1}, {im2}:\n" \
              "overlap:    {stats[overlap]}\n" \
              "difference: {stats[difference]}\n".format(
                    im1=images[i],
                    im2=images[i+1],
                    stats=img_stats)
