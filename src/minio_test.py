import boto3
from botocore.client import Config

# MinIO credentials
MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
BUCKET_NAME = "demo-bucket"  # Make sure you've created this bucket in MinIO console

def main():
    # Create the S3 client pointing to MinIO
    s3_client = boto3.client(
        's3',
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name="us-east-1"
    )

    # 1. List buckets
    response = s3_client.list_buckets()
    print("Buckets:", [bucket['Name'] for bucket in response['Buckets']])
    
    # 2. Upload a file (or string) to MinIO
    file_data = b"Hello from MinIO!"
    object_key = "test-folder/hello.txt"
    
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=object_key,
        Body=file_data
    )
    print(f"Uploaded '{object_key}' to bucket '{BUCKET_NAME}'.")

    # 3. Download the file
    response = s3_client.get_object(
        Bucket=BUCKET_NAME, 
        Key=object_key
    )
    content = response['Body'].read().decode('utf-8')
    print("File content:", content)
    
    # 4. List objects in the bucket
    objects = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    if 'Contents' in objects:
        print("Objects in bucket:")
        for obj in objects['Contents']:
            print(" -", obj['Key'])

if __name__ == '__main__':
    main()
