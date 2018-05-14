# !/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'FesianXu'
__date__ = '2018/5/13'
__version__ = ''


import queue

class FIFOQueue(object):
  '''
  FIFOQueue is designed to cache the batch sampling by DataLoader, it should be singleton and Global. This system should
  maintain only one FIFOQueue.
  a simple singleton wrapper of python bulit-in model queue
  NOT singleton anymore.
  '''
  __instance = None

  __max_len = None
  __queue = None
  def __init__(self, max_len=5):
    if self.__max_len is None:
      self.__max_len = max_len
    else:
      if self.__max_len is not max_len:
        raise ValueError('The FIFOQueue has been declared yet and max_len is not same!')

    if self.__queue is None:
      self.__queue = queue.Queue(maxsize=max_len)

  def enqueue(self, item):
    '''
    put a batch into queue. If the queue is full, then it will be blocked and wait until the queue is not full.
    :param item: a batch with the format of (data_batch, data_label)
    :return: None
    '''
    self.__queue.put(item)


  def dequeue(self):
    '''
    pop a batch from queue. If the queue is empty then it will be blocked till the queue is not empty.
    :return: the batch with the format of (data_batch, data_label)
    '''
    item = self.__queue.get()
    return item

  def max_len(self):
    return self.__max_len

  def get_len(self):
    return self.__queue.qsize()