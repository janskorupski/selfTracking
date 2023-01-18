import os.path

import Recorder
import time
import win32gui
import pytest

def test_output(monkeypatch):

    def mock_window(*args):
        return "mock window - aaa.txt"

    monkeypatch.setattr("Recorder.GetWindowText", mock_window )
    monkeypatch.setattr("Recorder.GetForegroundWindow", lambda: None)

    rec = Recorder.Recorder()
    rec.record(maxTime=3, verbose=False)

    file = str(list(time.localtime())[:-6])[1:-1].replace(", ", "-") + ".txt"

    assert file.split(".")[1] == "txt"
    listed = file[:-4].split("-")
    assert len(listed) == 3
    assert not any([not el.isnumeric for el in listed])

    assert os.path.exists(file)

    with open(file, "r", encoding="utf-8") as f:
        assert len(f.readline().split(";")) == 13

