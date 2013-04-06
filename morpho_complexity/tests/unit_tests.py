from unittest import TestCase
from morpho_complexity import chaincode
import numpy as np


class ChainCodeTests(TestCase):
    image1 = np.array([
            [255,255,255,255,255,255,255,255,255,],
            [255,255,255,255,0,255,255,255,255,],
            [255,255,255,0,0,0,255,255,255,],
            [255,0,0,0,0,0,0,255,255,],
            [255,255,255,0,0,0,255,255,255,],
            [255,255,255,255,0,255,255,255,255,],
            [255,255,255,255,255,255,255,255,255,],
            ])
    image2 = np.array([
            [255,255,255,255,255,255,255,255,255,],
            [255,255,0,0,0,0,0,255,255,],
            [255,255,0,0,0,0,0,255,255,],
            [255,255,0,0,0,0,0,255,255,],
            [255,255,0,0,0,0,0,255,255,],
            [255,255,0,0,0,0,0,255,255,],
            [255,255,255,255,255,255,255,255,255,],
            ])

    def test_horizontal(self):
        horz = np.array([
            [255,255,255,255,255],
            [255,0,0,0,255],
            [255,255,255,255,255],
        ])
        horz_cci = chaincode.ChainCodeImage(horz)
        chaincode_result = horz_cci.generate_chaincode()
        self.assertEquals([0,0,4], chaincode_result)

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
        back = np.array([
            [255,255,255,255,255,255,255,255],
            [255,255,255,0,255,255,255,255],
            [255,255,255,0,255,255,255,255],
            [255,255,255,0,255,255,255,255],
            [255,0,0,0,0,0,0,255],
            [255,255,255,0,255,255,255,255],
            [255,255,255,0,255,255,255,255],
            [255,255,255,255,255,255,255,255],
        ])
        back_cci = chaincode.ChainCodeImage(back)
        chaincode_result = back_cci.generate_chaincode()
        self.assertEquals([6,6,7,0,0,4,4,5,6,6,3,4,4,0,0,1,2], chaincode_result)
