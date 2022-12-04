import gzip
import io
import os
import pickle
import threading
import queue
import time
import uuid
from io import BytesIO

class RandomAccessPicklesWriter:
    def __init__(self, num_samples_per_file, output_folder):
        self.num_samples_per_file = num_samples_per_file
        self.data_queue = queue.Queue()
        self.output_folder = output_folder

        # self.file_number=0

    def _process(self, data):
        # t1 = time.time()
        binary_data = io.BytesIO()
        gzipfile = gzip.GzipFile(fileobj=binary_data, mode='wb', compresslevel=1)
        pickle.dump(data, gzipfile)
        gzipfile.close()
        gzip_binary_data = binary_data.getvalue()

        return gzip_binary_data

    def _unprocess(self, data):
        binary_data = io.BytesIO(data)
        gzipfile = gzip.GzipFile(fileobj=binary_data, mode='rb')
        data_loaded = pickle.load(gzipfile)
        gzipfile.close()

        return data_loaded

    def write_to_file(self, processed_data):
        uu_filename = str(uuid.uuid4())
        filename_data = os.path.join(self.output_folder, 'data_'+str(uu_filename)+'.bin')
        filename_meta = os.path.join(self.output_folder, 'data_'+str(uu_filename)+'.meta')

        splits = []
        with open(filename_data, 'wb') as f:
            for i in range(len(processed_data)):
                    splits.append(len(processed_data[i]))
                    f.write(processed_data[i])

        metadata = {'format':'BIDv0.9'}

        with open(filename_meta, 'wb') as f:
            pickle.dump((metadata, splits), f)

        # f = open(filename_data, 'rb')
        # done = 0
        # for i in range(len(splits)):
        #     f.seek(done)
        #     len_ = splits[i]
        #     print("X", i, len_)
        #     x = self.unprocess(f.read(len_))
        #     done += len_
        # f.close()

        # self.file_number += 1

    def _read_file(self, file):
        filename_data = os.path.join(file)
        filename_meta = os.path.splitext(file)[0] + '.meta'

        with open(filename_meta, 'rb') as f:
            splits = pickle.load(f)


        all_data_loaded = []
        with open(filename_data, 'rb') as f:
            for s in splits:
                all_data_loaded.append(self._unprocess(f.read(s)))

        return all_data_loaded


    def add(self, sample):
        processed_data = self._process(sample)

        self.data_queue.put(processed_data)

        if self.data_queue.qsize() >= self.num_samples_per_file:
            data_to_be_pushed = []
            while self.data_queue.qsize() > 0:
                processed_data = self.data_queue.get()
                data_to_be_pushed.append(processed_data)

            self.write_to_file(data_to_be_pushed)


    def close(self):
        if self.data_queue.qsize() == 0:
            return

        data_to_be_pushed = []
        while self.data_queue.qsize() > 0:
            processed_data = self.data_queue.get()
            data_to_be_pushed.append(processed_data)

        self.write_to_file(data_to_be_pushed)



