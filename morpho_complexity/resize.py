import numpy as np
import scipy
from scipy import ndimage, misc
import sys
from PIL import Image

def filter_image(image):
    filtered_image = np.zeros(shape=image.shape, dtype='uint8')
    ndimage.filters.gaussian_filter(image, 2, output=filtered_image,
            mode='constant', cval=255)
    return filtered_image

def resize_image(image, size):
    resized = misc.imresize(image, size, 'bicubic')
    return resized

def threshold_image(image, threshold=128):
    return np.where(image <= threshold, 0, 255)


def main(image, size, threshold):
    filtered = filter_image(image)
    resized = resize_image(filtered, size)
    thresholded = threshold_image(resized)
    return thresholded


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    from matplotlib import cm
    from PIL import Image
    image_name = sys.argv[1]
    img = Image.open(image_name)
    image = misc.fromimage(img, flatten=1)

    new_image = main(image, 2.0, 128)
    plt.imshow(new_image, cmap= cm.binary_r, interpolation='nearest')
    plt.show()
