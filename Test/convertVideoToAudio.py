#!/usr/bin/env python3

import sys
import ffmpeg
from io import BytesIO
import boto3
from pydub import AudioSegment


class Converter(object):
    CHUNK_SIZE = 15000
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

    def upload_to_s3(self, bucket, name, content):
        self.s3_connection.put_object(Bucket=bucket, Key=name, Body=content)

    def get_audio(self, video_file=DEFAULT_VIDEO):
        '''convert Video File to Audio'''
        mp3_file = '.'.join(sys.argv[1].split('.')[:-1] + ['mp3'])
        video_file.output(mp3_file).run()
        return mp3_file

    @staticmethod
    def file_chunk_name(orig, i):
        parts = orig.split('.')
        parts[-2] = '{}-{}'.format(parts[-2], i)
        return '.'.join(parts)

    def chunk_audio(self, file_name):
        '''chunk audio file into 15 second segments'''
        sound = AudioSegment.from_mp3(file_name)
        for i in range(int(sound.duration_seconds+1)//int(self.CHUNK_SIZE/1000)):
            chunk_stream = BytesIO()
            chunk = sound[i*self.CHUNK_SIZE:(i+1)*self.CHUNK_SIZE].export(chunk_stream, format='mp3')
            chunk_name = self.file_chunk_name(file_name, i)
            self.upload_to_s3(self.AUDIO_BUCKET_NAME, chunk_name, chunk)


def main():
    c = Converter()
    mp3_file = c.get_audio()
    c.chunk_audio(mp3_file)


def handler(event, context):
    convert_video_to_audio(ffmpeg.input(event['video_file']))


if __name__ == "__main__":
    main()
