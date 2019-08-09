import csv
import os

class Csv:
    def __init__(self, filepath, quotechar=','):
        self.filepath = filepath
        self.quotechar = quotechar

    def read(self):
        data_list = []
        with open(self.filepath, 'r') as f:
            data = csv.reader(f)
            for stu in data:
                data_list.append(stu)
        return data_list

    def write(self, data):
        try:
            with open(self.filepath, 'a', newline='') as f:
                csv_write = csv.writer(f)
                csv_write.writerow(data)
            return True
        except Exception as e:
            return e

    def insertRow(self, row, data):
        data_list = self.read()
        data_list.insert(row, data)
        self.write(data_list)
        return data_list

    def remove(self):
        os.remove(self.filepath)
