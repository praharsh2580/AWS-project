from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)

# Initialize EC2 client
ec2 = boto3.client('ec2')

@app.route('/launch_instance', methods=['POST'])
def launch_instance():
    try:
        instance = ec2.run_instances(
            ImageId='ami-071226ecf16aa7d96',  # Replace with your AMI ID
            InstanceType='t2.micro',
            MinCount=1,
            MaxCount=1
        )
        instance_id = instance['Instances'][0]['InstanceId']
        return jsonify({'instance_id': instance_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/terminate_instance', methods=['POST'])
def terminate_instance():
    try:
        instance_id = request.json.get('instance_id')
        ec2.terminate_instances(InstanceIds=[instance_id])
        return f'Instance {instance_id} terminated successfully!'
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
