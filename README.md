# Self-tracking

A short python package for self-tracking - measuring productivity, app-usage and general computer usage. The main idea is to strive for high temporal resolution (unlike most other existing apps) as well as minimal human intervention (so that you can forget it's even running in the background).

## Why 

Devising a multitude of cognitive and psychological assesments, trying to learn about ourselfs through deep conversations with friends and family, questionnaires and sometimes even pseudo-scientific facebook posts, we have forgotten that there is a continous stream of precise information about our behaviour literally being wasted as you read this. Unfortunately, most apps and programmes that track our activity on our computers only provide general statistics such as '% of app usage' or 'time spent on windows', while completely discarding the most important information.
The aim of this package is to extract as much information from our computer activity as possible, with the potential of using this information to improve productivity, uncovering maladaptive behaviour patterns in the day-to-day computer usage or perhaps even learning the relations between our health, emotions, strategies and the enviornmental data.

## Usage

### Seamless data recording

#### Windows
Assuming you have python installed
1. Find the 'Autostart folder' (usually located at C:\Users\<User>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup).
2. Create a new text file and change the extention to ".bat".
3. write 'python ' and paste the location of the "Recorder.py".
For conda or other enviornments users, you have to first add a line enabling the enviornment containing python (eg. "call conda activate <env name>")

## Future plans

- add a measure of productivity
- add a simple data visualisation module
- add a task distinction mechanism
- add differing measures of productivity for different tasks

potentially in the far future:
- opt-in: disable procrascination
- opt-in: track changes in files being edited
- opt-in: enforce task declaration before beggining a task
- opt-in: integrate and enforce questionnaire-based tracking methods (experience sampling, mood tracking)
- compatibility with other data (geolocation, )
- eyetracker compatibility



