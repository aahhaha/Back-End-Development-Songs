# Back-End-Development-Songs

Flask REST API with MongoDB persistence, based on the official IBM template.

## Environment Setup
Python 3.12; `python -m venv .venv`, activate it, then `pip install -r requirements.txt`.
The original Linux lab setup is available in `bin/setup.sh`.

Set MONGODB_SERVICE (default localhost), MONGODB_PORT (default 27017), and optional MONGODB_USERNAME / MONGODB_PASSWORD.
Run `python app.py` to initialize seed songs once and start port 8080.
Existing MongoDB records are preserved on restart.

Endpoints: GET /health (checks database connectivity), GET /count, GET /song, GET /song/<id>, POST /song, PUT /song/<id>, DELETE /song/<id>.

## Container
`docker build -t songs .`

`docker run --rm -p 8080:8080 -e MONGODB_SERVICE=mongo songs`

The MongoDB hostname must be reachable from the application container.
