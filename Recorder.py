import time
import keyboard
import mouse
from win32gui import GetWindowText, GetForegroundWindow
import os


def clear_output(wait=True):
    if wait:
        time.sleep(0.05)
    os.system('cls' if os.name == 'nt' else 'clear')


# recording will be done in 'blocks' of time.
# A switch to a different window or to an inactive/active state will trigger a new block.
# Also, there is an upper limit of block time.
class Recorder:

    def __init__(self, maxBlockTime=2 * 60, timeInactive=2 * 60, saveDir="."):

        # Parameters (settings)
        self.maxBlockTime = maxBlockTime
        self.timeBeforeInactive = timeInactive
        self.saveDir = saveDir

        self.startingTimeOfRecording = time.time()

        # block data
        self.lastBlockTrigger = time.time()
        self.handler = False  # Handler from keyboard package. False indicates no active handler.
        self.lastWindow = GetWindowText(GetForegroundWindow())
        self.handle = False  # Handle from keyboard package - the object returned by handler.
        self.keys_pressed = ""
        self.text_written = ""
        self.lastDateTime = ""

        # activity data
        self.active = True
        self.lastMouseMovement = time.time()
        self.lastMousePosition = mouse.get_position()
        self.lastKeyboardStroke = time.time()
        self.lastTextLength = 0

        self.hideText = False

    def record(self, maxTime=7 * 24 * 60 * 60):
        self.startingTimeOfRecording = time.time()
        self.createBlock()
        while time.time() - self.startingTimeOfRecording < maxTime:

            if keyboard.is_pressed("shift") and keyboard.is_pressed("esc"):
                self.endBlock()
                print("exit")
                break

            self.updateActivity()

            if self.checkBlockTrigger():
                self.triggerNewBlock()

        time.sleep(0.02)

    def checkActive(self):
        now = time.time()
        return self.timeBeforeInactive < now - self.lastKeyboardStroke or \
               self.timeBeforeInactive < now - self.lastMouseMovement

    def checkBlockTrigger(self):
        return self.lastWindow != GetWindowText(GetForegroundWindow()) \
               or time.time() - self.lastBlockTrigger > self.maxBlockTime \
               or self.active != self.checkActive()

    def startBlock(self):
        self.handler = keyboard.start_recording()
        self.lastBlockTrigger = time.time()
        self.lastWindow = GetWindowText(GetForegroundWindow())
        self.lastDateTime = str(list(time.localtime())[:-2])[1:-1].replace(", ", ";")

    def endBlock(self):
        handle = keyboard.stop_recording()
        self.keys_pressed = self.keysPressed(handle)
        self.text_written = self.textWritten(handle)
        self.outPut()

    def triggerNewBlock(self):
        self.endBlock()
        self.startBlock()

    def outPut(self):
        report = self.generateReport()
        with open(self.saveDir + "\\" + str(self.lastDateTime) + ".txt", "a", encoding="utf-8") as file:
            file.write(report)

    def generateReport(self):
        report = ""  # "year;month;day;hour;min;sec;weekday;secStart;secSpent;active;Window;textWritten\n"
        report += self.lastDateTime + ";" + \
                  str(self.lastBlockTrigger) + ";" + \
                  str(time.time() - self.lastBlockTrigger) + ";" + \
                  str(self.active) + ";" + \
                  self.lastWindow + ";" + \
                  self.text_written + ";" + \
                  self.keys_pressed + "\n"

    def keysPressed(self, handle):
        keys_pressed = ""
        for event in handle:
            if event.event_type == "down":
                if event.name != ";":
                    keys_pressed = keys_pressed + str(event.name)
                else:
                    keys_pressed = keys_pressed + "[<semicolon>]"
        return keys_pressed

    def textWritten(self, handle):
        text_written = ""
        for event in handle:
            if len(event.name) == 1 and event.event_type == "down":
                if event.name != ";":
                    text_written = text_written + str(event.name)
            elif event.name == "space" and event.event_type == "down":
                text_written = text_written + " "
            elif event.name == "backspace" and event.event_type == "down":
                text_written = text_written[:-1]  # + " [bckspc] "
        return text_written

    def updateActivity(self):
        if self.lastMousePosition != mouse.get_position():
            self.lastMouseMovement = time.time()
            self.lastMousePosition = mouse.get_position()
        if self.handler:
            if self.lastTextLength != self.handler[0].qsize():
                self.lastKeyboardStroke = time.time()
                self.lastTextLength = self.handler[0].qsize()

    def setParameters(self):
        pass

    def getParameters(self):
        pass

    def displaySettings(self):
        settingString = "|| settings    ||\n"
        settingString += f"|| refreshrate  : {self.maxBlockTime}\n"
        settingString += f"|| saveRate     : {1}\n"
        settingString += f"|| timeInactive : {self.timeBeforeInactive}\n"
        settingString += f"|| saveDir      : {self.saveDir}"

        clear_output(wait=True)
        timetime = time.time()
        print(settingString)
        print("Seconds from last keyboard stroke: " + str(round(timetime - self.lastKeyboardStroke)))
        print("Seconds from last mouse movement: " + str(round(timetime - self.lastMouseMovement)))
        print("active: " + str(self.active))
        print("last report: " + str(round(timetime - self.lastBlockTrigger)))


if __name__ == "__main__":
    rec = Recorder()
    rec.record(maxTime=40)
