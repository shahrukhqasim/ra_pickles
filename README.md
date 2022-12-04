# RA Pickles
In many applications, elements from a large dataset, that cannot be stored in memory, need
to be sampled (with or without replacement). This package simplifies this process by allowing random access to
elements in large datasets. Most python objects as dataset elements
can be used as pickles are used at the backend.


A dataset will be represented by a directory, stored in combination of meta and data files.
As file identifiers are randomly generated, two datasets can be added to
each other create a larger dataset without additional work. This also allows multiple
applications to add elements to the dataset in parallel.

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
files, multiple files will be created.
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

To access contents in the dataset, use the following code:
```
reader = RandomAccessPicklesReader(fold)
print("Total", reader.get_total())

print("Trying to retreive")
for i in range(30):
    print("Retrieving",i)
    a = reader.get_element(i)
    print(i, a[0])
```

Multiple elements can also be retrieved in parallel for fast access. To do so, first,
retrieval threads must be started (and closed at the end):
```
reader.start_parallel_retrieval_threads(n_theads=5)
data = reader.get_multi_in_parallel([1,2,3])
reader.close_parallel_retrieval_threads()
reader.close()
```

Good luck!

