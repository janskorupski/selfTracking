import keyboard
import time
import mouse
from win32gui import GetWindowText, GetForegroundWindow
import sys
import win32gui
import win32process
import win32api
import os


def clear_output(wait=True):
    if wait:
        time.sleep(0.05)
    os.system('cls' if os.name == 'nt' else 'clear')


maxTime = 60 * 60 * 24 * 31
refreshrate = 60 * 10
saveRate = 1
timeInactive = 60 * 2
saveDir = "C:\\Users\\PC\\Desktop\\pliki\\selfTracking"

maxTimeSynonyms = ["maxTime", "mT", "mt", "time", "max"]
refreshrateSynonyms = ["refreshrate", "rr", "refresh"]
saveRateSynonyms = ["saveRate", "sr"]
timeInactiveSynonyms = ["timeInactive", "ti", "inactive", ]
saveDirSynonyms = ["saveDir", "sd", "directory", "d", "dir"]

synonyms = [maxTimeSynonyms, refreshrateSynonyms, saveRateSynonyms, timeInactiveSynonyms, saveDirSynonyms]

if "-h" in sys.argv:
    print("Possible arguments (and their synonyms):")
    for syn in synonyms:
        print(",".join(syn))
    quit()

argDict = {}
for arg in sys.argv:
    if (len(arg.split("=")) == 2):
        argument = arg.split("=")[0].replace("-", "")
        value = arg.split("=")[1]
        if value.isnumeric():
            value = int(value)
        argDict[argument] = value
    elif ".py" not in arg:
        raise Exception(f"No argument {arg}")

for argName in argDict.keys():
    argName = argName.replace("-", "")
    if argName in maxTimeSynonyms:
        maxTime = argDict[argName]
    if argName in refreshrateSynonyms:
        refreshrate = argDict[argName]
    if argName in saveRateSynonyms:
        saveRate = argDict[argName]
    if argName in timeInactiveSynonyms:
        timeInactive = argDict[argName]
    if argName in saveDirSynonyms:
        saveDir = argDict[argName]

settingString = "|| settings    ||\n"
settingString += f"|| maxTime      : {maxTime}\n"
settingString += f"|| refreshrate  : {refreshrate}\n"
settingString += f"|| saveRate     : {saveRate}\n"
settingString += f"|| timeInactive : {timeInactive}\n"
settingString += f"|| saveDir      : {saveDir}"

print(settingString)

startTime = time.time()

report = ""  # "year;month;day;hour;min;sec;weekday;secStart;secSpent;active;Window;textWritten\n"

saveCounter = 0

lastTime = time.time()
lastWindow = GetWindowText(GetForegroundWindow())
lastDateTime = str(list(time.localtime())[:-2])[1:-1].replace(", ", ";")
textWritten = ""
keysPressed = ""
handler = keyboard.start_recording()

mousePosition = mouse.get_position()
lastMouseMovement = time.time()
lastTextLength = handler[0].qsize()
lastKeyboardStroke = time.time()

active = True
triggerNewReport = False
hideText = False

