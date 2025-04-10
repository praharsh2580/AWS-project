import boto3
from pprint import pprint

s3_console = boto3.client('s3')
response = s3_console.upload_file('C:\\Users\\dpraharsh\\OneDrive - Hitachi Vantara\\Desktop\\AWS\\S3\\s3example.txt', 'pranay2580', 's3example.txt')
print(response)
