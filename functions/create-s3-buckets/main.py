def handler(event, context):
    print('Creating s3 buckets.')

class AWS_Account(object):
    REGION  =  'us-east-1'     
    PROFILE = 'hackathon'

    def __init__(self, region=REGION, profile=PROFILE):
        self.region = region
        self.profile = profile
        self._session = None
        self._s3_connection = None
        self._iam_connection = None
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

    def create_s3_bucket(self, bucket):
        self._s3_connection.create_bucket(
            ACL = 'private',
            Bucket = bucket,
            CreateBucketConfiguration={
            'LocationConstraint': self.region }
            )

def handler(event, context):
    aws = AWS_Account()
    aws.create_s3_bucket('lam-sonicthorn-source')
    aws.create_s3_bucket('lam-sonicthorn-source')
    aws.create_s3_bucket('lam-sonicthorn-source')

