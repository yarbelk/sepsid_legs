import numpy
import scipy
import sys




class ChainCodeImage(object):
    neighbor_transform = numpy.array(
            [
                [-1, -1], [0, -1], [1, -1],
                [-1,  0],          [1,  0],
                [ 1, -1], [0,  1], [1,  1],
            ])

    chaincode_dirs = numpy.array([
            [3,2,1],
            [4,-1,0],
            [5,6,7]])
    chaincode_lookup = {
            0: (1,  0),
            1: (1, -1),
            2: (0, -1),
            3: (-1, -1),
            4: (-1, 0),
            5: (1, -1),
            6: (0,  1),
            7: (1,  1),
            }

    def __init__(self, image):
        self.image = self._get_binary_image(image)
        self.chaincode_points = []
        self.chaincode = []
        self.start_pos = None

    def from_chain_code(self, pos, code):
        return pos + self.chaincode_lookup[code]

    def _get_binary_image(self, image):
        """ true values are those that are leg"""
        bin_image = image < 255
        return bin_image

    def _is_inner_edge(self, pos):
        neighbors = self.neighbor_transform + pos
        value = self.image[pos[0]][pos[1]]
        if not value:
            return False
        for neighbor in neighbors:
            if (neighbor < 0).any():
                pass
            if not self.image[neighbor[0]][neighbor[1]]:
                return True

    def find_edge(self):
        it = numpy.nditer(self.image, flags=['multi_index'])
        while not it.finished:
            if self._is_inner_edge(it.multi_index):
                return it.multi_index
            it.iternext()
        sys.exit(1, "No Image edge")

    def _numpy_in(self, x, data):
        for y in data:
            if (x == y).all():
                return True
        return False

    def find_next_edge(self, pos, previous_code):
        """
        pos: coords of current pixel
        previous_code: how to get to the previous pixel
        """
        start_code = (previous_code -1) % 8
        lookup = [x % 8 for x in xrange(start_code + 8, start_code, -1)]
        found_white = False
        for code in lookup:
            check_pos = self.from_chain_code(pos,code)
            if not self.image[check_pos[0]][check_pos[1]]:
                found_white = True
            elif not found_white:
                continue
            else:
                if self._is_inner_edge(check_pos):
                    return (code, check_pos)
                else:
                    continue
        raise Exception("Can't find new edge point")

    def _generate_chaincod_points(self, pos):
        pos = numpy.array(pos)
        current_pos = pos
        self.start_pos = pos
        self.chaincode_points = [pos]
        previous_code = 1  # tricky hack to get the start chaincode search
        while True:
            new_chaincode, next_pos = self.find_next_edge(current_pos,
                                                        previous_code + 4)
            print new_chaincode, next_pos
            print self.chaincode_points, self.chaincode
            sys.stdout.flush()
            if (next_pos == self.start_pos).all():
                self.chaincode.extend([new_chaincode])
                break
            self.chaincode_points.extend([next_pos])
            self.chaincode.extend([new_chaincode])
            current_pos = next_pos


    def generate_chaincode(self):
        starting = self.find_edge()
        self._generate_chaincod_points(starting)

if __name__ == "__main__":
    image1 = numpy.array([
            [255,255,255,255,255,255,255,255,255,],
            [255,255,255,255,0,255,255,255,255,],
            [255,255,255,0,0,0,255,255,255,],
            [255,255,0,0,0,0,0,255,255,],
            [255,255,255,0,0,0,255,255,255,],
            [255,255,255,255,0,255,255,255,255,],
            [255,255,255,255,255,255,255,255,255,],
            ])
    image2 = numpy.array([
            [255,255,255,255,255,255,255,255,255,],
            [255,255,0,0,0,0,0,255,255,],
            [255,255,0,0,0,0,0,255,255,],
            [255,255,0,0,0,0,0,255,255,],
            [255,255,0,0,0,0,0,255,255,],
            [255,255,0,0,0,0,0,255,255,],
            [255,255,255,255,255,255,255,255,255,],
            ])

    chaincode_image1 = ChainCodeImage(image1)
    chaincode_image2 = ChainCodeImage(image1)

    print chaincode_image1.generate_chaincode()
    print chaincode_image1.generate_chaincode()
