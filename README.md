# Coinly

Coinly is a consumer credit-card bill payment and rewards dashboard. It allows users to view their spending, analyze transactions, track their coin balance, and redeem available rewards.

## Tech Stack

- **Frontend:** Next.js App Router, React, TypeScript, Tailwind CSS
- **Charts:** Recharts
- **Backend:** Python, FastAPI, Pydantic, SQLAlchemy 2.x, psycopg
- **Database:** PostgreSQL

## Architecture

The frontend and backend are separate applications.

The Next.js frontend handles the dashboard UI, transaction browsing, filters, charts, and rewards interactions. The FastAPI backend handles API requests, business logic, PostgreSQL queries, analytics, and reward redemption.

Transaction filtering, searching, sorting, and pagination are handled on the server so the browser does not need to load all 10,000 transactions at once.

The transaction table uses a native HTML table instead of a table library.

## Current Status

The Coinly dashboard is complete and has been tested locally.

Implemented features include:

- Responsive financial dashboard
- PostgreSQL-backed transaction browsing
- Server-side search, filtering, sorting, and pagination
- Transaction detail modal
- Spending analytics and charts
- Wallet balance
- Rewards catalogue
- Server-confirmed reward redemption
- Loading, empty, and error states

There is currently no deployed/hosted environment.

For more details about the data and implementation decisions, see:

- [database/DATA_QUALITY.md](database/DATA_QUALITY.md)
- [ASSUMPTIONS.md](ASSUMPTIONS.md)
- [DECISIONS.md](DECISIONS.md)

## PostgreSQL Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 16+
- Node.js 20+

Create a PostgreSQL database named `coinly` and configure `DATABASE_URL`.

Use `backend/.env.example` as the format reference. Do not commit local credentials or `.env` files.

From the project root:

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/python -m pip install -r backend/requirements.txt