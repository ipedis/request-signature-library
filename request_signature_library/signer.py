from httpx import Request

from request_signature_library.sign_generator import SignGenerator


class Signer:
    def __init__(self):
        self.sign_generator: SignGenerator = SignGenerator()

    def sign_request(self, secret: str, request: Request):
        signature = self.sign_generator.generate_signature(
            secret=secret,
            request=request
        )
        request.headers.update({"Sign": signature})

        return request
