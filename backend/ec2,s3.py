from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

# Flask App Setup
app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or not AWS_REGION:
    raise ValueError("AWS credentials or region are not set. Please configure them.")

# Initialize AWS Clients
ec2 = boto3.client(
    'ec2',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# Serve React Frontend
@app.route('/')
def serve_react():
    return send_from_directory(app.static_folder, 'index.html')

# API Endpoints
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

@app.route('/terminate_instance', methods=['POST'])
def terminate_instance():
    try:
        instance_id = request.json.get('instance_id')  # Instance ID

        ec2.terminate_instances(InstanceIds=[instance_id])
        return jsonify({'message': f"EC2 Instance '{instance_id}' terminated successfully!"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_bucket', methods=['POST'])
def create_bucket():
    try:
        bucket_name = request.json.get('bucket_name')  # Bucket Name

        s3.create_bucket(Bucket=bucket_name)
        return jsonify({'message': f"Bucket '{bucket_name}' created successfully!"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list_buckets', methods=['GET'])
def list_buckets():
    try:
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return jsonify({'buckets': buckets})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_to_bucket', methods=['POST'])
def upload_to_bucket():
    try:
        file = request.files['file']  # File
        bucket_name = request.form.get('bucket_name')  # Bucket Name

        s3.upload_fileobj(file, bucket_name, file.filename)
        return jsonify({'message': f"File '{file.filename}' uploaded successfully to bucket '{bucket_name}'!"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list_files', methods=['POST'])
def list_files():
    try:
        bucket_name = request.json.get('bucket_name')  # Bucket Name
        objects = s3.list_objects_v2(Bucket=bucket_name).get('Contents', [])
        files = [obj['Key'] for obj in objects] if objects else []
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_file', methods=['POST'])
def delete_file():
    try:
        bucket_name = request.json.get('bucket_name')  # Bucket Name
        file_key = request.json.get('file_key')  # File Key

        s3.delete_object(Bucket=bucket_name, Key=file_key)
        return jsonify({'message': f"File '{file_key}' deleted successfully from bucket '{bucket_name}'!"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_bucket', methods=['POST'])
def delete_bucket():
    try:
        bucket_name = request.json.get('bucket_name')  # Bucket Name

        objects = s3.list_objects_v2(Bucket=bucket_name).get('Contents', [])
        for obj in objects:
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])

        s3.delete_bucket(Bucket=bucket_name)
        return jsonify({'message': f"Bucket '{bucket_name}' deleted successfully!"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run Flask App
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
