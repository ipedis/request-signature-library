import hmac

from httpx import Request

from request_signature_library.exception.invalid_signature_exception import InvalidSignatureException
from request_signature_library.sign_generator import SignGenerator


class Verifier:
    def __init__(self):
        self.sign_generator: SignGenerator = SignGenerator()

    def verify(self, secret: str, request: Request, root_path: str = '') -> None:
        generated_signature = self.sign_generator.generate_signature(
            secret=secret,
            request=request,
            root_path=root_path
        )

        if not hmac.compare_digest(request.headers.get('Sign', ''), generated_signature):
            raise InvalidSignatureException
