from statistics import mean
import re
import string
import numpy as np
words_only = re.compile('\w+')


class Statistic:

    def __init__(self, name, calc_func):
        self.name = name
        self.calculate = calc_func


textWritten_stat = Statistic("textWritten", lambda keysPressed, textWritten: textWritten)
keysPressed_stat = Statistic("keysPressed", lambda keysPressed, textWritten: keysPressed)
symbolCount_stat = Statistic("keysPressed", lambda keysPressed, textWritten: len(textWritten))

def average_word_length(textWritten):
    words = words_only.findall(textWritten)
    lengths = [len(word) for word in words]
    return np.mean(lengths)

wordLength_stat = Statistic("wordLength_stat",\
                            lambda keysPressed, textWritten:\
                            mean([len(word) for word in textWritten.replace("\n", " ").split(" ")]))

all_stats = [textWritten_stat, keysPressed_stat, symbolCount_stat, wordLength_stat]
