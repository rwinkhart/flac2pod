#!/usr/bin/env python3

from argparse import ArgumentParser
from mutagen.flac import FLAC
from os import cpu_count, getuid, listdir, path, stat, walk
from pathlib import Path
from shutil import copy
from subprocess import DEVNULL, Popen
from sys import exit as s_exit
from time import sleep


# scans source directory for music files, returns lists of album directories and their full paths
def scan_source(_source):
    _artist_dirs, _album_dirs, _full_paths = [], [], []
    for _root, _directories, _files in walk(path.expanduser(_source)):
        for _dir in sorted(_directories):
            if not _root.endswith(path.expanduser(_source)):
                _artist_dirs.append(_root)
    _artist_dirs = list(set(_artist_dirs))
    for _artist in sorted(_artist_dirs):
        for _root, _directories, _files in walk(path.expanduser(_artist)):
            if not _root.endswith(path.expanduser(_artist)):
                _album_dirs.append(_root)
    _album_dirs = list(set(_album_dirs))
    for _album in sorted(_album_dirs):
        for _root, _directories, _files in walk(path.expanduser(_album)):
            for _filename in _files:
                if _filename.lower().endswith('.flac') or _filename.lower().endswith('.mp3') or \
                        _filename.lower().endswith('.mp4') or _filename.lower().endswith('.m4a'):
                    _full_paths.append(f"{_album}/{_filename}")
    return _album_dirs, _full_paths


# creates destination directory structure
def create_destination():
    for _dir in source_directories[0]:
        Path(path.expanduser(_dir.replace(path.expanduser(source), path.expanduser(destination))))\
            .mkdir(0o700, parents=True, exist_ok=True)


# counts how many ffmpeg processes are running under the current user
def count_user_ffmpeg_processes():
    _user = getuid()
    _proc_directory = '/proc'
    _running_processes = 0
    _subdirectories = [_d for _d in listdir(_proc_directory) if path.isdir(path.join(_proc_directory, _d))]
    for _subdirectory in _subdirectories:
        if _subdirectory.isnumeric():
            if stat(_proc_directory + '/' + _subdirectory).st_uid == _user:
                with open(_proc_directory + '/' + _subdirectory + '/cmdline', 'r') as _f:
                    if _f.read().startswith('ffmpeg'):
                        _running_processes += 1
    return _running_processes


