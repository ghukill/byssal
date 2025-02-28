import pytest

from byssal.crawlers.posix import POSIXLocalCrawler
from byssal.repository import Repository

@pytest.fixture
def repository(tmp_path):
    repo = Repository(data_directory=str(tmp_path))
    repo.create_database()
    return repo

@pytest.fixture
def sample_local_fs_crawler():
    return POSIXLocalCrawler(root_path="tests/fixtures/posix/sample_local_fs")