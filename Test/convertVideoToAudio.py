import argparse
import ffmpeg
from pydub import AudioSegment

PARSER = argparse.ArgumentParser(description='Convert Video to Audio using ffmpeg API')
PARSER.add_argument('--i', metavar='i', type=str, nargs=1)
ARGS = PARSER.parse_args()
VIDEO_FILE_PATH = ARGS.i[0]
VIDEO = ffmpeg.input(VIDEO_FILE_PATH)
MP3_FILENAME = VIDEO_FILE_PATH + ".mp3"

def convert_video_to_audio(video_file):
    '''convert Video File to Audio'''
    video_file.output(MP3_FILENAME).run()
    return

def chunk_audio(file):
    '''chunk audio file into 15 second segments'''
    sound = AudioSegment.from_mp3(file)
    if sound.duration_seconds <= 15.0:
        print "Audio file is less than or equal to 15 seconds in length"
    else:
        # split sound in 5-second slices and export
        for i, chunk in enumerate(sound[::15000]):
          with open("sound-%s.mp3" % i, "wb") as f:
            chunk.export(f, format="mp3")
        

def main():
    convert_video_to_audio(VIDEO)
    chunk_audio(MP3_FILENAME)

if __name__ == "__main__": main()