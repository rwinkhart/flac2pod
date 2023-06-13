#!/bin/sh
git add -f LICENSE README.md commit.sh package.sh share lib/flac2pod-artconvert.py lib/flac2pod-flacgain.py lib/flac2pod.py
git commit -m "$1"
git push
