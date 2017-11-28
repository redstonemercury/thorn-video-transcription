#!/usr/bin/env python3

# TODO: yeah... all of this

from lib.our_converter import Converter


def main():
    c = Converter()
    mp3_file = c.get_audio()
    c.chunk_audio(mp3_file)


def handler(event, context):
    convert_video_to_audio(ffmpeg.input(event['video_file']))


if __name__ == "__main__":
    main()
