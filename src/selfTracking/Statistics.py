class Statistic:

    def __init__(self, name, calc_func):
        self.name = name
        self.calculate = calc_func


textWritten_stat = Statistic("textWritten", lambda keysPressed, textWritten: textWritten)
keysPressed_stat = Statistic("keysPressed", lambda keysPressed, textWritten: keysPressed)

