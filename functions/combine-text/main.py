import boto3


DONE_OBJECT_SUFFIX = '-done.txt'


def parse_base_name(name):
    return name.rstrip(DONE_OBJECT_SUFFIX)


def list_objects(client, bucket_name, prefix=None):
    params = {
        'Bucket': bucket_name,
    }
    if prefix:
        params['Prefix'] = prefix

    output = client.list_objects(**params)
    return output['Contents']


def handle(event, context):
    client = boto3.session.Session().client('s3')

    for record in event['Records']:
        if 's3' in record:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']

            base_name = parse_base_name(key)
            parts = key.split('-')
            if len(parts) < 2:
                continue

            prefix = parts[0]

            print('Combining converted text files into single text file for {}.'.format(base_name))

            objs = list_objects(client, bucket)
            sorted(objs, key=lambda o: o['Key'])

            body = ''
            for obj in objs:
                if obj['Key'].startswith(prefix):
                    obj = client.get_object(Bucket=bucket, Key=obj['Key'])
                    body += obj['Body'].read().decode('utf-8')

            client.put_object(Body=body, Bucket=bucket, Key=base_name+'.txt')


if __name__ == '__main__':
    handle({
        'Records': [
            {
                's3': {
                    'bucket': {
                        'name': 'sonicthorn-text',
                    },
                    'object': {
                        'key': '234567-someaudiofile-done.txt',
                    },
                },
            },
        ],
    }, {})
