import ffmpeg
import argparse

PARSER = argparse.ArgumentParser(description='Convert Video to Audio using ffmpeg API')
PARSER.add_argument('--i', metavar='i', type=str, nargs=1)
ARGS = PARSER.parse_args()
print ARGS.i[0]
VIDEO = ffmpeg.input(ARGS.i[0])
