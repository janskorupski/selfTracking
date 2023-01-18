import pandas
import pandas as dp
import os

import pandas as pd


def is_recorder_data(file):
    if not file.split(".")[1] == "txt":
        return False
    listed = file[:-4].split(";")
    if len(listed) != 3:
        return False
    if any([not el.isnumeric for el in listed]):
        return False
    with open(file, "r", encoding="utf-8") as f:
        if len(f.readline().split(";")) != 13:
            return False
    return True


class Analyzer():

    def __init__(self, data_directory=".", flag_data=None, raw_data=None):

        self.data_directory = data_directory
        self.flag_data = flag_data
        if not self.flag_data:
            if os.path.exists("flag_data.txt"):
                self.flag_data = "flag_data.txt"
        self.raw_data = raw_data

    def setup_flags(self):
        pass

    def load_raw_data(self):
        header = "year;month;day;hour;min;sec;weekday;secStart;secSpent;active;Window;textWritten".split(";")
        self.raw_data = []
        for file in os.listdir(self.data_directory):
            if is_recorder_data(file):
                self.raw_data.append(pd.read_csv(file, sep=";", index_col=None, names=header))
        self.raw_data = pd.concat(self.raw_data)



if __name__ == "__main__":
    print(is_recorder_data(os.listdir()[4]))
