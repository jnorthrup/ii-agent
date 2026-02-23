"""Local file storage implementation."""

import os
import shutil
from pathlib import Path
from typing import Optional

from .base import BaseStorage


class LocalStorage(BaseStorage):
    """Local file storage backend."""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def upload(self, file_path: str, content: bytes) -> str:
        full_path = self.base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(content)
        return str(full_path)

    async def download(self, file_path: str) -> bytes:
        full_path = self.base_path / file_path
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return full_path.read_bytes()

    async def delete(self, file_path: str) -> bool:
        full_path = self.base_path / file_path
        if full_path.exists():
            full_path.unlink()
            return True
        return False

    async def exists(self, file_path: str) -> bool:
        return (self.base_path / file_path).exists()

    async def is_exists(self, file_path: str) -> bool:
        return await self.exists(file_path)

    async def get_url(self, file_path: str) -> str:
        full_path = self.base_path / file_path
        return f"file://{full_path}"

    async def get_public_url(self, file_path: str) -> str:
        return await self.get_url(file_path)

    async def get_permanent_url(self, file_path: str) -> str:
        return await self.get_url(file_path)

    async def get_download_signed_url(self, file_path: str, expiration: int = 3600) -> str:
        return await self.get_url(file_path)

    async def get_upload_signed_url(self, file_path: str, expiration: int = 3600) -> str:
        return await self.get_url(file_path)

    async def get_file_size(self, file_path: str) -> int:
        full_path = self.base_path / file_path
        if full_path.exists():
            return full_path.stat().st_size
        return 0

    async def list_files(self, prefix: str = "") -> list[str]:
        search_path = self.base_path / prefix if prefix else self.base_path
        if not search_path.exists():
            return []
        return [str(p.relative_to(self.base_path)) for p in search_path.rglob("*") if p.is_file()]

    async def read(self, file_path: str) -> bytes:
        return await self.download(file_path)

    async def write(self, file_path: str, content: bytes) -> str:
        return await self.upload(file_path, content)

    async def upload_and_get_permanent_url(self, file_path: str, content: bytes) -> str:
        await self.upload(file_path, content)
        return await self.get_permanent_url(file_path)

    async def write_from_url(self, file_path: str, url: str) -> str:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return await self.upload(file_path, response.content)
