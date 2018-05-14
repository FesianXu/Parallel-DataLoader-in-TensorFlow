# !/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'FesianXu'
__date__ = '2018/5/13'
__version__ = ''

import FIFOqueue as queue
import threading


class Train(object):
  _train_global_queue = None
  _val_global_queue = None
  _test_global_queue = None
  _threads = []

  def __init__(self,
               main_task,
               batch_size=32,
               train_yield=None,
               val_yield=None,
               test_yield=None,
               max_nthread=10,
               max_len=10):
    self._train_global_queue = queue.FIFOQueue(max_len=max_len) if train_yield is not None else None
    self._val_global_queue = queue.FIFOQueue(max_len=max_len) if val_yield is not None else None
    self._test_global_queue = queue.FIFOQueue(max_len=max_len) if test_yield is not None else None
    # init the global queue and maintain them
    train_threads = [threading.Thread(target=self._data_enqueue,
                     args=(train_yield, batch_size, task_id, 'train_data_load', self._train_global_queue))
    for task_id in range(max_nthread)]

    def wrapper_main_task(fn):
      while True:
        fn(self._train_global_queue.dequeue())

    self._threads += train_threads
    self._threads += [threading.Thread(target=wrapper_main_task, args=([main_task]))]

  def _data_enqueue(self, fn, batch_size, task_id, task_type, queue_h):
    print('here begin the data loading with task_id %d with type %s' % (task_id, task_type))
    while True:
      item = fn()
      item['task_id'] = task_id
      item['task_type'] = task_type
      queue_h.enqueue(item=item)


  def start(self):
    for each_t in self._threads:
      each_t.start()


if __name__ == '__main__':
  print('k')
  import os
  import random
  import numpy as np
  import scipy.io as sio
  import time

  def _train_yield():
    path = '/home/your_name/AI_workspace/datasets/raw/mats/'
    while True:
      dirs = os.listdir(path)
      random.shuffle(dirs)
      dirs = dirs[0:32]
      mat_list = []
      labels = []
      time.sleep(1)
      for ind, each in enumerate(dirs):
        name = path+each
        mat = sio.loadmat(name)
        mat = mat['skel']
        mat = np.reshape(mat, newshape=(-1, 75))
        mat_list.append(mat)
        labels.append(12)
      return {'x_train':mat_list, 'y_train':labels}

  yy = _train_yield()

  sess = 0
  def _train_proc(data):
    x_train = data['x_train']
    y_train = data['y_train']
    print(y_train)
    time.sleep(0.2)
    feed_dict = {

    }

  train = Train(main_task=_train_proc, train_yield=_train_yield, max_nthread=10)
  #
  train.start()



