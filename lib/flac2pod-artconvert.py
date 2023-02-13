#!/usr/bin/env python3

from argparse import ArgumentParser
from flac2pod import scan_source
from mutagen import mp4
from mutagen.mp4 import MP4Cover
from os import listdir
from PIL import Image

if __name__ == "__main__":
    parser = ArgumentParser(description='Convert embedded album art in MP4/M4A files to iPod-compatible JPEGs.')
    parser.add_argument('source_dir', nargs='+',
                        help='directory tree containing music files - folder must contain library sorted into artists '
                             'and albums')
    args = parser.parse_args()

    if args.source_dir[0].endswith('/'):
        source = args.source_dir[0][:-1]
    else:
        source = args.source_dir[0]

    source_directories = scan_source(source)

    for album in sorted(source_directories[0]):
        for song in listdir(album):
            audio = mp4.MP4(f"{album}/{song}")
            if audio.tags is None:
                continue
            if "covr" not in audio.tags:
                continue
            cover = audio.tags["covr"][0]
            open("/tmp/cover.png", "wb").write(cover)
            image = Image.open("/tmp/cover.png")
            image.thumbnail((300, 300))
            image.save("/tmp/cover.jpeg", "JPEG", quality=50)
            with open("/tmp/cover.jpeg", "rb") as f:
                audio["covr"] = [
                    MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
                ]
            audio.save()
