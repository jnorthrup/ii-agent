"""
Google Cloud Storage implementation.

Uses credentials from:
1. GOOGLE_APPLICATION_CREDENTIALS environment variable
2. gcloud application default credentials (~/.config/gcloud/)
3. GOOGLE_CREDENTIALS environment variable (JSON string)
"""

import os
import json
from pathlib import Path
from typing import Optional

from .base import BaseStorage


class GCS(BaseStorage):
    """Google Cloud Storage backend."""

    def __init__(
        self,
        project_id: str = "",
        bucket_name: str = "",
        custom_domain: Optional[str] = None,
    ):
        """Initialize GCS storage.
        
        Credentials are loaded automatically from:
        1. GOOGLE_APPLICATION_CREDENTIALS env var (path to credentials JSON)
        2. gcloud ADC (~/.config/gcloud/application_default_credentials.json)
        3. GOOGLE_CREDENTIALS env var (JSON string)
        
        Args:
            project_id: GCP project ID (optional, auto-detected if not provided)
            bucket_name: GCS bucket name
            custom_domain: Custom domain for public URLs (optional)
        """
        from google.cloud import storage as gcs_storage
        
        self.bucket_name = bucket_name
        self.custom_domain = custom_domain
        
        # Initialize GCS client with automatic credential detection
        self.client = self._create_gcs_client(project_id, gcs_storage)
        self.bucket = self.client.bucket(bucket_name)

    def _create_gcs_client(self, project_id: str, gcs_storage):
        """Create GCS client with credential auto-detection."""
        
        # Try GOOGLE_APPLICATION_CREDENTIALS first
        credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if credentials_path and Path(credentials_path).exists():
            from google.oauth2 import service_account
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
            return gcs_storage.Client(
                project=project_id or credentials.project_id,
                credentials=credentials
            )
        
        # Try GOOGLE_CREDENTIALS (JSON string)
        credentials_json = os.environ.get('GOOGLE_CREDENTIALS')
        if credentials_json:
            from google.oauth2 import service_account
            credentials_info = json.loads(credentials_json)
            credentials = service_account.Credentials.from_service_account_info(
                credentials_info
            )
            return gcs_storage.Client(
                project=project_id or credentials_info.get('project_id'),
                credentials=credentials
            )
        
        # Fall back to gcloud ADC (Application Default Credentials)
        # This uses ~/.config/gcloud/application_default_credentials.json
        return gcs_storage.Client(project=project_id)

    async def upload(self, file_path: str, content: bytes) -> str:
        """Upload a file to GCS."""
        blob = self.bucket.blob(file_path)
        blob.upload_from_string(content)
        return f"gs://{self.bucket_name}/{file_path}"

    async def download(self, file_path: str) -> bytes:
        """Download a file from GCS."""
        blob = self.bucket.blob(file_path)
        return blob.download_as_bytes()

    async def delete(self, file_path: str) -> bool:
        """Delete a file from GCS."""
        blob = self.bucket.blob(file_path)
        if blob.exists():
            blob.delete()
            return True
        return False

    async def exists(self, file_path: str) -> bool:
        """Check if a file exists in GCS."""
        blob = self.bucket.blob(file_path)
        return blob.exists()

    async def is_exists(self, file_path: str) -> bool:
        return await self.exists(file_path)

    async def get_url(self, file_path: str) -> str:
        """Get GCS URL for a file."""
        if self.custom_domain:
            return f"https://{self.custom_domain}/{file_path}"
        return f"gs://{self.bucket_name}/{file_path}"

    async def get_public_url(self, file_path: str) -> str:
        """Get public URL (makes blob public first)."""
        blob = self.bucket.blob(file_path)
        if not blob.public_url:
            blob.make_public()
        return blob.public_url

    async def get_permanent_url(self, file_path: str) -> str:
        """Get permanent URL (same as public URL)."""
        return await self.get_public_url(file_path)

    async def get_download_signed_url(
        self, 
        file_path: str, 
        expiration: int = 3600
    ) -> str:
        """Get signed URL for downloading."""
        blob = self.bucket.blob(file_path)
        return blob.generate_signed_url(
            version="v4",
            expiration=expiration,
            method="GET"
        )

    async def get_upload_signed_url(
        self, 
        file_path: str, 
        expiration: int = 3600
    ) -> str:
        """Get signed URL for uploading."""
        blob = self.bucket.blob(file_path)
        return blob.generate_signed_url(
            version="v4",
            expiration=expiration,
            method="PUT"
        )

    async def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes."""
        blob = self.bucket.blob(file_path)
        if blob.exists():
            blob.reload()
            return blob.size
        return 0

    async def list_files(self, prefix: str = "") -> list[str]:
        """List files in GCS bucket."""
        blobs = self.bucket.list_blobs(prefix=prefix)
        return [blob.name for blob in blobs]

    async def read(self, file_path: str) -> bytes:
        """Read file content."""
        return await self.download(file_path)

    async def write(self, file_path: str, content: bytes) -> str:
        """Write content to file."""
        return await self.upload(file_path, content)

    async def upload_and_get_permanent_url(self, file_path: str, content: bytes) -> str:
        """Upload and get permanent URL."""
        await self.upload(file_path, content)
        return await self.get_permanent_url(file_path)

    async def write_from_url(self, file_path: str, url: str) -> str:
        """Download from URL and upload to GCS."""
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return await self.upload(file_path, response.content)
