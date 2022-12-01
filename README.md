#RA Pickles
A simple package to create and access datasets based on python objects using pickles.
A dataset will be represented by a directory. And the files in the directory contain the data.
As file identifiers are randomly generated, files from two dataset folders can be added to
each other create a larger dataset. 

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
dataset = RandomAccessPicklesWriter(100, fold)
```

Now entries to the dataset can be added as follows:
```
for i in range(30):
    d = np.ones(4) * i
    dataset.add(d)
dataset.close()
```
Here, `30` numpy arrays have been added. 

To access contents in the dataset, use the following code:
```
dataset = RandomAccessPicklesReader(fold)
print("Total", dataset.get_total())

print("Trying to retreive")
for i in range(30):
    print("Retrieving",i)
    a = dataset.get_nth(i)
    print(i, a[0])
```

Good luck!

