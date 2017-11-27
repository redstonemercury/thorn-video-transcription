import ffmpeg
import argparse

PARSER = argparse.ArgumentParser(description='Convert Video to Audio using ffmpeg API')
PARSER.add_argument('--i', metavar='i', type=str, nargs=1)
ARGS = PARSER.parse_args()
VIDEO = ffmpeg.input(ARGS.i[0])

def convertVideoToAudio(VIDEO):
    VIDEO.output(ARGS.i[0] + '.mp3').run()
    return
