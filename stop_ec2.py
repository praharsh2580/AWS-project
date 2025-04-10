import boto3

aws_management_console = boto3.session.Session(profile_name="default")

ec2_console = aws_management_console.client("ec2")

stop_instance = ec2_console.stop_instances(
    InstanceIds = ['i-057ec35927a651527']
)
