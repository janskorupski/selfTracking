import os
import numpy as np
import pandas as pd
from pandas import DataFrame


def is_recorder_data(file):
    if len(file.split(".")) != 2:
        return False
    if not file.split(".")[1] == "txt":
        return False
    listed = file[:-4].split("-")
    if len(listed) != 3:
        return False
    if any([not el.isnumeric for el in listed]):
        return False
    try:
        with open(file, "r", encoding="utf-8") as f:
            if len(f.readline().split(";")) != 13:
                return False
    except UnicodeDecodeError:
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

        header = "year;month;day;hour;min;sec;weekday;secStart;secSpent;active;Window;textWritten;keysPressed".split(";")
        self.raw_data = []
        for file in os.listdir(self.data_directory):
            if is_recorder_data(file):
                self.raw_data.append(pd.read_csv(file, sep=";", encoding="utf-8", index_col=None, names=header))
        self.raw_data = pd.concat(self.raw_data)

        self.raw_data["textWritten"] = self.raw_data["textWritten"].fillna("")
        self.raw_data["keysPressed"] = self.raw_data["keysPressed"].fillna("")
        self.raw_data["Window"]      = self.raw_data["Window"].fillna("")

        self.raw_data = self.raw_data.reset_index()


    def make_time_series(self, statistic , sample_frequency = 60*1 ):

        block_times = pd.DataFrame({"start": self.raw_data.secStart, "end": self.raw_data.secStart + self.raw_data.secSpent})
        block_times["duration"] = block_times.end - block_times.start
        block_times = block_times.reset_index()

        statistics = self.raw_data.apply(statistic, axis=1)

        block_times = block_times.loc[ (statistics != 0).any(axis = 1) , : ]
        statistics  = statistics.loc[  (statistics != 0).any(axis = 1) , : ]

        block_times = block_times.reset_index()
        statistics  = statistics.reset_index()

        first_second = min(block_times.start)
        last_second = max(block_times.end)
        sample_time = list(range(round(first_second), round(last_second), sample_frequency))

        result: DataFrame = pd.DataFrame(np.zeros((len(sample_time), statistics.shape[1])), columns=statistics.columns)
        result.index = sample_time

        block_pointer = 0
        for time in sample_time:
            while block_times.start[block_pointer] <= time + sample_frequency:
                common_start = max(block_times.start[block_pointer], time)
                common_end = min(block_times.end[block_pointer], time + sample_frequency)

                common_time = common_end - common_start
                result.loc[time, :] += common_time / sample_frequency * statistics.iloc[block_pointer, :]

                block_pointer += 1
                if block_pointer >= block_times.shape[0]:
                    break
            block_pointer -= 1
            if block_pointer < 0:
                block_pointer = 0

        return result

def words_per_second(row):
    return (len(row.textWritten.split(" ")) - 1)/row.secSpent

def letters_per_second(row):
    return (len(row.textWritten))/row.secSpent

if __name__ == "__main__":
    analyzer = Analyzer()
    analyzer.load_raw_data()
    analyzer.raw_data
    aaa = analyzer.make_time_series([letters_per_second,words_per_second])
    aaa
