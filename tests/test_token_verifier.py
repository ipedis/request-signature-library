# tests/test_signer.py
from unittest.mock import MagicMock

from httpx import Request

from request_signature_library.exception.invalid_signature_exception import InvalidSignatureException
from request_signature_library.sign_generator import SignGenerator
from request_signature_library.signer import Signer
from request_signature_library.token_verifier import TokenVerifier
from request_signature_library.verifier import Verifier
from tests.conf_test import sample_secret


def test_request_is_verified(sample_secret):
    # Mock request
    request = Request('GET', 'https://example.com/test')

    # Instantiate Signer with mocked SignGenerator
    signer = Signer()

    # Call sign_request
    signed_request = signer.sign_request(secret=sample_secret, request=request)

    verifier = TokenVerifier()
    verifier.verify(secret=sample_secret, api_key='', request=signed_request)

    # Assert no exception is raised
    assert True


def test_request_is_not_verified(sample_secret):
    # Mock request
    request = Request('GET', 'https://example.com/test')

    # Instantiate Signer with mocked SignGenerator
    signer = Signer()

    # Call sign_request
    signed_request = signer.sign_request(secret=sample_secret, request=request)

    verifier = Verifier()
    try:
        verifier.verify(secret='fake secret', request=signed_request)
    except InvalidSignatureException:
        assert True
    else:
        assert False
