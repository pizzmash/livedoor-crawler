import csv


class Writer:
  HEADER = ["url", "id",
            "year", "month", "day", "hour", "minute",
            "category",
            "title",
            "summary1", "summary2", "summary3",
            "body"]

  def __init__(self, path):
    self.f = open(path, 'w')
    self.writer = csv.writer(self.f)
    self.writer.writerow(self.HEADER)

  def write(self, data):
    self.writer.writerow(data)

  def __del__(self):
    self.f.close()