def scan_destination_convert():
    _i, _i_total, _total_files = 0, 0, len(source_directories[1])
    for _file in source_directories[1]:
        _i_total += 1
        _progress = round((_i_total / _total_files) * 100, 2)
        if not Path(f"{(_file.replace(path.expanduser(source), path.expanduser(destination)))[:-5]}.m4a").is_file()\
                and not Path(f"{(_file.replace(path.expanduser(source), path.expanduser(destination)))}").is_file():
            if not _file.lower().endswith('.flac'):
                print(f"[{_file}] Not a FLAC file, copying...")
                copy(f"{_file}", f"{_file.replace(path.expanduser(source), path.expanduser(destination))}")
            else:
                _file_d = _file.replace(path.expanduser(source), path.expanduser(destination))[:-5] + '.m4a'
                _active_processes = count_user_ffmpeg_processes()
                while _active_processes >= cpu_count():
                    print(f"\nThere are already {_active_processes} processes running on your {cpu_count()} "
                          f"threads...\n")
                    sleep(1)
                    _active_processes = count_user_ffmpeg_processes()
                _i += 1
                print(f"\n{_progress}% | \u001b[38;5;0;48;5;15mConverting {_file} to {_file_d}...\u001b[0m\n")
                # get relevant ReplayGain info
                _audio = FLAC(f"{_file}")
                if args.albumgain:
                    if _audio.get('REPLAYGAIN_ALBUM_GAIN'):
                        _rggain = float(_audio.get('REPLAYGAIN_ALBUM_GAIN')[0][:-3])
                    elif _audio.get('replaygain_album_gain'):
                        _rggain = float(_audio.get('replaygain_album_gain')[0][:-3])
                    else:
                        _rggain = None
                    if _audio.get('REPLAYGAIN_ALBUM_PEAK'):
                        _rgpeak = float(_audio.get('REPLAYGAIN_ALBUM_PEAK')[0])
                    elif _audio.get('replaygain_album_peak'):
                        _rgpeak = float(_audio.get('replaygain_album_peak')[0])
                    else:
                        _rgpeak = None
                else:
                    if _audio.get('REPLAYGAIN_TRACK_GAIN'):
                        _rggain = float(_audio.get('REPLAYGAIN_TRACK_GAIN')[0][:-3])
                    elif _audio.get('replaygain_track_gain'):
                        _rggain = float(_audio.get('replaygain_track_gain')[0][:-3])
                    else:
                        _rggain = None
                    if _audio.get('REPLAYGAIN_TRACK_PEAK'):
                        _rgpeak = float(_audio.get('REPLAYGAIN_TRACK_PEAK')[0])
                    elif _audio.get('replaygain_track_peak'):
                        _rgpeak = float(_audio.get('replaygain_track_peak')[0])
                    else:
                        _rgpeak = None
                # determine ffmpeg arguments
                if args.bake and _rggain is not None:
                    _bake_args, _flac2pod_rg_tags = ['-filter:a', 'volume=' + str(_rggain) + 'dB'], []
                elif _rggain is not None and _rgpeak is not None:
                    _bake_args, _flac2pod_rg_tags = [], ['-metadata', f"comment=FLAC2PODRG#{_rggain}#{_rgpeak}#"]
                else:
                    _bake_args, _flac2pod_rg_tags = [], []
                if args.preserve:
                    _art_args = ['-c:v', 'copy', '-map_metadata', '0:g']
                else:
                    _art_args = ['-vn']
                # generate the appropriate ffmpeg command
                _cmd = ['ffmpeg', '-i', _file] + _art_args + ['-c:a', 'aac', '-b:a', '256k'] + _bake_args +\
                    _flac2pod_rg_tags + ['-aac_pns', '0', '-movflags', '+faststart', _file_d]
                if _rggain is not None:
                    print(f"\u001b[38;5;0;48;5;15mGain adjustment: {_rggain}dB\u001b[0m")
                else:
                    print('\u001b[38;5;0;48;5;88mNo ReplayGain data found!\u001b[0m')
                    if args.stopifnogain:
                        s_exit(1)
                Popen(_cmd, stdout=DEVNULL, stderr=DEVNULL)
    _active_processes = count_user_ffmpeg_processes()
    while _active_processes != 0:
        print(f"\nPlease wait for the remaining {_active_processes} conversions to complete...\n")
        sleep(1)
        _active_processes = count_user_ffmpeg_processes()
    print('\niPod conversion complete!\n')
    s_exit(0)


# argument parsing
if __name__ == "__main__":
    parser = ArgumentParser(description='Convert your existing FLAC library to be played on an iPod Classic.')
    parser.add_argument('source_dir', nargs='+',
                        help='directory tree containing music files - folder must contain library sorted into artists '
                             'and albums')
    parser.add_argument('destination_dir', nargs='+',
                        help='destination parent directory for output - will be created if it does not already exist')
    parser.add_argument('-b', '--bake', action='store_true',
                        help='bake (encode) ReplayGain values into output files')
    parser.add_argument('-a', '--albumgain', action='store_true',
                        help='read ReplayGain album gain instead of ReplayGain track gain')
    parser.add_argument('-x', '--stopifnogain', action='store_true',
                        help='stop flac2pod if ReplayGain data cannot be found in a file')
    parser.add_argument('-p', '--preserve', action='store_true',
                        help='copy album art from input files')
    args = parser.parse_args()

    if args.source_dir[0].endswith('/'):
        source = args.source_dir[0][:-1]
    else:
        source = args.source_dir[0]
    if args.destination_dir[0].endswith('/'):
        destination = args.destination_dir[0][:-1]
    else:
        destination = args.destination_dir[0]

    source_directories = scan_source(source)
    create_destination()
    scan_destination_convert()
