import hmac

from httpx import Request

from request_signature_library.exception.invalid_signature_exception import InvalidSignatureException
from request_signature_library.sign_generator import SignGenerator


class TokenVerifier:
    def __init__(self):
        self.sign_generator: SignGenerator = SignGenerator()

    def verify(self, secret: str, api_key: str, request: Request) -> None:
        generated_signature = self.sign_generator.generate_token(
            key=secret,
            data=api_key
        )

        if not hmac.compare_digest(request.headers.get('Authentication', ''), generated_signature):
            raise InvalidSignatureException
