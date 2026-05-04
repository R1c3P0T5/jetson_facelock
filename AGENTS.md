# Repository Guidelines

## Project Structure & Module Organization

This Jetson face-lock system is split by runtime target:

- `backend/`: FastAPI service. Entry point: `backend/main.py`; domain code: `backend/src/{auth,users,core}`; tests: `backend/tests/`; migrations: `backend/alembic/`.
- `frontend/`: Vue 3 + Vite app. Source: `frontend/src/`; public assets: `frontend/public/`; unit tests: `frontend/src/__tests__/`.
- `firmware/`: Raspberry Pi Pico W firmware using CMake and the Pico SDK.
- `scripts/`: Face registration/training utilities and validation scripts.
- `docs/`: Contributor documentation.

## Build, Test, and Development Commands

For Codex shell commands, prefix with `rtk`; Claude Code may proxy this through its local hook.

- Backend setup: `cd backend && uv sync --dev`
- Backend server: `cd backend && uv run fastapi dev main.py`
- Backend migrations: `cd backend && uv run alembic upgrade head`
- Backend tests: `cd backend && uv run pytest tests -v`
- Backend type check: `cd backend && uv run pyright`
- Frontend setup: `cd frontend && pnpm install`
- Frontend dev server: `cd frontend && pnpm dev`
- Frontend build/type check: `cd frontend && pnpm build`
- Frontend unit tests: `cd frontend && pnpm test:unit`
- Frontend lint/format: `cd frontend && pnpm lint && pnpm format`
- Firmware build: `cd firmware && cmake -B build && cmake --build build` (requires `PICO_SDK_PATH` set)

## Coding Style & Naming Conventions

Python targets 3.10+ and is formatted/linted with Ruff. Keep backend modules snake_case and grouped by domain. Vue/TypeScript uses ESLint, oxlint, and oxfmt; keep components PascalCase.

## Testing Guidelines

Backend tests use pytest, pytest-asyncio, httpx, and temporary database fixtures. Name files `test_*.py` in `backend/tests/`. Frontend tests use Vitest and Vue Test Utils with `*.spec.ts` under `frontend/src/__tests__/`. Run the relevant suite before opening a PR.

## Commit & Pull Request Guidelines

Commits must follow `type(scope): subject` or `type: subject`, using types such as `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `build`, `perf`, or `style`. Subjects start with a lowercase imperative verb and describe one change, for example `feat(frontend): add login form`. See [docs/commit-msg.md](docs/commit-msg.md) for scope and body guidance.

Before submitting a PR, run `uvx pre-commit run --all-files` or focused checks. See [docs/pre-commit.md](docs/pre-commit.md) for hook setup. PR descriptions should summarize behavior changes, list verification commands, link issues, and include screenshots for UI changes.

## Security & Configuration Tips

Create `backend/.env` from `backend/.env.example`. `SECRET_KEY` is required and must be at least 32 characters. Do not commit local databases, secrets, generated firmware outputs, or environment files.
