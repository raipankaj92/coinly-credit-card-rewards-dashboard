# Coinly

Coinly is a planned consumer credit-card bill payment and rewards dashboard for viewing spending, earning coins on successful payments, and redeeming rewards.

## Planned Stack

- Frontend: Next.js App Router, React, TypeScript, Tailwind CSS, and Recharts for later analytics
- Backend: Python, FastAPI, Pydantic, SQLAlchemy 2.x, and a PostgreSQL-compatible psycopg driver
- Database: PostgreSQL 16+ (PostgreSQL 18 preferred)

## Planned Architecture

The frontend and backend will remain separate applications. The FastAPI backend will expose route modules that call business services, which use repositories for PostgreSQL access. The frontend will use reusable components and server-side transaction querying for pagination, filtering, sorting, and search. The transaction table will be hand-built with native HTML and CSS.

## Current Status

Stage 1 is complete: the workspace has been inspected, the source data quality has been documented, and the initial project structure and documentation have been created.

Not implemented yet: database schema, seed pipeline, API endpoints, transaction table, filters, search, sorting, analytics, rewards UI, redemption flow, tests, deployment, and demo video.

See [database/DATA_QUALITY.md](database/DATA_QUALITY.md), [ASSUMPTIONS.md](ASSUMPTIONS.md), and [DECISIONS.md](DECISIONS.md) for the current groundwork.

## Preliminary Setup

Prerequisites planned for later stages:

- Node.js with npm
- Python 3.11+
- PostgreSQL 16+

Frontend setup will use `npm install` in `frontend/`. Backend setup will use a virtual environment and `pip install -r requirements.txt` in `backend/`. Database setup and the one-command seed process will be documented when implemented in Stage 2.

## Source Inputs

The supplied PDF is the authoritative assignment specification. The supplied JSON remains unchanged and will be normalized by the Stage 2 seed pipeline.
