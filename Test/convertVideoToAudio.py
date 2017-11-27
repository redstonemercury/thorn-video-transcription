import argparse
import ffmpeg

PARSER = argparse.ArgumentParser(description='Convert Video to Audio using ffmpeg API')
PARSER.add_argument('--i', metavar='i', type=str, nargs=1)
ARGS = PARSER.parse_args()
VIDEO = ffmpeg.input(ARGS.i[0])

def convert_video_to_audio(video_file):
    '''convert Video File to Audio'''
    video_file.output(ARGS.i[0] + '.mp3').run()
    return

def main():
    convert_video_to_audio(VIDEO)

if __name__ == "__main__": main()