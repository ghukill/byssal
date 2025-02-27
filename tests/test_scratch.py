from byssal.repository import Repository
from byssal.crawlers.posix import POSIXLocalCrawler


def test_repo_run_crawlers():
    repo = Repository("/tmp/byssal.sqlite")
    posix_crawler = POSIXLocalCrawler(root_path="tests/fixtures/posix/sample_local_fs")
    repo.run_crawlers(crawlers=[posix_crawler])
    threads = list(repo.run_crawlers(crawlers=[posix_crawler]))
    assert len(threads) == 5
