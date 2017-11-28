#!/usr/bin/env python3

import os
import sys
import boto3
import ffmpeg
from io import BytesIO
from pydub import AudioSegment


class Converter(object):
    BUFFER = 100
    CHUNK_SIZE = 15000 - 2 * BUFFER
    DEFAULT_VIDEO = ffmpeg.input(sys.argv[1])
    REGION = 'us-east-1'
    PROFILE = 'hackathon'
    VIDEO_BUCKET_NAME = 'sonicthorn-source'
    AUDIO_BUCKET_NAME = 'sonicthorn-audio'
    TEXT_BUCKET_NAME = 'sonicthorn-text'

    def __init__(self, region=REGION, profile=PROFILE):
        self.region = region
        self.profile = profile
        self._session = None
        self._s3_connection = None
        self._audio_bucket = None
        self._text_bucket = None
        self._source_bucket = None

    @property
    def session(self):
        if self._session is None:
            self._session = boto3.Session(region_name=self.region, profile_name=self.profile)
        return self._session

    @property
    def s3_connection(self):
        if self._s3_connection is None:
            self._s3_connection = self.session.client('s3')
        return self._s3_connection

    def upload_to_s3(self, bucket, name, content=None, file_name=None):
        assert not content or not file_name
        if content is not None:
            self.s3_connection.put_object(Bucket=bucket, Key=name, Body=content)
        if file_name is not None:
            print('FILE NAME:', file_name)
            with open(file_name, 'r') as f:
                self.s3_connection.put_object(Bucket=bucket, Key=name, Body=f.read().encode('base64'))

    @classmethod
    def convert_to_time(cls, i):
        seconds = i * (cls.CHUNK_SIZE // 1000)
        minutes = seconds // 60
        seconds = seconds % 60
        hours = minutes // 60
        return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)

    def get_audio(self, video_file=DEFAULT_VIDEO):
        '''convert Video File to Audio'''
        audio_file = '.'.join(sys.argv[1].split('.')[:-1] + ['wav'])
        video_file.output(audio_file).run()
        return audio_file

    # def get_audio(self, video_file=DEFAULT_VIDEO):
    #     '''convert Video File to Audio'''
    #     audio_file = '.'.join(sys.argv[1].split('.')[:-1] + ['wav'])
    #     i = 0
    #     while True:
    #         try:
    #             chunk_name = self.file_chunk_name(audio_file, i)
    #             print(chunk_name)
    #             print(i)
    #             print(self.convert_to_time(i+1))
    #             video_file.output(chunk_name, acodec='pcm_s16le', ar=16000, ac=1, ss=self.convert_to_time(i+1), t='00:00:15').run()
    #             i += 1
    #         except Exception as e:
    #             raise e

    @staticmethod
    def file_chunk_name(orig, i):
        parts = os.path.basename(orig).split('.')
        parts[-2] = '{}-{}'.format(parts[-2], str(i))
        return '.'.join(parts)

    @classmethod
    def file_manifest(cls, orig):
        return cls.file_chunk_name(orig, 'MANIFEST').rstrip('.wav')

    @staticmethod
    def file_chunk_name(orig, i):
        parts = os.path.basename(orig).split('.')
        parts[-2] = '{}-{}'.format(parts[-2], i)
        print('.'.join(parts))
        return '.'.join(parts)

    def chunk_audio(self, file_name):
        '''chunk audio file into 15 second segments'''
        # TODO: clean this up a bit -- offsets and whatnot
        sound = AudioSegment.from_wav(file_name)  # need this JUST FOR THE duration_seconds  UGGGG
        video_file = ffmpeg.input(file_name, format='wav')
        chunk_count = int(sound.duration_seconds+1)//(self.CHUNK_SIZE//1000)
        for i in range(chunk_count):
            chunk_name = self.file_chunk_name(file_name, i)
            video_file.output(chunk_name, acodec='pcm_s16le', ar=16000, ac=1, ss=self.convert_to_time(i), to=self.convert_to_time(i+1)).run()
            with open(chunk_name, 'rb') as f:
                self.upload_to_s3(self.AUDIO_BUCKET_NAME, chunk_name, content=f.read())
        self.upload_to_s3(self.AUDIO_BUCKET_NAME, self.file_manifest(file_name), content=str(chunk_count))

    def upload_video(self, file_name, content):
        self.upload_to_s3(self.VIDEO_BUCKET_NAME, file_name, content=content)


def main():
    c = Converter()
    file_name = c.get_audio()
    c.chunk_audio(file_name)



def handler(event, context):
    convert_video_to_audio(ffmpeg.input(event['video_file']))


if __name__ == "__main__":
    main()