while (time.time() - startTime < maxTime):
    time.sleep(0.05)

    if (keyboard.is_pressed("shift") and keyboard.is_pressed("esc")):
        print("exit")
        break

    if (keyboard.is_pressed("ctrl") and keyboard.is_pressed("~")):
        print("pausing for 10 seconds ... ")

        words = keyboard.stop_recording()

        for word in words:
            if (len(word.name) == 1 and word.event_type == "down"):
                textWritten = textWritten + str(word.name)
            elif (word.name == "space" and word.event_type == "down"):
                textWritten = textWritten + " "
            elif (word.name == "backspace" and word.event_type == "down"):
                textWritten = textWritten + " [bckspc] "

            if (word.name != ";"):
                keysPressed = keysPressed + str(word.name)
            else:
                keysPressed = keysPressed + "[<semicolon>]"

        textWritten = textWritten + " [ .. pause in recording .. ] "
        keysPressed = keysPressed + " [ .. pause in recording .. ] "

        time.sleep(1)
        while (not (keyboard.is_pressed("ctrl") and keyboard.is_pressed("~"))):
            time.sleep(0.05)

        print("... pause stopped")

        handler = keyboard.start_recording()

    if (mousePosition != mouse.get_position()):
        lastMouseMovement = time.time()
        mousePosition = mouse.get_position()

    if (lastTextLength != handler[0].qsize() and handler[0].qsize() != 0):
        lastKeyboardStroke = time.time()  # watch out, the handler changes at each report
        lastTextLength = handler[0].qsize()

    if (active and time.time() - lastKeyboardStroke > timeInactive and time.time() - lastMouseMovement > timeInactive):
        active = False
        triggerNewReport = True

    if (not active and (
            time.time() - lastKeyboardStroke < timeInactive or time.time() - lastMouseMovement < timeInactive)):
        active = True
        triggerNewReport = True

    clear_output(wait=True)
    timetime = time.time()
    print(settingString)
    print("Seconds from last keyboard stroke: " + str(round(timetime - lastKeyboardStroke)))
    print("Seconds from last mouse movement: " + str(round(timetime - lastMouseMovement)))
    print("active: " + str(active))
    print("last report: " + str(round(timetime - lastTime)))

    if (lastWindow != GetWindowText(GetForegroundWindow()) or time.time() - lastTime > refreshrate or triggerNewReport):
        triggerNewReport = False

        words = keyboard.stop_recording()
        handler = keyboard.start_recording()

        report = report + lastDateTime + ";" + str(lastTime) + ";" + str(time.time() - lastTime) + ";" + str(
            active) + ";" + lastWindow + ";"

        lastTime = time.time()
        lastWindow = GetWindowText(GetForegroundWindow())
        lastDateTime = str(list(time.localtime())[:-2])[1:-1].replace(", ", ";")

        for word in words:
            if (len(word.name) == 1 and word.event_type == "down"):
                if (word.name != ";"):
                    textWritten = textWritten + str(word.name)
            elif (word.name == "space" and word.event_type == "down"):
                textWritten = textWritten + " "
            elif (word.name == "backspace" and word.event_type == "down"):
                textWritten = textWritten[:-1]  # + " [bckspc] "

            if (word.event_type == "down"):
                if (word.name != ";"):
                    keysPressed = keysPressed + str(word.name)
                else:
                    keysPressed = keysPressed + "[<semicolon>]"

        report = report + textWritten + ";" + keysPressed + "\n"

        textWritten = ""
        keysPressed = ""

        if (saveCounter >= saveRate):

            saveCounter = 1

            tm = time.gmtime()
            date = str(tm.tm_year) + "-" + str(tm.tm_mon) + "-" + str(tm.tm_mday)

            f = open(saveDir + "\\" + date + ".txt", "a", encoding="utf-8")
            f.write(report)
            f.close()
            report = ""
        else:
            saveCounter = saveCounter + 1

words = keyboard.stop_recording()

report = report + lastDateTime + ";" + str(lastTime) + ";" + str(time.time() - lastTime) + ";" + str(
    active) + ";" + lastWindow + ";"

for word in words:
    if (len(word.name) == 1 and word.event_type == "down"):
        if (word.name != ";"):
            textWritten = textWritten + str(word.name)
    elif (word.name == "space" and word.event_type == "down"):
        textWritten = textWritten + " "
    elif (word.name == "backspace" and word.event_type == "down"):
        textWritten = textWritten[:-1]  # + " [bckspc] "

    if (word.event_type == "down"):
        if (word.name != ";"):
            keysPressed = keysPressed + str(word.name)
        else:
            keysPressed = keysPressed + "[<semicolon>]"

report = report + textWritten + ";" + keysPressed + "\n"

tm = time.localtime()
date = str(tm.tm_year) + "-" + str(tm.tm_mon) + "-" + str(tm.tm_mday)

f = open(saveDir + "\\" + date + ".txt", "a", encoding="utf-8")
f.write(report)
f.close()
report = ""