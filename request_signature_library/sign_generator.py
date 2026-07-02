import hmac
import hashlib
from httpx import Request


class SignGenerator:
    def hmac_digest(self, data: str, key: str) -> str:
        key_encoded = bytes(key, 'utf-8')
        data_encoded = bytes(data, 'utf-8')

        h = hmac.new(key_encoded, data_encoded, hashlib.sha512)

        return h.hexdigest()

    def generate_signature(self, secret: str, request: Request, root_path: str = '') -> str:
        path = root_path + request.url.path
        path = path.replace('//', '/')

        data = f"{request.method.upper()}{path}{request.headers.get('Request-Time', '')}"

        return self.hmac_digest(data, secret)

    def generate_token(self, key: str, data: str) -> str:
        return self.hmac_digest(data=data, key=key)
