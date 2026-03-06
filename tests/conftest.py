"""Shared fixtures for tests."""

import sqlite3
from pathlib import Path

import pytest

from icecream.models import get_connection


@pytest.fixture
def conn(tmp_path: Path) -> sqlite3.Connection:
    """Provide a fresh in-memory-like DB connection for each test."""
    db_path = tmp_path / "test.db"
    return get_connection(db_path)
