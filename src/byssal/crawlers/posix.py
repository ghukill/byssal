import logging
from pathlib import Path

from byssal.crawlers.base import Crawler
from byssal.threads.posix import POSIXLocalThread

logger = logging.getLogger(__name__)


class POSIXLocalCrawler(Crawler):
    def __init__(self, root_path: str | Path):
        self.root_path = Path(root_path).expanduser()

    def crawl(self):
        for file in self._discover_files(self.root_path):
            thread = POSIXLocalThread.from_filepath(file)
            yield thread

    @staticmethod
    def _discover_files(root_dir: str | Path):
        for path_obj in Path(root_dir).rglob("*"):
            if path_obj.is_file():
                yield path_obj
