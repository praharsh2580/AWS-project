import boto3

s3_console = boto3.client('s3')

download = s3_console.download_file('pranay2580', 's3example.txt', 'C:\\Users\\dpraharsh\\OneDrive - Hitachi Vantara\\Desktop\\s3download.txt')
