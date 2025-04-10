import boto3

aws_management_console=boto3.session.Session(profile_name="default")

iam_console=aws_management_console.client("iam")

result=iam_console.list_users()
print(result)
