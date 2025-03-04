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

@pytest.fixture
def invalid_path_crawler():
    """
    Returns a POSIXLocalCrawler with a non-existent path.
    Useful for testing error handling when crawling invalid directories.
    """
    return POSIXLocalCrawler(root_path="/path/that/does/not/exist")
