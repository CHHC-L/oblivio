from flask import request
from google.cloud import storage
from app import gcs_client
import os

def handle_upload(request):
    file = request.files['file']
    if not file:
        return "No file uploaded", 400
    bucket_name = os.environ.get('GCS_BUCKET_NAME')
    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file.stream)
    return f"File {file.filename} uploaded successfully"
