import hmac
import hashlib
from httpx import Request


class SignGenerator:
    def hmac_digest(self, data: str, key: str) -> str:
        key_encoded = bytes(key, 'utf-8')
        data_encoded = bytes(data, 'utf-8')

        h = hmac.new(key_encoded, data_encoded, hashlib.sha512)

        return h.hexdigest()

    def generate_signature(self, secret: str, request: Request) -> str:
        path = request.url.path
        path = path.replace('//', '/')

        # if request.url.query:
        #     params = request.url.query
        #     path = path + "?" + params.decode('utf-8') if isinstance(params, bytes) else params

        data = f"{request.method.upper()}{path}{request.headers.get('Request-Time', '')}"

        # if request.:
        #     data = f"{data}{request.content}"

        return self.hmac_digest(data, secret)

    def generate_token(self, key: str, data: str) -> str:
        return self.hmac_digest(data=data, key=key)
