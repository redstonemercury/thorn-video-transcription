#!/usr/bin/env python3

from lib.our_converter import Converter


def main(video_file):
    """ This will take in a video file, split it into wavs, then upload it to S3 """
    c = Converter()
    with open(video_file, 'rb') as f:
        c.upload_video(video_file, f.read())
    mp3_file = c.get_audio()
    c.chunk_audio(mp3_file)


def handler(event, context):
    convert_video_to_audio(ffmpeg.input(event['video_file']))


if __name__ == "__main__":
    main()
