# Agent Instructions

This file is the short operational guide for agents working in this repository.
For project overview and architecture, read [README.md](./README.md). For the
full contributor workflow, read [DEVELOPMENT.md](./DEVELOPMENT.md).

## Repository Map

- `backend/`: FastAPI service. Entry point: `main.py`; app code in `src/`;
  tests in `tests/`; migrations in `alembic/`.
- `frontend/`: Vue 3 + Vite dashboard. Source in `src/`; generated API client
  in `src/api/`; unit tests under `src/__tests__/`.
- `firmware/`: Raspberry Pi Pico W firmware built with CMake and the Pico SDK.
- `scripts/`: Face registration, recognition, training, validation, and API
  generation utilities.
- `docs/`: Contributor documentation, including commit and pre-commit rules.

## Common Commands

Run commands from the relevant subdirectory unless noted.

```bash
# Backend
cd backend
uv sync --dev
uv run fastapi dev main.py
uv run alembic upgrade head
uv run pytest tests -v
uv run pyright main.py src tests alembic

# Frontend
cd frontend
pnpm install
pnpm dev
pnpm build
pnpm test:unit
pnpm lint
pnpm format

# Firmware
cd firmware
cmake -B build
cmake --build build
```

When backend API contracts change, regenerate and commit the frontend client:

```bash
bash scripts/generate-api.sh
```

## Tooling Expectations

- Backend Python uses Ruff for lint/format, pyright for type checking, pytest for
  tests, and Alembic for migrations.
- Frontend TypeScript/Vue uses ESLint, oxlint, oxfmt, vue-tsc, Vitest, and
  Histoire.
- Run focused checks for the area you changed. Before review, run:

```bash
uvx pre-commit run --all-files
```

Install hooks once per clone:

```bash
uvx pre-commit install --install-hooks
```

See [docs/pre-commit.md](./docs/pre-commit.md) for hook details.

## Commit Rules

Commits must use:

```text
type(scope): subject
type: subject
```

Allowed types include `feat`, `fix`, `docs`, `test`, `refactor`, `chore`,
`ci`, `build`, `perf`, and `style`. Use a lowercase imperative subject and keep
each commit focused on one logical change.

Prefer stable scopes such as `auth`, `users`, `core`, `face`, `frontend`,
`firmware`, `docs`, `tooling`, `ci`, `config`, `deps`, and `tests`. If a change
spans unrelated areas, split it into separate commits when practical.

Use `fix` for user-visible or workflow-breaking defects, including broken local
tooling behavior. Use `docs` for documentation-only changes. Use `ci` only for
CI workflow behavior.

See [docs/commit-msg.md](./docs/commit-msg.md) for the complete rules.

## Security Notes

Do not commit secrets, local databases, captured face data, generated firmware
outputs, or environment files. Create `backend/.env` from
`backend/.env.example`; `SECRET_KEY` is required and must be at least 32
characters.
