import gzip
import io
import os
import pickle
import queue
import threading
import time

import numpy as np
from tqdm import tqdm


class RandomAccessPicklesReader():
    def __init__(self, folder=None, files=None):
        """
        :param folder: The folder in which to create the dataset in
        :param files: Or just give it a list of files ('.bin') to read. The folder parameter will not be used if
                      files is not None
        """

        super(RandomAccessPicklesReader).__init__()

        if int(folder==None) + int(files==None) != 1:
            raise RuntimeError("Only set a folder of files")

        # self.data_queue = queue.Queue()
        if files is None:
            all_files = os.listdir(folder)
            all_files = [os.path.join(folder, x) for x in all_files]
            self.data_files = [os.path.splitext(x)[0]+'.bin' for x in all_files if x.endswith('.meta')]
            self.data_files = [x for x in self.data_files if x in all_files]
        else:
            self.data_files = files

        self.data_files.sort()
        self._read_meta()
        self.read_n_queue = None

    def _read_meta(self):
        meta_files = [os.path.splitext(x)[0]+'.meta' for x in self.data_files]

        self.metadata = []
        print("Reading meta files")
        for i in tqdm(range(len(meta_files))):
            metafile = meta_files[i]
            with open(metafile, 'rb') as f:
                _, m = pickle.load(f)
                self.metadata.append([0]+np.cumsum(m).tolist())

        self.current_file_index = 0
        self.current_file = None
        self.current_data_index = 0

    def __iter__(self):
        return self

    def get_total(self):
        """
        Get total number of entries in the dataset

        :return: An integer representing total number of entries
        """

        return int(np.sum([len(x)-1 for x in self.metadata]))

    def get_nth_file_and_loc(self, n):
        the_file = None
        reading_seek_start = -1
        reading_seek_end = -1
        elements_skipped = 0
        for i, m in enumerate(self.metadata):
            if n >= elements_skipped and n < (elements_skipped + len(m) - 1):
                reading_seek_start = m[n - elements_skipped]
                reading_seek_end = m[n - elements_skipped + 1]
                the_file = self.data_files[i]

            elements_skipped += len(m) - 1

        if reading_seek_start == -1:
            return None
        # t1 = time.time()
        bin_length = reading_seek_end - reading_seek_start
        return the_file, reading_seek_start, bin_length

    def _data_reading_thread(self, process):
        while True:
            try:
                nth = self.read_n_queue.get(timeout=3)
                if nth is None:
                    break
            except queue.Empty:
                continue
            try:
                result = self.get_element(nth, process=process)
            except OSError as e:
                print("Error occurred")
                result = None

            self.read_n_queue_output.put((nth, result))


    def start_parallel_retrieval_threads(self, n_theads):
        """
        Start threads to retrieve multiple elements in parallel (using get_multi_in_parallel function).

        :param n_theads: Number of threads to use
        :return: Doesn't return anything
        """
        the_threads = []
        self.read_n_queue = queue.Queue()
        self.read_n_queue_output = queue.Queue()

        for i in range(n_theads):
            t = threading.Thread(target=self._data_reading_thread, args=(True,))
            the_threads.append(t)
            t.start()

        self._data_reading_threads = the_threads

    def close_parallel_retrieval_threads(self):
        """
        Close the parallel retrieval threads
        :return: Doesn't return anything
        """

        for _ in self._data_reading_threads:
            self.read_n_queue.put(None)
            self.read_n_queue.put(None)

        for x in self._data_reading_threads:
            x.join()


    def get_multi_in_parallel(self, indices, timeout=30):
        """
        Get multiple dataset elements in parallel for a faster access

        :param indices: A list of indices what to retreive
        :param timeout: Timeout in secconds
        :return: A list of retreived dataset elements
        """

        if self.read_n_queue is None:
            raise RuntimeError('Please call start_async_threads before!')

        N = indices
        for n in N:
            self.read_n_queue.put(n)
        N = set(N)

        # arguments = {
        #
        # }
        # for n in N:
        #     the_file, reading_seek_start, bin_length =
        #     if n in arguments:
        #         arguments[n].append(())

        results = list()
        N_recieved = set()

        while True:
            try:
                nth, result = self.read_n_queue_output.get(timeout=timeout)
            except queue.Empty:
                break
            N_recieved.add(nth)
            results.append(result)
            if len(N.intersection(N_recieved)) == len(N):
                break

        return results


    def get_element(self, index, process=True):
        # t1 = time.time()
        the_file, reading_seek_start, bin_length = self.get_nth_file_and_loc(index)

        # print("Reading took",time.time()-t1,"seconds")
        # t1 = time.time()
        try:
            file = open(the_file, 'rb')
            file.seek(reading_seek_start)
            d = file.read(bin_length)
        except OSError as e:
            print("Eror occurred in",the_file,reading_seek_start, bin_length)
            raise e

        # print("Bytes",len(d))
        if process:
            d = self._unprocess(d)
        # print("Unprocessing took",time.time()-t1,"seconds")
        file.close()
        # print("in:",time.time()-t1)

        return d


    def __next__(self):
        # print("Calling next")
        # if self.current_file is None:
        #     self.current_data_index = 0

        self.current_file = open(self.data_files[self.current_file_index], 'rb')
        self.current_file.seek(self.metadata[self.current_file_index][self.current_data_index])

        bin_length = self.metadata[self.current_file_index][self.current_data_index+1]-self.metadata[self.current_file_index][self.current_data_index]
        d = self._unprocess(self.current_file.read(bin_length))

        self.current_data_index += 1
        self.current_file.close()

        if self.current_data_index == len(self.metadata[self.current_file_index]) - 1:
            # self.current_file = None
            self.current_file_index += 1
            self.current_data_index = 0

            if self.current_file_index == len(self.metadata):
                self.current_file_index = 0

        # print("Next done", typeg)

        return d

    def close(self):
        """
        Close the reader
        :return: Nothing
        """
        if self.current_file is not None:
            self.current_file.close()
            self.current_file = None


    def _unprocess(self, data):
        binary_data = io.BytesIO(data)
        gzipfile = gzip.GzipFile(fileobj=binary_data, mode='rb')
        data_loaded = pickle.load(gzipfile)
        gzipfile.close()

        return data_loaded

    def _process(self, data):
        binary_data = io.BytesIO()
        gzipfile = gzip.GzipFile(fileobj=binary_data, mode='wb')
        pickle.dump(data, gzipfile)
        gzipfile.close()



