import pytest
import os.path
from src.selfTracking import Recorder
import time
import win32gui

def test_output(monkeypatch):

    # during testing, we don't want to really record any data (especially since this only works on Windows)
    monkeypatch.setattr("Recorder.GetWindowText", lambda *args: "mock window - aaa.txt")
    monkeypatch.setattr("Recorder.GetForegroundWindow", lambda: None)

    rec = Recorder.Recorder()
    rec.record(maxTime=3, verbose=False)

    # the expected filename of the log
    file = str(list(time.localtime())[:-6])[1:-1].replace(", ", "-") + ".txt"

    # first, check whether the log even exists
    assert os.path.exists(file)

    # if id does, check if the number of columns matches the expected value
    with open(file, "r", encoding="utf-8") as f:
        assert len(f.readline().split(";")) == 13

