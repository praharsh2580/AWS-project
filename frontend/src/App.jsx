import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [buckets, setBuckets] = useState([]);
  const [selectedBucket, setSelectedBucket] = useState('');
  const [newBucketName, setNewBucketName] = useState('');
  const [file, setFile] = useState(null);
  const [files, setFiles] = useState([]);
  const [amis, setAmis] = useState([]);
  const [selectedAmi, setSelectedAmi] = useState('');
  const [instanceTypes, setInstanceTypes] = useState([]);
  const [selectedInstanceType, setSelectedInstanceType] = useState('');
  const [instanceId, setInstanceId] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchDropdownData = async () => {
      try {
        const bucketsResponse = await axios.get('http://127.0.0.1:5000/list_buckets');
        setBuckets(bucketsResponse.data.buckets);
        setAmis([
          { name: 'Ubuntu', id: 'ami-00a929b66ed6e0de6' },
          { name: 'CentOS', id: 'ami-04adc082cd8225313' },
          { name: 'Windows', id: 'ami-084568db4383264d4' },
        ]);
        setInstanceTypes([
          { type: 't2.micro', description: 'Small, low-cost instance' },
          { type: 't2.small', description: 'Small instance with more memory' },
          { type: 't2.medium', description: 'Medium-sized instance for moderate workloads' },
        ]);
      } catch (error) {
        setMessage(`Error fetching data: ${error.message}`);
      }
    };

    fetchDropdownData();
  }, []);

  const handleCreateBucket = async () => {
    if (!newBucketName) {
      setMessage('Please enter a bucket name.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/create_bucket', { bucket_name: newBucketName });
      setBuckets((prev) => [...prev, newBucketName]);
      setMessage(response.data.message);
      setNewBucketName('');
    } catch (error) {
      setMessage(`Error creating bucket: ${error.message}`);
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!selectedBucket || !file) {
      setMessage('Please select a bucket and choose a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('bucket_name', selectedBucket);

    try {
      const response = await axios.post('http://127.0.0.1:5000/upload_to_bucket', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setMessage(response.data.message);
      handleListFiles();
    } catch (error) {
      setMessage(`Error uploading file: ${error.message}`);
    }
  };

  const handleListFiles = async () => {
    if (!selectedBucket) {
      setMessage('Please select a bucket.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/list_files', { bucket_name: selectedBucket });
      setFiles(response.data.files);
    } catch (error) {
      setMessage(`Error listing files: ${error.message}`);
    }
  };

  const handleDeleteFile = async (fileKey) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/delete_file', {
        bucket_name: selectedBucket,
        file_key: fileKey,
      });
      setFiles((prevFiles) => prevFiles.filter((file) => file !== fileKey));
      setMessage(response.data.message);
    } catch (error) {
      setMessage(`Error deleting file: ${error.message}`);
    }
  };

  const handleDeleteBucket = async () => {
    if (!selectedBucket) {
      setMessage('Please select a bucket.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/delete_bucket', { bucket_name: selectedBucket });
      setBuckets((prevBuckets) => prevBuckets.filter((bucket) => bucket !== selectedBucket));
      setFiles([]);
      setSelectedBucket('');
      setMessage(response.data.message);
    } catch (error) {
      setMessage(`Error deleting bucket: ${error.message}`);
    }
  };

  const handleLaunchInstance = async () => {
    if (!selectedAmi || !selectedInstanceType) {
      setMessage('Please select an AMI and instance type.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/launch_instance', {
        ami: selectedAmi,
        instance_type: selectedInstanceType,
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage(`Error launching instance: ${error.message}`);
    }
  };

  const handleTerminateInstance = async () => {
    if (!instanceId) {
      setMessage('Please enter an instance ID.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/terminate_instance', { instance_id: instanceId });
      setMessage(response.data.message);
    } catch (error) {
      setMessage(`Error terminating instance: ${error.message}`);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>AWS Resource Management Portal</h1>

      <div style={{ marginBottom: '20px' }}>
        <h3>Create New S3 Bucket</h3>
        <input
          type="text"
          placeholder="Enter bucket name"
          value={newBucketName}
          onChange={(e) => setNewBucketName(e.target.value)}
        />
        <button onClick={handleCreateBucket}>Create Bucket</button>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3>Select an S3 Bucket</h3>
        <select value={selectedBucket} onChange={(e) => setSelectedBucket(e.target.value)}>
          <option value="">Select Bucket</option>
          {buckets.map((bucket, index) => (
            <option key={index} value={bucket}>
              {bucket}
            </option>
          ))}
        </select>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3>Upload File to Selected Bucket</h3>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleFileUpload}>Upload</button>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3>Files in Selected Bucket</h3>
        <button onClick={handleListFiles}>List Files</button>
        {files.length > 0 && (
          <ul>
            {files.map((file, index) => (
              <li key={index}>
                {file}{' '}
                <button onClick={() => handleDeleteFile(file)}>Delete</button>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3>Delete Selected S3 Bucket</h3>
        <button onClick={handleDeleteBucket}>Delete Bucket</button>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3>Launch EC2 Instance</h3>
        <div>
          <label>Choose AMI:</label>
          <select value={selectedAmi} onChange={(e) => setSelectedAmi(e.target.value)}>
            <option value="">Select AMI</option>
            {amis.map((ami, index) => (
              <option key={index} value={ami.id}>
                {ami.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Choose Instance Type:</label>
          <select value={selectedInstanceType} onChange={(e) => setSelectedInstanceType(e.target.value)}>
            <option value="">Select Instance Type</option>
            {instanceTypes.map((instanceType, index) => (
              <option key={index} value={instanceType.type}>
                {instanceType.type} - {instanceType.description}
              </option>
            ))}
          </select>
        </div>
        <button onClick={handleLaunchInstance}>Launch Instance</button>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3>Terminate EC2 Instance</h3>
        <input
          type="text"
          placeholder="Enter Instance ID"
          value={instanceId}
          onChange={(e) => setInstanceId(e.target.value)}
        />
        <button onClick={handleTerminateInstance}>Terminate Instance</button>
      </div>

      {message && <div style={{ marginTop: '20px' }}><strong>{message}</strong></div>}
    </div>
  );
}

export default App;

