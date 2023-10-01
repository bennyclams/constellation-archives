from werkzeug.utils import secure_filename
import boto3
import uuid
import os

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

def upload_file_to_s3(f, acl="public-read", prefix="images/"):
    filename = secure_filename(f.filename)
    file_ext = filename.split(".")[-1]
    r_filename = str(uuid.uuid4())
    filename = r_filename + "." + file_ext
    if not prefix.endswith("/"):
        prefix += "/"
    filename = prefix + filename
    s3.upload_fileobj(
        f,
        os.getenv("AWS_BUCKET_NAME"),
        filename,
        ExtraArgs={
            # "ACL": acl,
            "ContentType": f.content_type
        }
    )
    return filename
