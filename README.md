# Coinly

Coinly is a planned consumer credit-card bill payment and rewards dashboard for viewing spending, earning coins on successful payments, and redeeming rewards.

## Planned Stack

- Frontend: Next.js App Router, React, TypeScript, and Tailwind CSS
- Planned analytics visualization: Recharts (not installed in Stage 1)
- Backend: Python, FastAPI, Pydantic, SQLAlchemy 2.x, and a PostgreSQL-compatible psycopg driver
- Database: PostgreSQL 16+ (PostgreSQL 18 preferred)

## Planned Architecture

The frontend and backend will remain separate applications. The FastAPI backend will expose route modules that call business services, which use repositories for PostgreSQL access. The frontend will use reusable components and server-side transaction querying for pagination, filtering, sorting, and search. The transaction table will be hand-built with native HTML and CSS.

## Current Status

Stage 2 is complete: PostgreSQL models, metadata-based schema initialization, a deterministic seed command, and focused normalization tests are available.

Not implemented yet: API endpoints, transaction table, filters, search, sorting, analytics, rewards UI, redemption flow, frontend application, deployment, and demo video.

See [database/DATA_QUALITY.md](database/DATA_QUALITY.md), [ASSUMPTIONS.md](ASSUMPTIONS.md), and [DECISIONS.md](DECISIONS.md) for the current groundwork.

## PostgreSQL Setup and Seed

Prerequisites:

- Python 3.11+
- PostgreSQL 16+

Create a PostgreSQL database, then configure `DATABASE_URL` using [`backend/.env.example`](backend/.env.example) as the format reference. Do not commit a local `.env` file or credentials.

From the project root, create a virtual environment and install the backend dependencies:

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/python -m pip install -r backend/requirements.txt
```

Set the connection URL and run the one-command schema initialization and deterministic seed:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://username:password@localhost:5432/coinly"
backend/.venv/Scripts/python backend/scripts/seed.py
```

The command creates the `transactions`, `rewards`, `wallets`, and `redemptions` tables, truncates the application tables on every rerun, resets their identities, and inserts exactly 10,000 source transactions, five rewards, and one wallet. It validates counts before committing the transaction. It never modifies the supplied JSON.

Run normalization tests from the project root with:

```powershell
backend/.venv/Scripts/python -m unittest discover -s backend/tests -p "test_*.py"
```

## Source Inputs

The supplied PDF is the authoritative assignment specification. The supplied JSON remains unchanged and will be normalized by the Stage 2 seed pipeline.
