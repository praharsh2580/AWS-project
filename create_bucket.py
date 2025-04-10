import boto3

aws_management_console = boto3.session.Session(profile_name = "default")

s3_console = boto3.client("s3")

create_bucket = s3_console.create_bucket(
    Bucket = "pranay2580",
    CreateBucketConfiguration={
        'LocationConstraint': 'ap-south-1', #For regions other than us-east-1, include a valid LocationConstraint
    },
)