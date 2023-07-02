#!/usr/bin/env python3

from argparse import ArgumentParser
from flac2pod import scan_source
from glob import glob
from mutagen.flac import FLAC, FLACNoHeaderError
from os import listdir
from subprocess import PIPE, run
from sys import exit as s_exit

if __name__ == "__main__":
    parser = ArgumentParser(description='Quickly tag your FLAC library with ReplayGain data using metaflac.')
    parser.add_argument('source_dir', nargs='+',
                        help='directory tree containing music files - folder must contain library sorted into artists '
                             'and albums')
    parser.add_argument('-f', '--force', action='store_true',
                        help='overwrite existing ReplayGain data')
    args = parser.parse_args()

    if args.source_dir[0].endswith('/'):
        source = args.source_dir[0][:-1]
    else:
        source = args.source_dir[0]

    source_directories = scan_source(source)

    gain = 1
    for album in sorted(source_directories[0]):
        for song in listdir(album):
            gain = 1  # reset for each song
            if not song.lower().endswith('.flac'):
                gain = 2  # set non-flac signal
            else:
                try:
                    audio = FLAC(f"{album}/{song}")
                    if audio.get('replaygain_track_gain') or audio.get('REPLAYGAIN_TRACK_GAIN'):
                        print(f"[{album}/*] ReplayGain data is already present.")
                        break
                    else:
                        gain = 0
                except FLACNoHeaderError:
                    gain = 2  # set non-flac signal
            if gain == 2:
                print(f"[{album}/*] Contains non-FLAC files, skipping album...")
                break
        if gain != 2 and (args.force or gain == 0):
            print(f"[{album}/*] Adding ReplayGain data...")
            album_files = glob(album + '/*')
            run(['metaflac', '--remove-replay-gain'] + album_files)
            output = run(['metaflac', '--add-replay-gain'] + album_files, stderr=PIPE, text=True)
            if output.returncode == 1:
                if output.stderr.__contains__('sample') or output.stderr.__contains__('resolution of') or output.\
                        stderr.__contains__('does not match'):
                    print('Resolution/Sample Rate/Channel mismatch, scanning tracks as individuals...')
                    for song in listdir(album):
                        print(f"[{album}/{song}] Adding ReplayGain data...")
                        output = run(('metaflac', '--add-replay-gain', f"{album}/{song}"), stderr=PIPE, text=True)
                        if output.returncode == 1:
                            print('There was an error processing your files.')
                            print(f"Return Code: [{str(output.returncode)}] {output.stderr}")
                            s_exit(1)
                else:
                    print('There was an error processing your files.')
                    print(f"Return Code: [{str(output.returncode)}] {output.stderr}")
                    s_exit(1)
