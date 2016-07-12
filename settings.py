from os import path

##
## FILES
##

EXTENSIONS = ["mp3", "wav", "mid", "mp4"]

##
## PITCH
## 
PITCH_START = 1
PITCH_MIN = 0.85
PITCH_MAX = 1.15

PITCH_CHANGE_CHANCE = 0.1 # per second
PITCH_CHANGE_SPEED = 0.005 # per second

##
## GLITCH
##

GLITCH_DURATION = 0.25
GLITCH_CHANCE = 0.1

##
## EVENTS
##

MIN_WAIT_AFTER_EVENT = 10

###
### FFMPEG
###

FFMPEG_BIN = path.join(".", "ffmpeg", "bin", "ffmpeg.exe")
MPG123_DLL = path.join(".", "mpg123-1.23.4-x86-64", "libmpg123-0.dll")

##
## EXPERIMENTAL
##

##
## SEEK at Runtime
##

DO_SEEK = False
SEEK_TO = 0