import time

from httpx import Request

from request_signature_library.exception.invalid_signature_exception import InvalidSignatureException
from request_signature_library.sign_generator import SignGenerator


class Verifier:
    def __init__(self):
        self.sign_generator: SignGenerator = SignGenerator()

    def verify(self, secret: str, request: Request, root_path: str = '', max_age: float | None = None) -> None:
        """Raise InvalidSignatureException if the `Sign` header does not match.

        When `max_age` is set (seconds), the `Request-Time` header must also be a
        unix timestamp within `max_age` of now, which limits replay of captured requests.
        """
        generated_signature = self.sign_generator.generate_signature(
            secret=secret,
            request=request,
            root_path=root_path
        )

        if not self.sign_generator.matches(request.headers.get('Sign', ''), generated_signature):
            raise InvalidSignatureException

        if max_age is not None:
            self.__verify_request_time(request, max_age)

    def __verify_request_time(self, request: Request, max_age: float) -> None:
        try:
            request_time = float(request.headers.get('Request-Time', ''))
        except ValueError:
            raise InvalidSignatureException('Request-Time header is missing or invalid.')

        if abs(time.time() - request_time) > max_age:
            raise InvalidSignatureException('Request has expired.')
