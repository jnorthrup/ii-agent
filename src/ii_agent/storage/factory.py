from ii_agent.storage import BaseStorage, GCS, LocalStorage
import os


def create_storage_client(
    storage_provider: str,
    project_id: str = "",
    bucket_name: str = "",
    custom_domain: str | None = None,
) -> BaseStorage:
    if storage_provider == "gcs":
        return GCS(
            project_id,
            bucket_name,
            custom_domain,
        )
    elif storage_provider == "local":
        return LocalStorage(base_path=os.path.expanduser("~/.ii_agent/storage"))
    raise ValueError(f"Storage provider {storage_provider} not supported")
