# flac2pod
Seamlessly converts your existing FLAC library to be played on an iPod Classic.

This script makes use of ffmpeg to convert your existing FLAC music library to either MP3-320 or ALAC for easy iPod Classic use. It also takes advantage of "rg2sc" (https://github.com/rwinkhart/rg2sc) to convert any existing ReplayGain tags to Apple Sound Check tags that are compatible with Apple products.

# Usage

```
flac2pod -f --mp3  # will convert library to MP3-320 and forcefully update Sound Check tags (even if they already exist)

flac2pod --alac  # will convert library to ALAC in a .m4a container - only updates missing Sound Check tags

flac2pod  # will convert library to MP3-320 - only updates missing Sound Check tags
```

In order for flac2pod to function, your library must be structured as follows:
Library dir -> Artist dir -> Album dir -> FLAC files

When prompted for the source directory, you want to input your library parent directory.

# Installation

flac2pod is available in the AUR as "flac2pod". If installing on a non-Arch-based distribution, follow the manual installation instructions:

- copy the flac2pod executable from https://github.com/rwinkhart/flac2pod/blob/master/bin/flac2pod to your /usr/bin/
- copy the rg2sc executable from https://github.com/rwinkhart/rg2sc/blob/master/bin/rg2sc to your /usr/bin
- install python-mutagen, ffmpeg, and lame
