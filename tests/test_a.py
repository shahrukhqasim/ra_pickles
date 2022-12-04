import os
import shutil

from ra_pickles import RandomAccessPicklesReader, RandomAccessPicklesWriter
import numpy as np
import unittest


class TestCase(unittest.TestCase):
    def setUp(self):
        self.fold = 'test_fold'
        self.num_entires = 107

        if os.path.exists(self.fold):
            if os.path.isdir(self.fold):
                shutil.rmtree(self.fold)
        os.mkdir(self.fold)

    def tearDown(self):
        if os.path.exists(self.fold):
            if os.path.isdir(self.fold):
                shutil.rmtree(self.fold)

    def test_write_and_write(self):
        dataset = RandomAccessPicklesWriter(self.num_entires, self.fold)
        for i in range(self.num_entires):
            d = np.ones(4) * i
            dataset.add(d)

        dataset.close()

        dataset = RandomAccessPicklesReader(self.fold)
        total = dataset.get_total()
        assert self.num_entires == total

        for i in range(self.num_entires):
            a = dataset.get_nth(i)
            assert a[0] == i

        dataset.close()

    def test_write_and_write_2(self):
        dataset = RandomAccessPicklesWriter(50, self.fold)
        for i in range(self.num_entires):
            d = np.ones(4) * i
            dataset.add(d)

        dataset.close()

        dataset = RandomAccessPicklesReader(self.fold)
        total = dataset.get_total()
        assert self.num_entires == total

        for i in range(self.num_entires):
            a = dataset.get_nth(i)

        dataset.close()


if __name__ == '__main__':
    unittest.main()
