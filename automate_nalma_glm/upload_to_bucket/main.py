import boto3
import os

def upload_directory_contents_to_s3(local_path, bucket_name, s3_prefix=''):
    s3 = boto3.client('s3')
    
    # Walk through all files and directories in the local path
    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            # Construct S3 key (object key) by combining the s3_prefix and the relative path of the file
            s3_key = os.path.join(s3_prefix, os.path.relpath(local_file_path, local_path)).replace("\\", "/")
            # Upload the file to S3
            s3.upload_file(local_file_path, bucket_name, s3_key)
            print(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_key}")



