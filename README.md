# flac2pod
Seamlessly converts your existing FLAC library to be played on an iPod Classic.

This script makes use of ffmpeg to convert your existing FLAC music library to MP3-320 for easy iPod Classic use. It also takes advantage of "rg2sc" (https://github.com/rwinkhart/rg2sc) to convert any existing ReplayGain tags to Apple Sound Check tags that are compatible with Apple products.

# Usage
Simply run:
```
flac2pod
```
...and you will be prompted for your source and destination directories.

In order for flac2pod to function, your library must be structured as follows:

library parent dir -> artist dir -> album dir -> FLAC files

When prompted for the source directory, you want to input your library parent directory.

# Installation

flac2pod is available in the AUR as "flac2pod". If installing on a non-Arch-based distribution, follow the manual installation instructions:

- copy the flac2pod executable from https://github.com/rwinkhart/flac2pod/blob/master/bin/flac2pod to your /usr/bin/
- copy the rg2sc executable from https://github.com/rwinkhart/rg2sc/blob/master/bin/rg2sc to your /usr/bin
- install python-mutagen, ffmpeg, and lame
