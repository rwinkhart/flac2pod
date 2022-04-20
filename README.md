# flac2pod
Converts your existing FLAC library to be played on an iPod Classic.

This script makes use of ffmpeg to convert your existing FLAC music library to AAC-256 for easy iPod Classic use. It can also bake your existing ReplayGain data into the output files.
SoundCheck support was removed due to this feature being very finicky on iPods. If you would like to add SoundCheck data to your output files, omit the --bake option and then use https://github.com/rwinkhart/rg2sc on your output files.

# Usage
Simply run...
```
flac2pod <source_dir> <destination_dir>
```
...to convert your library, or run...
```
flac2pod --help
```
...to see additional options.

In order for flac2pod to function, your source_dir must be structured as follows:

source_dir -> artist dir -> album dir -> FLAC files

# Installation

flac2pod is available in the AUR as "flac2pod". If installing on a non-Arch-based distribution, follow the manual installation instructions:

- copy the flac2pod executable from https://github.com/rwinkhart/flac2pod/blob/master/bin/flac2pod to your /usr/bin/
- install python-mutagen, ffmpeg, and screen
- start converting
