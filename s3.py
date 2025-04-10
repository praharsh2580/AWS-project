from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)

# Initialize S3 client
s3 = boto3.client('s3')

# S3 Bucket Name
BUCKET_NAME = 'praharsh45678'  # Replace with your bucket name

# Route to upload a file to S3

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)
        return jsonify({'message':'Upload Successful'}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500


# Route to list all files in S3
@app.route('/list_files', methods=['GET'])
def list_files():
    try:
        objects = s3.list_objects_v2(Bucket=BUCKET_NAME).get('Contents', [])
        files = [obj['Key'] for obj in objects]  # Extract filenames from the response
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
