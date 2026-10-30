import pytest
from httpx import Request

from request_signature_library.exception.invalid_signature_exception import InvalidSignatureException
from request_signature_library.signer import Signer
from request_signature_library.token_verifier import TokenVerifier


def test_request_is_verified(sample_secret, sample_api_key):
    signer = Signer()
    # Call sign_request
    token = signer.sign_generator.generate_token(key=sample_secret, data=sample_api_key)
    request = Request('GET', 'https://example.com/test', headers={'Authentication': token})
    verifier = TokenVerifier()
    verifier.verify(secret=sample_secret, api_key=sample_api_key, request=request)

    # Assert no exception is raised
    assert True


def test_request_is_not_verified(sample_secret, sample_api_key):
    signer = Signer()
    # Call sign_request
    token = signer.sign_generator.generate_token(key=sample_secret, data=sample_api_key)
    request = Request('GET', 'https://example.com/test', headers={'Authentication': token})
    verifier = TokenVerifier()
    verifier.verify(secret=sample_secret, api_key=sample_api_key, request=request)

    verifier = TokenVerifier()
    try:
        verifier.verify(secret='fake secret', api_key=sample_api_key, request=request)
    except InvalidSignatureException:
        assert True
    else:
        assert False


def test_non_ascii_token_is_rejected(sample_secret, sample_api_key):
    request = Request('GET', 'https://example.com/test', headers=[(b'Authentication', b'\xe9')])

    with pytest.raises(InvalidSignatureException):
        TokenVerifier().verify(secret=sample_secret, api_key=sample_api_key, request=request)
