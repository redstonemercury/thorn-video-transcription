#!/usr/bin/env python3

from lib.our_converter import Converter

# TODO: yeah... all of this too

def main():
    c = Converter()
    mp3_file = c.get_audio()
    c.chunk_audio(mp3_file)


def handler(event, context):
    convert_video_to_audio(ffmpeg.input(event['video_file']))


if __name__ == "__main__":
    main()
