import boto3

s3=boto3.client("s3")

ec2=boto3.client("ec2")

response_ec2 = ec2.run_instances(
    ImageId='ami-071226ecf16aa7d96',
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1
)
print("EC2 Instance created:",response_ec2)

bucket_name="pranay0987"

response_s3=s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={
        'LocationConstraint': 'us-west-2'
    }
)
print("S3 Bucket created:",response_s3)
