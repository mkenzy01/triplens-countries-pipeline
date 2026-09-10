import io
import json
import os

from dotenv import load_dotenv
from minio import Minio

load_dotenv()


def get_minio_client():
    return Minio(
        os.getenv("MINIO_ENDPOINT"),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False,
    )


def upload_json(data, object_name, bucket_name=None):
    client = get_minio_client()

    if bucket_name is None:
        bucket_name = os.getenv("MINIO_BUCKET")

    json_bytes = json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    ).encode("utf-8")

    data_stream = io.BytesIO(json_bytes)

    client.put_object(
        bucket_name=bucket_name,
        object_name=object_name,
        data=data_stream,
        length=len(json_bytes),
        content_type="application/json",
    )

    print(f"Uploaded to MinIO: {bucket_name}/{object_name}")