"""
Pytest configuration file for model-mix tests.

This file contains shared fixtures and configuration for all tests.
"""
import pytest
import sys
import os

# Add the parent directory to sys.path so tests can import from the main module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def pytest_configure(config):
    """Configure custom markers for pytest."""
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests (fast, isolated)"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (slower)"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running tests"
    )
