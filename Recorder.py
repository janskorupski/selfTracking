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
        self.max_block_time = maxBlockTime
        self.time_before_inactive = timeInactive
        self.save_directory = saveDir

        self.starting_time_of_recording = time.time()

        # block data
        self.last_block_trigger = time.time()
        self.handler = False  # Handler from keyboard package. False indicates no active handler.
        self.last_window = GetWindowText(GetForegroundWindow())
        self.handle = False  # Handle from keyboard package - the object returned by handler.
        self.keys_pressed = ""
        self.text_written = ""
        self.last_date_time = ""

        # activity data
        self.last_active_state = True
        self.last_mouse_movement = time.time()
        self.last_mouse_position = mouse.get_position()
        self.last_keyboard_stroke = time.time()
        self.last_text_length = 0

        self.hideText = False

    def record(self, maxTime=7 * 24 * 60 * 60):
        self.starting_time_of_recording = time.time()
        self.start_block()
        while time.time() - self.starting_time_of_recording < maxTime:

            if keyboard.is_pressed("shift") and keyboard.is_pressed("esc"):
                self.end_block()
                print("exit")
                break

            self.update_activity()

            if self.check_block_trigger():
                self.trigger_new_block()

        time.sleep(0.02)

    def check_active(self):
        now = time.time()
        return self.time_before_inactive < now - self.last_keyboard_stroke or \
               self.time_before_inactive < now - self.last_mouse_movement

    def check_block_trigger(self):
        if self.last_window != GetWindowText(GetForegroundWindow()) \
                or time.time() - self.last_block_trigger > self.max_block_time \
                or self.last_active_state != self.check_active():
            self.last_active_state = self.check_active()
            return True

    def start_block(self):
        self.handler = keyboard.start_recording()
        self.last_block_trigger = time.time()
        self.last_window = GetWindowText(GetForegroundWindow())
        self.last_date_time = str(list(time.localtime())[:-6])[1:-1].replace(", ", ";")

    def end_block(self):
        handle = keyboard.stop_recording()
        self.keys_pressed = self.extract_keys_pressed(handle)
        self.text_written = self.extract_text_written(handle)
        self.output()

    def trigger_new_block(self):
        self.end_block()
        self.start_block()

    def output(self):
        report = self.generate_report()
        with open(self.save_directory + "\\" + str(self.last_date_time) + ".txt", "a", encoding="utf-8") as file:
            file.write(report)

    def generate_report(self):
        report = ""  # "year;month;day;hour;min;sec;weekday;secStart;secSpent;active;Window;textWritten\n"
        report += self.last_date_time + ";" + \
                  str(self.last_block_trigger) + ";" + \
                  str(time.time() - self.last_block_trigger) + ";" + \
                  str(self.last_active_state) + ";" + \
                  self.last_window + ";" + \
                  self.text_written + ";" + \
                  self.keys_pressed + "\n"
        return report

    def extract_keys_pressed(self, handle):
        keys_pressed = ""
        for event in handle:
            if event.event_type == "down":
                if event.name != ";":
                    keys_pressed = keys_pressed + str(event.name)
                else:
                    keys_pressed = keys_pressed + "[<semicolon>]"
        return keys_pressed

    def extract_text_written(self, handle):
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

    def update_activity(self):
        if self.last_mouse_position != mouse.get_position():
            self.last_mouse_movement = time.time()
            self.last_mouse_position = mouse.get_position()
        if self.handler:
            if self.last_text_length != self.handler[0].qsize():
                self.last_keyboard_stroke = time.time()
                self.last_text_length = self.handler[0].qsize()

    def set_parameters(self):
        pass

    def get_parameters(self):
        pass

    def display_settings(self):
        settingString = "|| settings    ||\n"
        settingString += f"|| refreshrate  : {self.max_block_time}\n"
        settingString += f"|| saveRate     : {1}\n"
        settingString += f"|| timeInactive : {self.time_before_inactive}\n"
        settingString += f"|| saveDir      : {self.save_directory}"

        clear_output(wait=True)
        timetime = time.time()
        print(settingString)
        print("Seconds from last keyboard stroke: " + str(round(timetime - self.last_keyboard_stroke)))
        print("Seconds from last mouse movement: " + str(round(timetime - self.last_mouse_movement)))
        print("active: " + str(self.last_active_state))
        print("last report: " + str(round(timetime - self.last_block_trigger)))


if __name__ == "__main__":
    rec = Recorder()
    rec.record(maxTime=30)
