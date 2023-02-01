import os
import numpy as np
import pandas as pd
from pandas import DataFrame

import Janitor


def is_recorder_data(file):
    if not os.path.isfile(file):
        return False
    if not os.path.splitext('./data/2022-10-25.txt')[1] in [".txt", ".csv"]:
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
        with open(file, "r", encoding="ANSI") as f:
            if len(f.readline().split(";")) != 13:
                return False
    except UnicodeDecodeError:
        return False
    return True


class Analyzer():

    def __init__(self, data_directory=".", flag_data=None, raw_data=None, flag_rules=None, flag_separator=chr(164)):

        self.data_directory = data_directory
        self.flag_data = flag_data
        self.flag_rules = flag_rules
        self.hand_flagged_windows = None
        self.flags = None
        if not self.flag_data:
            expected_path = os.path.join(self.data_directory, "hand_flagged_windows.csv")
            if os.path.exists(expected_path):
                self.hand_flagged_windows = expected_path
        if not self.flag_data:
            expected_path = os.path.join(self.data_directory, "flag_data.csv")
            if os.path.exists(expected_path):
                self.flag_data = expected_path
        if not self.flag_rules:
            expected_path = os.path.join(self.data_directory, "flag_rules.csv")
            if os.path.exists(expected_path):
                self.flag_rules = expected_path
        self.raw_data = raw_data

        self.flag_separator = flag_separator

    def update_flag_file(self):
        # the method takes the 'flag rules' file as well as the 'hand_flagged_windows' file as input
        #  (also adds missing, unflagged windows to the hand_flagged_windows file) and creates
        #  'flag_data' file as output, to later be used during time series data creation
        all_windows = set(self.raw_data.Window)

        #  if file does not exist, create an empty file
        if not self.flag_data:
            self.flag_data = os.path.join(self.data_directory, "flag_data.csv")
            with open(self.flag_data, "w", encoding="utf-8") as file:
                file.write(f"window{self.flag_separator}flag")

        #  if file does not exist, create an empty file
        if not self.flag_rules:
            self.flag_rules = os.path.join(self.data_directory, "flag_rules.csv")
            with open(self.flag_rules, "w", encoding="utf-8") as file:
                file.write(f"rule{self.flag_separator}flag")

        #  if file does not exist, create an empty file
        if not self.hand_flagged_windows:
            self.hand_flagged_windows = os.path.join(self.data_directory, "hand_flagged_windows.csv")
            with open(self.hand_flagged_windows, "w", encoding="utf-8") as file:
                file.write(f"window{self.flag_separator}flag")

        #  read the 'flag_data.csv' data
        flag_data = pd.read_csv(self.flag_data, encoding="utf-8", sep=self.flag_separator, dtype='str', index_col=None)

        #  read the 'hand_flagged_windows.csv' data
        hand_flagged_windows = pd.read_csv(self.hand_flagged_windows, encoding="utf-8", sep=self.flag_separator, dtype='str', index_col=None)
        hand_flagged_windows = hand_flagged_windows.fillna("")

        #  read the 'flag_rules.csv' data
        flag_rules = pd.read_csv(self.flag_rules, encoding="utf-8", sep=self.flag_separator, dtype='str', index_col=None)
        flag_rules = flag_rules.fillna("")

        #  set flags according to rules and list all remaining
        unflagged_windows = []
        self.flags = {}
        for window in all_windows:
            for idx, row in flag_rules.iterrows():
                if row.rule in window:
                    self.flags[window] = row.flag
                    break
            if window not in self.flags:
                unflagged_windows.append(window)
                self.flags[window] = ""

        for idx, row in hand_flagged_windows.iterrows():
            if row.flag != "":
                self.flags[row.window] = row.flag

        #  get rid of all the windows which were flagged by hand from 'unflagged_windows' list
        unflagged_windows = [window for window in unflagged_windows if window not in hand_flagged_windows.window]
        if len(unflagged_windows) > 0:
            tmp_data_frame = pd.DataFrame({"window": unflagged_windows, "flag": ""})
            hand_flagged_windows = pd.concat([hand_flagged_windows, tmp_data_frame])

        #  update hand-flagging file
        hand_flagged_windows.to_csv(self.hand_flagged_windows, encoding="utf-8", sep=self.flag_separator, index=False)

        #  update flag data file
        flag_dataFrame_to_save = pd.DataFrame( self.flags , index=[1] ).T.reset_index()
        flag_dataFrame_to_save.columns = ["window", "flag"]
        flag_dataFrame_to_save.to_csv(self.flag_data, encoding="utf-8", sep=self.flag_separator, index=False)


    def load_raw_data(self):

        header = "year;month;day;hour;min;sec;weekday;secStart;secSpent;active;Window;textWritten;keysPressed".split(
            ";")
        self.raw_data = []
        for file in os.listdir(self.data_directory):
            file = os.path.join(self.data_directory, file)
            if is_recorder_data(file):

                try:
                    new_data = pd.read_csv(file, sep=";", encoding="utf-8", index_col=None, names=header)
                except pd.errors.ParserError:
                    Janitor.reseparate(file, new_seperator=chr(164))
                    pd.read_csv(file, sep=chr(164), encoding="utf-8", index_col=None, names=header)
                except:
                    raise Exception(f"Cannot read file: {file} ")

                self.raw_data.append(new_data)

        self.raw_data = pd.concat(self.raw_data)

        self.raw_data["textWritten"] = self.raw_data["textWritten"].fillna("")
        self.raw_data["keysPressed"] = self.raw_data["keysPressed"].fillna("")
        self.raw_data["Window"] = self.raw_data["Window"].fillna("")

        self.raw_data = self.raw_data.reset_index()

    def make_time_series(self, statistic, sample_frequency=60 * 1):

        block_times = pd.DataFrame(
            {"start": self.raw_data.secStart, "end": self.raw_data.secStart + self.raw_data.secSpent})
        block_times["duration"] = block_times.end - block_times.start
        block_times = block_times.reset_index()

        statistics = self.raw_data.apply(statistic, axis=1)

        block_times = block_times.loc[(statistics != 0).any(axis=1), :]
        statistics = statistics.loc[(statistics != 0).any(axis=1), :]

        block_times = block_times.reset_index()
        statistics = statistics.reset_index()

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

                common_time = max(common_end - common_start, 0)
                aa = common_time / sample_frequency * statistics.iloc[block_pointer, :]
                result.loc[time, :] += aa

                if common_time < 0:
                    pass

                block_pointer += 1
                if block_pointer >= block_times.shape[0]:
                    break
            block_pointer -= 1
            if block_pointer < 0:
                block_pointer = 0

        return result


def words_per_second(row):
    return (len(row.textWritten.split(" ")) - 1) / row.secSpent


def letters_per_second(row):
    return (len(row.textWritten)) / row.secSpent


if __name__ == "__main__":
    analyzer = Analyzer(data_directory="./data/")
    analyzer.load_raw_data()
    analyzer.raw_data
    analyzer.update_flag_file()
    #aaa = analyzer.make_time_series([letters_per_second, words_per_second])
    #aaa.to_csv("time_series.csv", sep=";")
