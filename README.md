#### Introduction

This library is useful to sign HTTP requests and verify them once received.

#### Dependencies

- [httpx](https://www.python-httpx.org/)

#### Usage

- To use this library in any repository, while running poetry on your project,
use this command.  
```commandline
poetry add git+ssh://git@github.com:docaxess/request-signature-library.git#master
```  
This will add this library to your project.
- In your project `env` file add a secret to sign the request with.
```dotenv
REQUEST_SIGNATURE=your-secret-key
```
- For now library uses timestamp, and url of the request to create hmac digest
and if digest does not match, `InvalidSignatureException` will be thrown.
- For working examples,
  - For signing request check [Orchestrator API Client](https://github.com/docaxess/pdf-orchestrator/blob/master/app/infrastructure/service/api/client.py)
  - For verification, check [Parser Middleware](https://github.com/docaxess/pdf-parser/blob/master/app/infrastructure/service/request_middleware.py)
- To run tests run this command from your poetry shell.
```commandline
poetry run pytest
```

#### TODOs

- [ ] Add url query parameters to digest if present.
- [ ] Add POST body when present to digest.
- [ ] Since all service are using FastAPI, use [starlette](https://www.starlette.io/requests/) requests instead of httpx.
- [x] ~~Create tests.~~

