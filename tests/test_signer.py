from unittest.mock import MagicMock

from httpx import Request

from request_signature_library.sign_generator import SignGenerator
from request_signature_library.signer import Signer


def test_sign_header_is_added_to_request(sample_secret):
    # Mock request
    request = Request('GET', 'https://example.com/test')

    # Mock SignGenerator
    mock_sign_generator = MagicMock(SignGenerator)
    mock_sign_generator.generate_signature.return_value = 'mock-signature'

    # Instantiate Signer with mocked SignGenerator
    signer = Signer()
    signer.sign_generator = mock_sign_generator

    # Call sign_request
    signed_request = signer.sign_request(secret=sample_secret, request=request)

    # Assert the signature is added to headers
    assert signed_request.headers['Sign'] == 'mock-signature'
