import gzip
import io
import pickle

import networkx as nx
import torch
from datasets.binary_iterable_dataset_reader import BinaryIterableDataseReader
from datasets.binary_iterable_dataset import BinaryIterableDatasetWriter
import numpy as np


dataset = BinaryIterableDataseReader('/Users/shahrukhqasim/Workspace/NextCal/ShahRukhStudies/toydetector2/scripts/sample_particles/bid')

print("Trying to retreive")
for i in range(150):
    print("Retrieving",i)
    a = dataset.__next__()
    # print(i, a[0])

print("Here?")

dataset.close()


# file = '/Users/shahrukhqasim/Workspace/NextCal/ShahRukhStudies/toydetector2/scripts/sample_particles/bid/data_00395629-d4c9-4963-89e9-a369eb1f37a6.bin'
# meta = '/Users/shahrukhqasim/Workspace/NextCal/ShahRukhStudies/toydetector2/scripts/sample_particles/bid/data_00395629-d4c9-4963-89e9-a369eb1f37a6.meta'
#
#
# with open(meta, 'rb') as f:
#     _, splits = pickle.load(f)
#
# print(splits)
# print(np.cumsum(splits))
#
# # print(np.sum(splits))
#
# binary_file = open(file, 'rb')
#
# start = 0
# for s in splits:
#     binary_file.seek(start)
#     print(start,s)
#     binary_data = binary_file.read(s)
#     binary_data = io.BytesIO(binary_data)
#     gzipfile = gzip.GzipFile(fileobj=binary_data, mode='rb')
#     data_loaded = pickle.load(gzipfile)
#     gzipfile.close()
#
#     start += s
#
# binary_file.close()