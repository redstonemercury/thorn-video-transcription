import boto3

client = boto3.client('lex-runtime')
s3 = boto3.resource('s3')

def convert_audio_to_text(input_file):
    s3.Bucket('sonicthorn-audio').download_file(input_file, '/tmp/audio_file')

    with open('/tmp/audio_file', 'rb') as f:
        output = client.post_content(botName='sonicthorn', botAlias='processaudio', userId='UserOne', contentType='audio/l16; rate=16000; channels=1', accept='audio/pcm', inputStream=f)
        return output


def handle(event, context):
    output = convert_audio_to_text((event['audio_file']))
    print(output)

