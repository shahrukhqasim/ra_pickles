import os
import shutil

from RandomAccessPickles.ra_pickles.random_access_pickles_reader import RandomAccessPicklesReader
from RandomAccessPickles import RandomAccessPicklesWriter
import numpy as np


fold = 'test_folder'
dataset = RandomAccessPicklesWriter(100, fold)

if os.path.exists(fold):
    if os.path.isdir(fold):
        shutil.rmtree(fold)
os.mkdir(fold)


for i in range(30):
    d = np.ones(4) * i
    dataset.add(d)

dataset.close()

dataset = RandomAccessPicklesReader(fold)
print("Total", dataset.get_total())

print("Trying to retreive")
for i in range(150):
    print("Retrieving",i)
    a = dataset.get_nth(i)
    print(i, a[0])

print("Here?")

dataset.close()