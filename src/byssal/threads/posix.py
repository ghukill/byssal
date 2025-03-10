import datetime
import hashlib
import os.path
from pathlib import Path
import uuid

from byssal.threads.base import Thread


class POSIXLocalThread(Thread):
    thread_type: str = "posix_local"

    def check_exists(self) -> bool:
        return os.path.exists(self.uri)

    def calculate_sha256(self):
        return self.calculate_sha256_from_filepath(self.uri)
        
    def calculate_md5(self):
        return self.calculate_md5_from_filepath(self.uri)

    @classmethod
    def calculate_sha256_from_filepath(cls, filepath: str | Path) -> str:
        """Calculate SHA-256 of file.

        This is performed by reading the file in batches and incrementally updating the
        SHA-256, making this a memory safe operation for even large files.
        """
        hash_sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
        
    @classmethod
    def calculate_md5_from_filepath(cls, filepath: str | Path) -> str:
        """Calculate MD5 of file.

        This is performed by reading the file in batches and incrementally updating the
        MD5, making this a memory safe operation for even large files.
        """
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
        
    @classmethod
    def from_filepath(cls, filepath: str | Path):
        if isinstance(filepath, str):
            filepath = Path(filepath)
        return cls(
            thread_uuid=str(uuid.uuid4()),
            sha256=cls.calculate_sha256_from_filepath(filepath),
            uri=str(filepath),
            created=datetime.datetime.now(),
            exists=True,
        )

    def read(self) -> bytes:
        with open(self.uri, "rb") as f:
            return f.read()
