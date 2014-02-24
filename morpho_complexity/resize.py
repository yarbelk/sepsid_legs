import numpy as np
import scipy
from scipy import ndimage, misc
import sys
from PIL import Image


SIZE = 50000


def filter_image(image):
    filtered_image = np.zeros(shape=image.shape, dtype='uint8')
    ndimage.filters.gaussian_filter(image, 2, output=filtered_image,
                                    mode='constant', cval=255)
    return filtered_image


def crop_image(image):
    """
    Crop all extra whitespace.
    """
    idx = np.where(image == 0)
    box = map(min, idx)[::-1] + map(max, idx)[::-1]
    tmp = Image.fromarray(image, 'L')
    region = tmp.crop(box)
    return region


def resize_image(image):
    """
    Resize image until area is 50000 +/- 500
    """
    image_size = image.shape[0] * image.shape[1]
    working_image = image
    while True:
        image_size = working_image.shape[0] * working_image.shape[1]
        current_area = image_size - np.count_nonzero(working_image)
        if abs(current_area - SIZE) <= 500:
            print "finishing area: {}".format(current_area)
            return working_image
        current_area = abs(current_area)
        ratio = np.sqrt(SIZE) / np.sqrt(current_area)
        print "ratio: {}, current_area: {}".format(ratio, current_area)
        working_image = misc.imresize(working_image, ratio, 'bicubic')
        working_image = threshold_image(working_image)


def threshold_image(image, threshold=128):
    return np.where(image <= threshold, 0, 255)


def main(image, threshold):
    filtered = filter_image(image)
    thresholded = threshold_image(filtered)
    resized = resize_image(thresholded)
    return resized


if __name__ == '__main__':
    import os
    import sys
    import argparse

    arg_parser = argparse.ArgumentParser(prog="image_sizes",
            description="resize images to 50,000 pixels in area")
    arg_parser.add_argument('-i',dest='input',
            required=True,
            help="where are the images")
    arg_parser.add_argument('-o',dest='output',
            required=True,
            help="where to save")

    args = arg_parser.parse_args(sys.argv[1:])

    the_dir = args.input
    try:
        os.path.isdir(the_dir)
    except:
        print "give me a real dir please"
        sys.exit(1)

    try:
        os.path.isdir(args.output)
    except:
        print "give me a real output dir please"
        sys.exit(1)

    tmp = [os.path.join(the_dir, image_file) for image_file in os.listdir(the_dir)]
    for filename in tmp:
        if '.tif' in filename:
            output_file = os.path.splitext(filename)[0] + "_resized.tif"
            print "input: {}".format(filename)
            print "output: {}".format(output_file)

            img = Image.open(filename)
            image = misc.fromimage(img, flatten=1)

            new_image = main(image, 128)
            misc.imsave(output_file, new_image)
