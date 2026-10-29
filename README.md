# request-signature-library

Small Python library to sign HTTP requests with a shared secret (HMAC-SHA512) and verify them on the receiving service. It is meant for authenticating calls between services that share a secret.

## Requirements

- Python 3.12+
- [httpx](https://www.python-httpx.org/)

## Installation

The package is installed from git, pinned to a tag:

```bash
uv add "request-signature-library @ git+https://github.com/ipedis/request-signature-library.git@v2.0.0"
# or
pip install "git+https://github.com/ipedis/request-signature-library.git@v2.0.0"
```

Every service that signs or verifies requests must share the same secret, for example through an environment variable:

```dotenv
SIGNATURE_SECRET=your-secret-key
```

Use a long random value (e.g. `python -c "import secrets; print(secrets.token_hex(32))"`).

## Usage

### Signing a request (client side)

```python
import time

import httpx
from request_signature_library.signer import Signer

request = httpx.Request(
    "POST",
    "https://api.example.com/orders",
    json={"order_id": 42},
    headers={"Request-Time": f"{time.time()}"},
)
signed_request = Signer().sign_request(secret=SIGNATURE_SECRET, request=request)
httpx.Client().send(signed_request)
```

`sign_request` adds a `Sign` header. The `Request-Time` header is set by the caller: the library includes it in the signature but does not add it.

### Verifying a request (server side)

```python
from request_signature_library.exception.invalid_signature_exception import InvalidSignatureException
from request_signature_library.verifier import Verifier

verifier = Verifier()

try:
    verifier.verify(secret=SIGNATURE_SECRET, request=request, max_age=300)
except InvalidSignatureException:
    ...  # reject with 401/403
```

- `request` can be an `httpx.Request` or a Starlette/FastAPI `Request`: only `method`, `url.path` and `headers` are read.
- `root_path`: if the receiving app is mounted under a prefix (FastAPI `root_path`) and therefore sees a shorter `url.path` than the one the client signed, pass that prefix so both sides compute the same path.
- `max_age` (seconds, optional): also require `Request-Time` to be a unix timestamp no older (or further in the future) than `max_age`. Without it, the timestamp is not checked.

### API token

`TokenVerifier` checks a static token instead of a per-request signature: the client sends `Authentication: HMAC-SHA512(secret, api_key)`.

```python
from request_signature_library.sign_generator import SignGenerator
from request_signature_library.token_verifier import TokenVerifier

token = SignGenerator().generate_token(key=secret, data=api_key)        # client
TokenVerifier().verify(secret=secret, api_key=api_key, request=request)  # server
```

## What is signed

```
HMAC-SHA512(secret, METHOD + path + Request-Time)
```

`path` is `root_path + url.path` with `//` replaced by `/`. Comparison is done in constant time.

Security limits to keep in mind:

- The query string and the body are **not** signed: someone able to intercept a request can change them without invalidating the signature. Use TLS between services.
- Without `max_age`, a captured request can be replayed indefinitely.
- The API token is static: anyone who sees it can reuse it until the secret or the API key changes.

## Development

```bash
uv sync                  # creates .venv with dev dependencies
uv run pytest            # run the tests
uv run pytest tests/test_verifier.py::test_request_is_verified
uv export --no-hashes --no-emit-project -q > /tmp/req.txt && uv run pip-audit -r /tmp/req.txt
```

Without uv, with Python 3.12+ and pip 25.1+ (needed for `--group`):

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e . --group dev
.venv/bin/pytest
```

With only Docker (no Python installed):

```bash
docker run --rm -v "$PWD":/app -w /app -e UV_PROJECT_ENVIRONMENT=/tmp/venv \
  ghcr.io/astral-sh/uv:0.13.6-python3.12-trixie-slim uv run --locked pytest
```

## License

Apache License 2.0, see [LICENSE](LICENSE).
