import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from src.storage.minio_client import upload_json


sample_data = {
    "project": "TripLens",
    "status": "MinIO upload test",
    "success": True,
}


upload_json(
    data=sample_data,
    object_name="tests/minio_upload_test.json"
)