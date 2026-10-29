import time

import pytest
from httpx import Request

from request_signature_library.exception.invalid_signature_exception import InvalidSignatureException
from request_signature_library.signer import Signer
from request_signature_library.verifier import Verifier


def test_request_is_verified(sample_secret):
    # Mock request
    request = Request('GET', 'https://example.com/test')

    # Instantiate Signer with mocked SignGenerator
    signer = Signer()

    # Call sign_request
    signed_request = signer.sign_request(secret=sample_secret, request=request)

    verifier = Verifier()
    verifier.verify(secret=sample_secret, request=signed_request)

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


def test_non_ascii_signature_is_rejected(sample_secret):
    request = Request('GET', 'https://example.com/test', headers=[(b'Sign', b'\xe9')])

    with pytest.raises(InvalidSignatureException):
        Verifier().verify(secret=sample_secret, request=request)


def test_root_path_is_part_of_signature(sample_secret):
    signed_request = Signer().sign_request(
        secret=sample_secret,
        request=Request('GET', 'https://example.com/api/test')
    )
    # receiving app is mounted under /api and only sees /test
    received = Request('GET', 'https://service/test', headers={'Sign': signed_request.headers['Sign']})

    Verifier().verify(secret=sample_secret, request=received, root_path='/api')
    with pytest.raises(InvalidSignatureException):
        Verifier().verify(secret=sample_secret, request=received)


def _signed_request(secret: str, request_time: str | None) -> Request:
    headers = {} if request_time is None else {'Request-Time': request_time}
    request = Request('POST', 'https://example.com/test', headers=headers)
    return Signer().sign_request(secret=secret, request=request)


def test_recent_request_is_accepted_with_max_age(sample_secret):
    request = _signed_request(sample_secret, f"{time.time()}")

    Verifier().verify(secret=sample_secret, request=request, max_age=60)


@pytest.mark.parametrize('request_time', [None, 'not-a-time', f"{time.time() - 3600}"])
def test_missing_invalid_or_expired_request_time_is_rejected(sample_secret, request_time):
    request = _signed_request(sample_secret, request_time)

    with pytest.raises(InvalidSignatureException):
        Verifier().verify(secret=sample_secret, request=request, max_age=60)


def test_request_time_is_not_checked_without_max_age(sample_secret):
    request = _signed_request(sample_secret, f"{time.time() - 3600}")

    Verifier().verify(secret=sample_secret, request=request)
