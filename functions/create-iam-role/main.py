import boto3

class AWS_Account(object):
    REGION  =  'us-east-1'     
    PROFILE = 'hackathon'
    NAME = 'sonicthorn'

    def __init__(self, region=REGION, profile=PROFILE, name=NAME):
        self.name = name
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
    def iam_connection(self):
        if self._iam_connection is None:
            self._iam_connection = self.session.client('iam')
        return self._iam_connection

    def create_service_role(self, name):
        my_managed_policy = {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Action": [
              "s3:PutObject",
              "s3:GetObject",
              "s3:DeleteObject"
            ],
            "Resource": ["arn:aws:s3:::lam-%s-*" % name]
          }
        ]
        }
        response = iam.create_policy(
        PolicyName=name,
        PolicyDocument=json.dumps(my_managed_policy)
        )

    def create_s3_bucket(self, bucket, name):
        self._s3_connection.create_bucket(
            ACL=private
            Bucket = bucket,
            CreateBucketConfiguration={
            'LocationConstraint': self.region }
            )


def handler(event, context):
    context['Creating service role for lambda.']
    aws = AWS_Account()
    aws.create_service_role
