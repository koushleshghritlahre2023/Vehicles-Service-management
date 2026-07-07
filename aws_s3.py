import boto3
from config import Config

s3 = boto3.client(
    "s3",
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name=Config.AWS_REGION
)

def upload_invoice(file_path, file_name):
    s3.upload_file(
        file_path,
        Config.AWS_BUCKET_NAME,
        file_name
    )

    return f"https://{Config.AWS_BUCKET_NAME}.s3.amazonaws.com/{file_name}"