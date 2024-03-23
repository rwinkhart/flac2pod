# flac2pod

Converts your existing FLAC library to be played on an iPod Classic.

This script makes use of ffmpeg to convert your existing FLAC music library to AAC-256 for easy iPod Classic use. It can also bake your existing ReplayGain data into the output files. SoundCheck support was removed due to this feature being very finicky on iPods. If you would like to add SoundCheck data to your output files, omit the --bake option and then use https://github.com/rwinkhart/rg2sc on your output files.

In order for ReplayGain baking to work, your FLAC library must already be tagged with ReplayGain data. If you haven't already done this, flac2pod comes with a script (flac2pod-flacgain) for quickly applying these ReplayGain tags.

# WARNING

This is an older project of mine that is only updated to fix bugs and maintain compatibility. It is written rather poorly, but it does what it says on the tin, so I will not be investing time into rewriting it.

# Usage

Simply run...

```
flac2pod <source_dir> <destination_dir>
```

...to convert your library, or run...

```
flac2pod --help
```

...to see additional options, or run...

```
flac2pod-flacgain <source_dir>
```

...to tag your FLAC library with ReplayGain data, or run...

```
flac2pod-artconvert <source_dir>
```

...to convert embedded PNGs (in MP4/M4A files) to iPod-ready JPEGs.

In order for flac2pod to function, your source_dir must be structured as follows:

source_dir -> artist dir -> album dir -> FLAC files

# Installation

flac2pod is available in the AUR as "flac2pod".

If installing on a non-Arch-based distribution, a generic package is available on the releases page.
