#Import all the modules and libraries
import boto3
from pprint import pprint
#Open management console
aws_management_console = boto3.session.Session(profile_name = "default")

#Open EC2 console
ec2_console = aws_management_console.client("ec2")

#Use boto3 docs
instances = ec2_console.describe_instances()

for reservations in instances['Reservations']:
    for instance in reservations['Instances']:
        print(instance['InstanceId'])