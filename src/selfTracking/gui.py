import tkinter as tk
import customtkinter as ctk
import Statistics
import os
import configparser

settingsPath = "./settings.ini"
config = configparser.ConfigParser()
config['active'] = {
    "Record": "False",
    "isRecording": "False"
}
config['settings'] = {
            "maxTime": str(4 * 7 * 24 * 60 * 60),
            "maxBlockTime": str(2 * 60),
            "timeInactive": str(2 * 60),
            "saveDir": ".",
            "Record": "False",
            "python" : "False"
}
config['statistics'] = {}
for stat in Statistics.all_stats:
    config['statistics'][stat.name] = str(stat.is_safe)

header = "year;month;day;hour;min;sec;weekday;secStart;secSpent;active;Window"
for stat in Statistics.all_stats:
    header += ";" + stat.name
hardCodedExample = [header,
                    "2024;3;2;2;58;45;5;1709344725.1013916;120.11262965202332;True;*Bez tytułu — Notatnik;Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.;right shiftLoremspaceipsumspacedolorspacesitspaceamet,spaceconsecteturspaceadipiscingspaceelitspacebackspace,spacesedspacefospacebackspacebackspacebackspacedospaceeiusmodspacetempotbackspacerspaceincididuntspaceutspacelaborespaceetspacedolorespacemagnaspacealiqua.spaceright shiftUtspaceenimspaceadspaceminimspaceveniam,spacequisspacenostrudspaceexercitationspaceullamcospacelaborisspacenisispaceuspacetalibackspacebackspacebackspacebackspacebackspacetspacealiquipspaceexspaceeaspacecommodospaceconsequatspacebackspace.;231;5.444444444444445",
                    "2024;3;2;3;0;45;5;1709344845.2226956;6.349174737930298;True;Strona logowania | iPKO - bankowość elektroniczna PKO Banku Polskiego - Google Chrome;loginloginhahaslohaslo;loginloginenterhabackspacectrlahaslohaslo;22;22"]
hardCodedExample = [row.split(";") for row in hardCodedExample]


def save_settings():
    with open(settingsPath, 'w') as file:
        config.write(file)


def read_settings(settingsPath=settingsPath):
    config.read(settingsPath)


if os.path.exists(settingsPath):
    read_settings()
else:
    save_settings()

window = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

sidePanelRight = ctk.CTkFrame(master=window)
sidePanelRight.grid(row=1, column=2)

# The middle panel
table = ctk.CTkFrame(master=window)


def update_table():
    for child in table.winfo_children():
        child.destroy()
    table.grid(row=1, column=1)
    table.rowconfigure(1, minsize=40)
    table.columnconfigure(1, minsize=40)
    for i, row in enumerate(hardCodedExample):
        for j, value in enumerate(row):
            if hardCodedExample[0][j] in config["statistics"].keys():
                if not config.getboolean("statistics", hardCodedExample[0][j]):
                    continue
            cellFrame = ctk.CTkFrame(master=table)
            cellFrame.grid(row=i, column=j, padx=5, pady=5)
            if len(value) > 50:
                value = value[:47] + "..."
            cell = ctk.CTkLabel(text=value, master=cellFrame, wraplength=100)
            cell.pack()
    return table


update_table()

# Right side panel
recordButtonFrame = ctk.CTkFrame(master=sidePanelRight)
recordButtonFrame.grid(row=1, column=2)
recordButton = ctk.CTkButton(text="Record", master=recordButtonFrame)
if config.getboolean("active", "Record") == 1:
    recordButton.configure(text="Stop recording")
recordButton.pack()


def on_record_click(event):
    if not config.getboolean("active", "Record"):
        recordButton.configure(text="Stop recording")
        config["active"]["Record"] = "True"
        save_settings()
        # to do
        # subProcessRunRecorder() # to implement!
    else:
        recordButton.configure(text="Record")
        config["active"]["Record"] = "False"
        save_settings()


recordButton.bind("<Button-1>", on_record_click)

checkBoxTextFrame = ctk.CTkFrame(master=sidePanelRight)
checkBoxTextFrame.grid(row=2, column=2)
checkBoxText = ctk.CTkLabel(text="Recorded data:", master=checkBoxTextFrame)
checkBoxText.pack()


def on_checkbox_toggle():
    for i, stat in enumerate(Statistics.all_stats):
        config['statistics'][stat.name] = str(stat_checkBoxVars[i].get())
    save_settings()
    update_table()


stat_checkBoxes = []
stat_checkBoxVars = []
frame = ctk.CTkFrame(master=sidePanelRight)
frame.grid(row=3, column=2)
for i, stat in enumerate(Statistics.all_stats):
    var = ctk.BooleanVar(name=stat.name)
    var.set(config.getboolean("statistics", stat.name))
    stat_checkBoxVars.append(var)
    cb = ctk.CTkCheckBox(text=stat.name, master=frame, variable=var, command=on_checkbox_toggle)
    cb.grid(row=i + 1, column=1, sticky='w')
    stat_checkBoxes.append(cb)

window.mainloop()
