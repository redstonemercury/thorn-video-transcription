import boto3
import json

client = boto3.client('lex-runtime')
s3 = boto3.resource('s3')

def convert_audio_to_text(input_file):
    s3.Bucket('sonicthorn-audio').download_file(input_file, '/tmp/' + input_file)

    with open('/tmp/' + input_file, 'rb') as f:
        output = client.post_content(botName='sonicthorn', botAlias='processaudio', userId='UserOne', contentType='audio/l16; rate=16000; channels=1', accept='audio/pcm', inputStream=f)
        return output


def write_text_file(output, output_file):
    output_file = open(output_file, 'w')
    output_file.write(json.dumps(output['ResponseMetadata']['HTTPHeaders']))
    output_file.close()


def upload_to_s3(input_file, write_file):
    s3.Object('sonicthorn-text', input_file).upload_file(write_file)


def handle(event, context):
    file_root = event['Records'][0]['s3']['object']['key']
    write_file = '/tmp/' + file_root + '.txt'

    output = convert_audio_to_text(file_root)

    write_text_file(output, write_file)

    upload_to_s3(file_root + '.txt', write_file)

