import csv
from abc import ABCMeta, abstractmethod
from itertools import groupby
from datetime import datetime


class CSVCommon(metaclass=ABCMeta):
  HEADER = ["url", "id",
            "year", "month", "day", "hour", "minute",
            "category",
            "title",
            "summary1", "summary2", "summary3",
            "body"]

  @abstractmethod
  def __del__(self):
    pass


class Writer(CSVCommon):
  def __init__(self, path):
    self.f = open(path, 'w')
    self.writer = csv.writer(self.f)
    self.writer.writerow(self.HEADER)

  def write(self, data):
    self.writer.writerow(data)

  def __del__(self):
    self.f.close()


class Reader(CSVCommon):
  def __init__(self, path):
    self.f = open(path, 'r')
    self.reader = csv.DictReader(self.f)

  def latest_date(self):
    result = {}
    articles = [art for art in self.reader]
    articles.sort(key=lambda a: a[self.HEADER[7]])
    for key, group in groupby(articles, key=lambda a: a[self.HEADER[7]]):
      date = max([datetime(int(art[self.HEADER[2]]),
                           int(art[self.HEADER[3]]),
                           int(art[self.HEADER[4]]),
                           int(art[self.HEADER[5]]),
                           int(art[self.HEADER[6]])) for art in group])
      result[key] = date
    return result

  def __del__(self):
    self.f.close()

