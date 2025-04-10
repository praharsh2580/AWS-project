import boto3

aws_management_console = boto3.session.Session(profile_name="default")

s3_console = aws_management_console.client("s3")

delete_s3 = s3_console.delete_bucket(
    Bucket = "pranay2580"
)