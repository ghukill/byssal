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

    def calculate_md5(self):
        return self.calculate_md5_from_filepath(self.uri)

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
        return cls(
            thread_uuid=str(uuid.uuid4()),
            md5=cls.calculate_md5_from_filepath(filepath),
            uri=filepath,
            created=datetime.datetime.now(),
            exists=True,
        )
