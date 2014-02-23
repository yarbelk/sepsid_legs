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
    raise NotImplemented()


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
    from matplotlib import pyplot as plt
    from matplotlib import cm
    image_name = sys.argv[1]
    output_image_name = sys.argv[2]
    img = Image.open(image_name)
    image = misc.fromimage(img, flatten=1)

    new_image = main(image, 128)
    plt.imshow(new_image, cmap=cm.binary_r, interpolation='nearest')
    plt.show()
    misc.imsave(output_image_name, new_image)
