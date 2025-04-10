# from flask import Flask, render_template, request, jsonify
# import boto3
# import os
# from flask_cors import CORS # type: ignore

# app = Flask(__name__)
# CORS(app)
# # Initialize AWS Services
# s3 = boto3.client('s3')
# ec2 = boto3.client('ec2')

# # S3 Bucket Name
# BUCKET_NAME = 'praharsh123456789'  # Replace with your bucket name

# @app.route('/')
# def index():
#     return render_template('index.html')

# # S3: Upload File
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     try:
#         file = request.files['file']
#         s3.upload_fileobj(file, BUCKET_NAME, file.filename)
#         return 'File uploaded successfully!'
#     except Exception as e:
#         return str(e)

# # S3: List Files
# @app.route('/list_files', methods=['GET'])
# def list_files():
#     try:
#         objects = s3.list_objects_v2(Bucket=BUCKET_NAME).get('Contents', [])
#         files = [obj['Key'] for obj in objects]
#         return jsonify({'files': files})
#     except Exception as e:
#         return str(e)

# # EC2: Launch Instance
# @app.route('/launch_instance', methods=['POST'])
# def launch_instance():
#     try:
#         instance = ec2.run_instances(
#             ImageId='ami-071226ecf16aa7d96',  # Replace with a valid AMI ID
#             InstanceType='t2.micro',
#             MinCount=1,
#             MaxCount=1
#         )
#         instance_id = instance['Instances'][0]['InstanceId']
#         return jsonify({'instance_id': instance_id})
#     except Exception as e:
#         return str(e)

# # EC2: Terminate Instance
# @app.route('/terminate_instance', methods=['POST'])
# def terminate_instance():
#     try:
#         instance_id = request.json.get('instance_id')
#         ec2.terminate_instances(InstanceIds=[instance_id])
#         return f'Instance {instance_id} terminated successfully!'
#     except Exception as e:
#         return str(e)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
import boto3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

ec2 = boto3.client('ec2')
s3 = boto3.client('s3')


@app.route('/')
def index():
    return "AWS Resource Management Backend Running"


# Launch EC2 instance
@app.route('/launch_instance', methods=['POST'])
def launch_instance():
    try:
        ami_id = request.json.get('ami')  # AMI ID
        instance_type = request.json.get('instance_type')  # Instance Type

        instance = ec2.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1
        )
        instance_id = instance['Instances'][0]['InstanceId']
        return jsonify({'message': f"EC2 Instance '{instance_id}' launched successfully!"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Terminate EC2 instance
@app.route('/terminate_instance', methods=['POST'])
def terminate_instance():
    try:
        instance_id = request.json.get('instance_id')  # Instance ID

        ec2.terminate_instances(InstanceIds=[instance_id])
        return jsonify({'message': f"EC2 Instance '{instance_id}' terminated successfully!"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Create S3 bucket
@app.route('/create_bucket', methods=['POST'])
def create_bucket():
    try:
        bucket_name = request.json.get('bucket_name')  # Bucket Name

        s3.create_bucket(Bucket=bucket_name)
        return jsonify({'message': f"Bucket '{bucket_name}' created successfully!"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# List S3 buckets
@app.route('/list_buckets', methods=['GET'])
def list_buckets():
    try:
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return jsonify({'buckets': buckets})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Upload file to bucket
@app.route('/upload_to_bucket', methods=['POST'])
def upload_to_bucket():
    try:
        file = request.files['file']  # File
        bucket_name = request.form.get('bucket_name')  # Bucket Name

        s3.upload_fileobj(file, bucket_name, file.filename)
        return jsonify({'message': f"File '{file.filename}' uploaded successfully to bucket '{bucket_name}'!"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# List files in bucket
@app.route('/list_files', methods=['POST'])
def list_files():
    try:
        bucket_name = request.json.get('bucket_name')  # Bucket Name
        objects = s3.list_objects_v2(Bucket=bucket_name).get('Contents', [])
        files = [obj['Key'] for obj in objects] if objects else []
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Delete file from bucket
@app.route('/delete_file', methods=['POST'])
def delete_file():
    try:
        bucket_name = request.json.get('bucket_name')  # Bucket Name
        file_key = request.json.get('file_key')  # File Key

        s3.delete_object(Bucket=bucket_name, Key=file_key)
        return jsonify({'message': f"File '{file_key}' deleted successfully from bucket '{bucket_name}'!"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Delete S3 bucket
@app.route('/delete_bucket', methods=['POST'])
def delete_bucket():
    try:
        bucket_name = request.json.get('bucket_name')  # Bucket Name

        # Ensure bucket is empty before deletion
        objects = s3.list_objects_v2(Bucket=bucket_name).get('Contents', [])
        for obj in objects:
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])

        s3.delete_bucket(Bucket=bucket_name)
        return jsonify({'message': f"Bucket '{bucket_name}' deleted successfully!"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)

