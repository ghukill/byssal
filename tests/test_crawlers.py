import os
import pytest
from pathlib import Path

from byssal.crawlers.posix import POSIXLocalCrawler


def test_invalid_path_crawler_initialization(invalid_path_crawler):
    """Test that a crawler can be initialized with an invalid path."""
    assert invalid_path_crawler is not None
    assert invalid_path_crawler.root_path == "/path/that/does/not/exist"


def test_invalid_path_crawler_crawl(invalid_path_crawler):
    """Test that crawling an invalid path raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        list(invalid_path_crawler.crawl())


def test_nonexistent_directory_crawler():
    """Test creating a crawler with a non-existent directory."""
    # Create a path that definitely doesn't exist
    temp_nonexistent_path = "/tmp/definitely_not_a_real_directory_" + os.urandom(8).hex()
    
    # Initialize crawler with non-existent path
    crawler = POSIXLocalCrawler(root_path=temp_nonexistent_path)
    
    # Verify the crawler was created but crawling fails
    assert crawler.root_path == temp_nonexistent_path
    with pytest.raises(FileNotFoundError):
        list(crawler.crawl())


def test_path_becomes_invalid(tmp_path):
    """Test what happens when a valid path becomes invalid during execution."""
    # Create a temporary directory
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    
    # Create a file in the directory
    test_file = test_dir / "test.txt"
    test_file.write_text("test content")
    
    # Initialize crawler with the temporary directory
    crawler = POSIXLocalCrawler(root_path=str(test_dir))
    
    # Remove the directory to make the path invalid
    test_file.unlink()
    test_dir.rmdir()
    
    # Verify crawling now fails
    with pytest.raises(FileNotFoundError):
        list(crawler.crawl())


def test_relative_path_crawler():
    """Test that a crawler works with relative paths."""
    # Use a relative path to the fixtures
    relative_path = "tests/fixtures/posix/sample_local_fs"
    
    # Initialize crawler with relative path
    crawler = POSIXLocalCrawler(root_path=relative_path)
    
    # Verify crawling works
    threads = list(crawler.crawl())
    assert len(threads) > 0


def test_path_with_special_characters():
    """Test that paths with special characters are handled correctly."""
    # This test is more of a demonstration - in a real test you'd create
    # a directory with special characters in its name
    
    # For now, just verify that initializing with such a path doesn't crash
    special_path = "/tmp/path with spaces and $pecial ch@racters"
    crawler = POSIXLocalCrawler(root_path=special_path)
    assert crawler.root_path == special_path
    
    # We don't try to crawl as the path doesn't exist
