import asyncio
import io
from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.exceptions import ClientError



class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
            self,
            file_path: str,
    ):
        object_name = file_path.split("/")[-1]
        try:
            async with self.get_client() as client:
                with open(file_path, "rb") as file:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        Body=file,
                    )
        except ClientError as e:
            print(f"Error uploading file: {e}")

    async def upload_file_v2(self, file_obj, filename: str):
        try:
            async with self.get_client() as client:
                file_bytes = io.BytesIO(file_obj.read())
                file_bytes.seek(0)
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=filename,
                    Body=file_bytes,
                )
                print(f"File {filename} uploaded to {self.bucket_name}")
        except Exception as e:
            print(f"Error uploading file: {e}")

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
        except ClientError as e:
            print(f"Error deleting file: {e}")

    async def get_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                data = await response["Body"].read()
                return data
        except ClientError as e:
            print(f"Error downloading file: {e}")
