import pytest


@pytest.fixture
def sample_secret():
    return "test-secret"


@pytest.fixture
def sample_api_key():
    return "test-api-key"
