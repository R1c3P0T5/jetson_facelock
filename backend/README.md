# Jetson Facelock Backend

User authentication and face recognition API for Jetson devices.

The backend provides FastAPI routes for user registration, JWT login,
authenticated profile access, admin user management, and face embedding
metadata updates.

## Setup

Install development dependencies from the `backend/` directory:

```bash
uv sync --dev
```

Create a local environment file:

```bash
cp .env.example .env
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Set the generated value as `SECRET_KEY` in `.env`.

Initialize or migrate the database:

```bash
uv run alembic upgrade head
```

Start the development server:

```bash
uv run fastapi dev main.py
```

Equivalent uvicorn command:

```bash
uv run uvicorn main:app --reload
```

Run tests:

```bash
uv run pytest tests -v
```

## Environment Variables

`SECRET_KEY` is required and must be at least 32 characters. Generate it with:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

`DATABASE_URL` defaults to:

```text
sqlite+aiosqlite:///./jetson_facelock.db
```

The default points to a SQLite database in the `backend/` directory. Tests
override this with isolated temporary databases and do not use the production or
development database.

`DEBUG` controls debug mode and defaults to `False`.

`JWT_ALGORITHM` defaults to `HS256`.

`JWT_EXPIRATION_HOURS` defaults to `24`.

Optional default admin seed:

```env
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_PASSWORD=<set-a-strong-admin-password>
DEFAULT_ADMIN_FULL_NAME=Administrator
DEFAULT_ADMIN_EMAIL=admin@example.com
```

`DEFAULT_ADMIN_USERNAME` and `DEFAULT_ADMIN_PASSWORD` must be set together.
`DEFAULT_ADMIN_FULL_NAME` and `DEFAULT_ADMIN_EMAIL` are optional. When enabled,
the app lifespan creates the admin user on startup if that username does not
already exist. Existing users are not overwritten.

## Project Structure

```text
backend/
|-- main.py              # FastAPI app factory and lifespan integration
|-- src/
|   |-- auth/            # Registration, login, JWT utilities, auth dependencies
|   |-- users/           # User model, schemas, service layer, CRUD routes
|   `-- core/            # Settings, database session setup, exceptions, security
|-- tests/               # Unit and integration tests
|-- alembic/             # Database migrations
|-- .env.example         # Environment template
`-- pyproject.toml       # Dependencies and tool configuration
```

## API Documentation

Run the development server and open the generated API documentation:

```text
http://localhost:8000/docs
```

FastAPI also exposes ReDoc at:

```text
http://localhost:8000/redoc
```

The OpenAPI schema is generated from the active application code, so use these
pages as the source of truth for available endpoints, request bodies, response
schemas, and authentication requirements.

## Development

Add dependencies:

```bash
uv add package-name
```

Create a migration after model changes:

```bash
uv run alembic revision --autogenerate -m "describe change"
```

Apply migrations:

```bash
uv run alembic upgrade head
```

Run the full test suite:

```bash
uv run pytest tests -v
```

Run type checking:

```bash
uv run pyright main.py src tests alembic
```

Run coverage:

```bash
uv run pytest tests --cov=src --cov-report=term-missing --cov-report=html
```

## Tech Stack

- FastAPI with the standard extras
- SQLModel and SQLAlchemy async sessions
- SQLite with `aiosqlite` for local development
- Alembic migrations
- Argon2id password hashing through `argon2-cffi`
- JWT authentication through `python-jose`
- pytest, pytest-asyncio, httpx, pyright, and ruff

## Troubleshooting

If settings fail with `SECRET_KEY not set or too short`, create `backend/.env`
from `.env.example` and set a generated secret value.

If tests create database files in the project directory, check that tests are
running through the provided `tests/conftest.py` fixtures. The default test
fixtures set `DATABASE_URL` to a per-test temporary database path.

If the server cannot import `main`, run commands from the `backend/` directory.
The app object is `main:app`.

If a database schema looks stale, run:

```bash
uv run alembic upgrade head
```
