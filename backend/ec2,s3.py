from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import boto3
import os

app = Flask(__name__, static_folder='build', static_url_path='')
CORS(app)
 
@app.route('/')
def serve_react():
    return send_from_directory(app.static_folder, 'index.html')

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

