from ii_agent.storage import BaseStorage, GCS, LocalStorage
import os


def create_storage_client(
    storage_provider: str = "local",
    project_id: str = "",
    bucket_name: str = "",
    custom_domain: str | None = None,
) -> BaseStorage:
    """Create storage client based on provider.
    
    For GCS, credentials are automatically loaded from:
    1. GOOGLE_APPLICATION_CREDENTIALS env var (path to JSON)
    2. gcloud ADC (~/.config/gcloud/)
    3. GOOGLE_CREDENTIALS env var (JSON string)
    
    Args:
        storage_provider: "gcs" or "local"
        project_id: GCP project ID (auto-detected for GCS if not provided)
        bucket_name: GCS bucket name
        custom_domain: Custom domain for public URLs
        
    Returns:
        Storage client instance
    """
    # Allow override from environment
    storage_provider = os.environ.get("STORAGE_PROVIDER", storage_provider)
    bucket_name = os.environ.get("STORAGE_BUCKET", bucket_name) or "ii-agent-storage"
    project_id = os.environ.get("STORAGE_PROJECT_ID", project_id)
    
    if storage_provider == "gcs":
        return GCS(
            project_id=project_id,
            bucket_name=bucket_name,
            custom_domain=custom_domain,
        )
    elif storage_provider == "local":
        return LocalStorage(base_path=os.path.expanduser("~/.ii_agent/storage"))
    raise ValueError(f"Storage provider {storage_provider} not supported")
