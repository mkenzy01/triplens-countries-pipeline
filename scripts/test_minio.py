import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from src.storage.minio_client import get_minio_client


client = get_minio_client()

buckets = client.list_buckets()

print("Connected to MinIO successfully.")
print("Buckets:")

for bucket in buckets:
    print(f"- {bucket.name}")