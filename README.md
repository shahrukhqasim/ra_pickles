# RA Pickles
In many applications, elements from a large dataset, that cannot be stored in memory, need
to be sampled (with or without replacement). This simple package simplifies this process
by allowing storage of large datasets by splitting them over multiple files in a directory.
Once that's done, any dataset element can be queried. Further, most python objects as dataset elements can be used as pickles are used at the backend.


As mentioned before, a dataset will be represented by a directory that contains
two sets of files, meta and data. The file identifiers are randomly generated and therefore,
two datasets can be added together to create a larger dataset without additional work.
This also allows multiple applications to add elements to the dataset in parallel. An example
is multiple simulations running in parallel.

## Installation
`pip3 install ra-pickles`

## Example
First import all the packages
```
from ra_pickles import RandomAccessPicklesReader, RandomAccessPicklesWriter
import shutil
import os
import numpy as np
```

So to create a dataset in `test_folder`, use the following code. `100` here
specifies number of dataset samples in each file. If there are more than `100`
files, multiple files will be created. Heuristically, this number can be chosen
such that resulting data files are approximately `1 GB`, although this wouldn't
affect performance much as a complete file is not fully loaded into memory. 
On the other hand, a too small number can also affect performance as some file
systems create issues if there are too many files.
```
fold = 'test_folder'
writer = RandomAccessPicklesWriter(100, fold)
```

Now entries to the dataset can be added as follows:
```
for i in range(30):
    # d is the dataset element which can be any python object
    d = np.ones(4) * i
    
    # and you add it to the dataset
    writer.add(d)
writer.close()
```
Here, `30` numpy arrays have been added. 

To sample elements in the dataset, use the following code:
```
reader = RandomAccessPicklesReader(fold)
print("Total", reader.get_total())

print("Trying to retreive")
for i in range(30):
    print("Retrieving",i)
    a = reader.get_element(i)
    print(i, a[0])
```
The index retrieval index can be randomly generated --`[0, reader.get_total() )`
to sample random elements.

Multiple elements can also be retrieved in parallel for fast access. To do so, first,
retrieval threads must be started (and closed at the end):
```
reader.start_parallel_retrieval_threads(n_theads=5)
data = reader.get_multi_in_parallel([1,2,3])
reader.close_parallel_retrieval_threads()
reader.close()
```

Good luck!

