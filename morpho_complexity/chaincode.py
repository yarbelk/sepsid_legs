import numpy
import scipy
import sys




class ChainCodeImage(object):
    # For some reason, I have to define this column major.  I don't know why
    #TODO figure out why
    # check memory representation vs display order by printing out a gradent.
    neighbor_transform = numpy.array(
            [
                [-1, -1],[-1,  0] ,[ -1, 1],
                [0, -1],          [0,  1],
                 [1, -1],[1,  0] , [1,  1],
            ])

    # For some reason, I have to define this column major.  I don't know why
    #TODO figure out why
    chaincode_lookup = {
            0: (0,  1),
            1: (-1, 1),
            2: (-1, 0),
            3: (-1, -1),
            4: (0, -1),
            5: (1, -1),
            6: (1,  0),
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

    def _get_neighbors(self, pos):
        shape = self.image.shape
        neighbors = self.neighbor_transform + pos
        to_delete = []
        for i, neighbor in enumerate(neighbors):
            if (neighbor < 0).any() or (neighbor >= shape).any():
                to_delete.extend([i])
        to_delete.reverse()
        for i in to_delete:
            neighbors = numpy.delete(neighbors, i, 0)
        return neighbors

    def _is_inner_edge(self, pos):
        neighbors = self._get_neighbors(pos)
        neighbors_values = numpy.array([self.image[neighbor[0]][neighbor[1]] for neighbor  in neighbors])
        value = self.image[pos[0]][pos[1]]
        return value and not neighbors_values.all()

    def find_edge(self):
        it = numpy.nditer(self.image, flags=['multi_index'])
        while not it.finished:
            if self._is_inner_edge(it.multi_index):
                return it.multi_index
            it.iternext()
        sys.exit(1, "No Image edge")

#    def _numpy_in(self, x, data):
#        # silly kludge to compare against None in data
#        for y in data:
#            if (x == y).all():
#                return True
#        return False

    def find_next_edge(self, pos, previous_code):
        """
        pos: coords of current pixel
        previous_code: how to get to the previous pixel
        """
        start_code = (previous_code -1) % 8
        lookup = numpy.arange(start_code + 8, start_code, -1) % 8
        found_white = False
        for code in lookup:
            check_pos = self.from_chain_code(pos,code)
            if not self.image[check_pos[0]][check_pos[1]]:
                found_white = True
                continue
            elif not found_white:
                continue
            else:
                if self._is_inner_edge(check_pos):
                    return (code, check_pos)
                else:
                    continue
        raise Exception("Can't find new edge point")

    def _generate_chaincode_points(self, pos):
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
        self._generate_chaincode_points(starting)
        return self.chaincode

def print_state(image, current_pos, lookat_pos, chaincode):
    row = 0
    print '\n\n','='*80, '\n\n'
    it = numpy.nditer(image, flags=['multi_index'])
    for x in it:
        if it.multi_index[0] != row:
            print '\n',
            row +=1
        oc = '1'
        if not x:
            oc = '0'
        if (current_pos == it.multi_index).all():
            oc = 'X'
        # ugly
        if (lookat_pos == it.multi_index).all():
            oc = str(chaincode + 1)
        print oc,


if __name__ == "__main__":

    chaincode_image1 = ChainCodeImage(image1)
    chaincode_image2 = ChainCodeImage(image1)

    print chaincode_image1.generate_chaincode()
    print chaincode_image1.generate_chaincode()
