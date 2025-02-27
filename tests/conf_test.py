# tests/conftest.py
import pytest


@pytest.fixture
def sample_secret():
    return "test-secret"
