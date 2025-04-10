import boto3
from pprint import pprint

aws_management_console = boto3.session.Session(profile_name="default")

ec2_console = aws_management_console.client("ec2")

terminate_instances = ec2_console.terminate_instances(
    InstanceIds = ['i-057ec35927a651527']
)

for terminating in terminate_instances['TerminatingInstances']:
    print(terminating['InstanceId'])