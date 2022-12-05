import os
import shutil

from RandomAccessPickles.ra_pickles import RandomAccessPicklesReader, RandomAccessPicklesWriter
# from RandomAccessPickles.ra_pickles.random_access_pickles_reader import RandomAccessPicklesReader
# from RandomAccessPickles.ra_pickles.random_access_pickles_writer import RandomAccessPicklesWriter

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
            a = dataset.get_element(i)
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
            a = dataset.get_element(i)

        dataset.close()

    def test_aync(self):
        dataset = RandomAccessPicklesWriter(self.num_entires, self.fold)
        for i in range(self.num_entires):
            d = np.ones(4) * i
            dataset.add(d)

        dataset.close()

        dataset = RandomAccessPicklesReader(self.fold)
        dataset.start_parallel_retrieval_threads(n_theads=5)

        data = dataset.get_multi_in_parallel([1,2,3])

        dataset.close_parallel_retrieval_threads()

        dataset.close()


if __name__ == '__main__':
    unittest.main()
