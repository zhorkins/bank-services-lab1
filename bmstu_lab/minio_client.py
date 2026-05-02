import uuid
from minio import Minio
from django.conf import settings

class MinioClient:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_USE_HTTPS
        )
        self.bucket = settings.MINIO_BUCKET_NAME
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def upload_file(self, file, folder='img'):
        ext = file.name.split('.')[-1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        object_name = f"{folder}/{filename}"
        self.client.put_object(
            self.bucket, object_name, file, length=-1, part_size=10*1024*1024,
            content_type=file.content_type
        )
        return object_name