# Self-tracking

A short python package for self-tracking - measuring productivity, app-usage and general computer usage. The main idea is to strive for high temporal resolution (unlike most other existing apps) as well as minimal human intervention (so that you can forget it's even running in the background).

## Why 

Devising a multitude of cognitive and psychological assessments, trying to learn about ourselves through deep conversations with friends and family, questionnaires and sometimes even pseudo-scientific Facebook posts, we have forgotten that there is a continuous stream of precise information about our behaviour literally being wasted as you read this. Unfortunately, most apps and programmes that track our activity on our computers only provide general statistics such as '% of app usage' or 'time spent on windows', while completely discarding the most important information.
The aim of this package is to extract as much information from our computer activity as possible, with the potential of using this information to improve productivity, uncovering maladaptive behaviour patterns in the day-to-day computer usage or perhaps even learning the relations between our health, emotions, strategies and the environmental data.

## How
### Recording format
The 'Recorder.record()' method records the activity of the user in blocks of time. For each block, its starting time, end time, name of the active window and, to some extent, details of activity are stored as a row in a '.csv' file. User is deemed as not-active if he has not moved his mouse or clicked any key in a given time (by default 2 minutes). The time of each block has an upper limit, after which a new block will be triggered. The actions which trigger a new block include:
- changing of the active window
- reaching the maximal block time
- changing the activity status (active->not-active or not-active->active)

Each time one of these actions triggers a 'new block' event the recording is terminated, the recorded data added as a new line in the .csv file and a new recording is started. The saved data files are split by days and so the data directory will contain a separate '.csv' file for each day of the recording.

### Analysis

Any methods used by the 'Analyzer' class require loading the raw data first, using the 'load_raw_data' method. This loads all the data files created by the 'Recorder.record()' method in a given data directory.

#### Flagging
Each window name can be given a 'flag' (e.g. 'work', 'break', 'writing'). This is partially automated by the 'update_flag_file' method in two ways:
- a file 'flag_rules.csv' can be modified by the user to specify keywords and their associated flags. Each window name which contains a given keyword will then be automatically assigned the associated flag. In case of multiple keywords only the first one is considered (by the order of lines in the .csv file).
- a file 'hand_flagged_windows.csv' will be automatically generated with all the window names that exist in the data directory and do not contain any keywords from the 'flag_rules.csv' file. This file can be modified by the user to manually assign flags to each window. In case of a conflict, the manually assigned flags have a priority over the rule-generated flags.

The method will also create the 'flag_data.csv' file, which contains all the window names existing in the data with the final flags assigned. This file will be used in further analysis by the 'make_time_series' method (details in the next section). It can be edited manually, but it is not advised, as changes will be overwritten by the 'update_flag_file' method the next time it will be used.

**Please note, that for practical purposes the separator in the ".csv" files mentioned above cannot be '.' or ';'. By default '¤' (chr(164)) is used, as it cannot be written with a standard keyboard.**

#### Time series preprocessing
The 'make_time_series' method morphs the raw data (the result of 'Recorder.record' method) into a time-series data with a specified statistic. It requires a 'statistic' argument, eg.:
```{python}
analyzer.make_time_series(lambda x: len(row.textWritten)/row.secSpent ) 
```
and creates a pandas DataFrame indexed by minutes, with the calculated statistic for each minute (by default, sampling frequency can be specified). For minutes which encompass multiple blocks, the statistic is the mean value of the statistic for each included block, weighted proportionally to the time portions. This DataFrame can be used for further data analysis.

## Usage

### Seamless data recording

#### Windows
1. Find the 'Autostart folder' (usually located at C:\Users\<User>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup).
2. Create a new text file and change the extension to ".bat".
3. write 'python ' and paste the location of the "Recorder.py".
For conda or other environments users, you have to first add a line enabling the environment containing python (e.g. "call conda activate <env name>")

#### Linux
Currently the package does not support other operating systems than windows (it utilises 'win32gui' for data recording). This package was created for my personal use and I have not yet made the full transition to the only sensible operating system. I will add this feature if I ever find the time. 

#### IOS 
... no.

## Future plans

- add a more sensible measure of productivity
- add a simple data visualisation module
- add a task distinction mechanism
- add differing measures of productivity for different tasks (This can be done manually now with the usage of flags, but requires much work)

potentially in the far future:
- opt-in: disable procrastination
- opt-in: track changes in files being edited
- opt-in: enforce task declaration before beginning a task
- opt-in: integrate and enforce questionnaire-based tracking methods (experience sampling, mood tracking)
- compatibility with other data (geolocation, experience sampling)
- eye tracker compatibility
