#!/usr/bin/env python3

from argparse import ArgumentParser
from flac2pod import scan_source
from mutagen.flac import FLAC, FLACNoHeaderError
from os import listdir, system
from subprocess import PIPE, run
from sys import exit as s_exit

# argument parsing
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
        std_album = album.replace(' ', '\\ ').replace("'", "\\'").replace(')', '\\)').replace('(', '\\(')\
            .replace(']', '\\]').replace('[', '\\[').replace('&', '\\&').replace('`', '\\`').replace('$', '\\$')
        for song in listdir(album):
            try:
                audio = FLAC(f"{album}/{song}")
                if audio.get('replaygain_track_gain') or audio.get('REPLAYGAIN_TRACK_GAIN'):
                    gain = 1
                else:
                    gain = 0
                    break
            except FLACNoHeaderError:
                print(f"[{album}/*] Contains non-FLAC files, skipping album...")
                gain = 2
        if gain != 2 and (args.force or gain == 0):
            print(f"[{album}/*] Adding ReplayGain data...")
            system(f"metaflac --remove-replay-gain {std_album}/*")
            output = run(f"metaflac --add-replay-gain {std_album}/*", shell=True, stdout=PIPE, text=True)
            if output.returncode == 1:
                if output.stdout.__contains__('sample') or output.stdout.__contains__('resolution of'):
                    print('Resolution/Sample Rate mismatch, scanning tracks as individuals...')
                    for song in listdir(album):
                        print(f"[{album}/{song}] Adding ReplayGain data...")
                        std_song = song.replace(' ', '\\ ').replace("'", "\\'").replace(')', '\\)')\
                            .replace('(', '\\(').replace('&', '\\&').replace('`', '\\`').replace('$', '\\$')
                        output = run(f"metaflac --add-replay-gain {std_album}/{std_song}", shell=True, stdout=PIPE,
                                     text=True)
                        if output.returncode == 1:
                            print('There was an error processing your files.')
                            print(f"Return Code: [{str(output.returncode)}] {output.stdout}")
                            s_exit(1)
                else:
                    print('There was an error processing your files.')
                    print(f"Return Code: [{str(output.returncode)}] {output.stdout}")
                    s_exit(1)

        else:
            print(f"[{album}/*] ReplayGain data is already present.")

    s_exit(0)
