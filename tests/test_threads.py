import hashlib
import os
from pathlib import Path

import pytest

from byssal.threads.posix import POSIXLocalThread


def test_calculate_sha256_from_filepath():
    """Test that SHA-256 calculation works correctly."""
    # Get path to a test fixture file
    fixture_path = Path("tests/fixtures/posix/sample_files/fruit.txt")
    
    # Calculate SHA-256 using our implementation
    calculated_hash = POSIXLocalThread.calculate_sha256_from_filepath(fixture_path)
    
    # Calculate expected SHA-256 using hashlib directly
    expected_hash = hashlib.sha256()
    with open(fixture_path, "rb") as f:
        expected_hash.update(f.read())
    expected_hash = expected_hash.hexdigest()
    
    # Verify the hashes match
    assert calculated_hash == expected_hash


def test_thread_from_filepath():
    """Test creating a Thread from a filepath."""
    fixture_path = Path("tests/fixtures/posix/sample_files/fruit.txt")
    
    # Create thread from filepath
    thread = POSIXLocalThread.from_filepath(fixture_path)
    
    # Verify thread properties
    assert thread.thread_type == "posix_local"
    assert thread.uri == str(fixture_path)
    assert thread.exists is True
    
    # Verify SHA-256 hash is correct
    expected_hash = hashlib.sha256()
    with open(fixture_path, "rb") as f:
        expected_hash.update(f.read())
    expected_hash = expected_hash.hexdigest()
    
    assert thread.sha256 == expected_hash
