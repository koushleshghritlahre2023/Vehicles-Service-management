from aws_s3 import s3
from config import Config

response = s3.list_buckets()

print("Connected Successfully")

for bucket in response["Buckets"]:
    print(bucket["Name"])