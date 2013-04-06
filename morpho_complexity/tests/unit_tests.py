from unittest import TestCase
from morpho_complexity import chaincode
import numpy as np


class ChainCodeTests(TestCase):

    def test_horizontal(self):
        horz = np.array([
            [255,255,255,255,255],
            [255,0,0,0,255],
            [255,255,255,255,255],
        ])
        horz_cci = chaincode.ChainCodeImage(horz)
        chaincode_result = horz_cci.generate_chaincode()
        self.assertEquals([0,0,4], chaincode_result)

    def test_small_square(self):
        horz = np.array([
            [255,255,255,255],
            [255,0,0,255],
            [255,0,0,255],
            [255,255,255,255],
        ])
        horz_cci = chaincode.ChainCodeImage(horz)
        chaincode_result = horz_cci.generate_chaincode()
        self.assertEquals([0,6,4], chaincode_result)

    def test_big_square(self):
        horz = np.array([
            [255,255,255,255,255],
            [255,0,0,0,255],
            [255,0,0,0,255],
            [255,0,0,0,255],
            [255,255,255,255,255],
        ])
        horz_cci = chaincode.ChainCodeImage(horz)
        chaincode_result = horz_cci.generate_chaincode()
        self.assertEquals([0,0,6,6,4,4,2], chaincode_result)

    def test_vertical(self):
        vert = np.array([
            [255,255,255,],
            [255,0,255,],
            [255,0,255,],
            [255,0,255,],
            [255,255,255,],
        ])
        vert_cci = chaincode.ChainCodeImage(vert)
        chaincode_result = vert_cci.generate_chaincode()
        self.assertEquals([6,6,2], chaincode_result)

    def test_forward(self):
        forward = np.array([
            [255,255,255,255,255],
            [255,255,255,0,255],
            [255,255,0,255,255],
            [255,0,255,255,255],
            [255,255,255,255,255],
        ])
        forward_cci = chaincode.ChainCodeImage(forward)
        chaincode_result = forward_cci.generate_chaincode()
        self.assertEquals([5,5,1], chaincode_result)

    def test_back(self):
        back = np.array([
            [255,255,255,255,255],
            [255,0,255,255,255],
            [255,255,0,255,255],
            [255,255,255,0,255],
            [255,255,255,255,255],
        ])
        back_cci = chaincode.ChainCodeImage(back)
        chaincode_result = back_cci.generate_chaincode()
        self.assertEquals([7,7,3], chaincode_result)

    def test_cross(self):
        cross = np.array([
            [255,255,255,255,255,255,255,255,255],
            [255,255,255,255,0,255,255,255,255],
            [255,255,255,255,0,255,255,255,255],
            [255,255,255,255,0,255,255,255,255],
            [255,0,0,0,0,0,0,0,255],
            [255,255,255,255,0,255,255,255,255],
            [255,255,255,255,0,255,255,255,255],
            [255,255,255,255,0,255,255,255,255],
            [255,255,255,255,255,255,255,255,255],
        ])
        cross_cci = chaincode.ChainCodeImage(cross)
        chaincode_result = cross_cci.generate_chaincode()
        expected_code = [6,6,7,0,0,4,4,5,6,6,2,2,3,4,4,0,0,1,2]
        self.assertEquals(expected_code, chaincode_result)
