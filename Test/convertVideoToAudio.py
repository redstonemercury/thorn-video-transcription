#!/usr/bin/env python3
import sys
import ffmpeg

from pydub import AudioSegment


CHUNK_SIZE = 15


def get_audio():
    '''convert Video File to Audio'''
    video_file = ffmpeg.input(sys.argv[1])
    mp3_file = '.'.join(sys.argv[1].split('.')[:-1] + ['mp3'])
    video_file.output().run()
    return


def chunk_audio(file_name):
    '''chunk audio file into 15 second segments'''
    sound = AudioSegment.from_mp3(file_name)
    for i in range((sound.duration_seconds+1)//CHUNK_SIZE):
        with open('sound-{}.mp3'.format(i), 'wb') as f:
            sound.export(f, format='mp3')


def main():
    convert_video_to_audio(VIDEO)
    chunk_audio(MP3_FILENAME)


def handler(event, context):
	convert_video_to_audio(ffmpeg.input(event['video_file']))


if __name__ == "__main__": main()
