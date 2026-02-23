import asyncio
import logging
import os
import subprocess
from typing import Optional

from ii_agent.core.storage.models.settings import Settings
from ii_agent.sandbox.base_sandbox import BaseSandbox
from ii_agent.sandbox.sandbox_registry import SandboxRegistry
from ii_agent.utils.constants import WorkSpaceMode

logger = logging.getLogger(__name__)

@SandboxRegistry.register(WorkSpaceMode.TART)
class TartSandbox(BaseSandbox):
    """
    Sandbox implementation using Tart for macOS virtualization.
    """
    mode: WorkSpaceMode = WorkSpaceMode.TART

    def __init__(self, session_id: str, settings: Settings):
        super().__init__(session_id=session_id, settings=settings)
        self.vm_name = f"ii-agent-{session_id}"
        self.ip_address: Optional[str] = None

    async def create(self) -> None:
        """
        Creates a new Tart VM.
        For now, we assume a base image 'ghcr.io/cirruslabs/ubuntu:latest' exists.
        """
        logger.info(f"Creating Tart VM: {self.vm_name}")
        # clone from a base image
        base_image = os.getenv("TART_BASE_IMAGE", "openclaw-ubuntu")
        cmd = ["tart", "clone", base_image, self.vm_name]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            logger.error(f"Failed to clone Tart VM: {stderr.decode()}")
            raise RuntimeError(f"Tart clone failed: {stderr.decode()}")
        
        # Automatically start the VM after creation
        await self.start()

    async def start(self) -> None:
        """
        Starts the Tart VM with workspace mounting.
        """
        from ii_agent.core.config.utils import load_ii_agent_config
        from ii_agent.sandbox.config import SandboxSettings

        config = SandboxSettings()
        host_workspace = os.path.join(load_ii_agent_config().host_workspace, self.session_id)
        os.makedirs(host_workspace, exist_ok=True)

        logger.info(f"Starting Tart VM: {self.vm_name} with mount {host_workspace}")
        
        # Mount workspace, project code, and cloud-init config
        project_root = os.getcwd()
        cloud_init_dir = os.path.join(project_root, "cloud-init-setup")
        cmd = [
            "tart", "run", 
            f"--dir=workspace:{host_workspace}",
            f"--dir=code:{project_root}",
            f"--dir=cloud-init:{cloud_init_dir}",
            self.vm_name
        ]
        
        # We don't use --detach because some Tart versions don't support it.
        # instead we just don't await the process completion here.
        self._process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Check if it failed immediately (within 2 seconds)
        try:
            await asyncio.wait_for(self._process.wait(), timeout=2.0)
            if self._process.returncode != 0:
                stdout, stderr = await self._process.communicate()
                logger.error(f"Failed to start Tart VM: {stderr.decode()}")
                raise RuntimeError(f"Tart run failed: {stderr.decode()}")
        except asyncio.TimeoutError:
            # Still running, which is good for a VM process
            pass

        # Wait for IP
        await self._wait_for_ip()
        
        # Setup the guest over SSH
        await self._setup_guest()
        
        self.host_url = f"http://{self.ip_address}:{os.getenv('BACKEND_PORT', 8000)}"

    async def _setup_guest(self) -> None:
        """
        Configures the guest VM over SSH.
        """
        logger.info(f"Setting up Tart guest: {self.vm_name} at {self.ip_address}")
        
        # Give cloud-init a moment to process the config
        logger.info("Waiting 20 seconds for cloud-init to process...")
        await asyncio.sleep(20)
        
        # Commands to run in the guest
        setup_cmds = [
            "sudo mkdir -p /mnt/workspace /mnt/code",
            "sudo mount -t virtiofs workspace /mnt/workspace",
            "sudo mount -t virtiofs code /mnt/code",
            "python3 -m pip install pydantic pydantic-settings httpx fastapi uvicorn aiofiles",
            "export PYTHONPATH=/mnt/code/src",
            "cd /mnt/workspace",
            "nohup python3 /mnt/code/src/ii_agent/utils/tool_client/sandbox_server.py --port 8000 > /tmp/sandbox.log 2>&1 &",
            "sleep 5" # Give it a moment to start
        ]
        
        full_cmd = " && ".join(setup_cmds)
        
        # Use SSH with the injected key (trying cirrus user)
        ssh_cmd = [
            "ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=10", "-o", "BatchMode=yes",
            f"cirrus@{self.ip_address}",
            full_cmd
        ]
        
        process = await asyncio.create_subprocess_exec(
            *ssh_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            logger.warning(f"Guest setup failed with key (user cirrus): {stderr.decode()}")
            # Fallback to sshpass if key injection didn't work for some reason
            ssh_cmd = [
                "/opt/homebrew/bin/sshpass", "-p", "cirrus",
                "ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=10",
                f"cirrus@{self.ip_address}",
                full_cmd
            ]
            process = await asyncio.create_subprocess_exec(
                *ssh_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                 logger.warning(f"Fallback guest setup also failed for user cirrus: {stderr.decode()}")
                 
                 # Final fallback to ubuntu user
                 ssh_cmd = [
                    "/opt/homebrew/bin/sshpass", "-p", "ubuntu",
                    "ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=10",
                    f"ubuntu@{self.ip_address}",
                    full_cmd
                ]
                 process = await asyncio.create_subprocess_exec(
                    *ssh_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                 await process.wait()

    async def _wait_for_ip(self, timeout: int = 60) -> str:
        """
        Waits for the VM to get an IP address.
        """
        logger.info(f"Waiting for IP for Tart VM: {self.vm_name}")
        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < timeout:
            cmd = ["tart", "ip", self.vm_name]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode == 0:
                self.ip_address = stdout.decode().strip()
                logger.info(f"Tart VM IP: {self.ip_address}")
                return self.ip_address
            await asyncio.sleep(2)
        
        raise TimeoutError(f"Timed out waiting for IP for VM {self.vm_name}")

    async def stop(self) -> None:
        """
        Stops the Tart VM.
        """
        logger.info(f"Stopping Tart VM: {self.vm_name}")
        cmd = ["tart", "stop", self.vm_name]
        process = await asyncio.create_subprocess_exec(*cmd)
        await process.wait()

    async def cleanup(self) -> None:
        """
        Deletes the Tart VM.
        """
        logger.info(f"Cleaning up Tart VM: {self.vm_name}")
        await self.stop()
        cmd = ["tart", "delete", self.vm_name]
        process = await asyncio.create_subprocess_exec(*cmd)
        await process.wait()

    async def connect(self) -> None:
        """
        Connects to an already running VM.
        """
        if not self.ip_address:
            await self._wait_for_ip()
        self.host_url = f"http://{self.ip_address}:{os.getenv('BACKEND_PORT', 8000)}"

    def expose_port(self, port: int) -> str:
        """
        Exposes a port. For Tart, we assume direct IP access is enough
        or we provide the IP:Port combination.
        """
        if not self.ip_address:
            return f"http://vm-not-running:{port}"
        return f"http://{self.ip_address}:{port}"
