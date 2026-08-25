# Technical Decisions

## Next.js + TypeScript

I used Next.js with the App Router and TypeScript for the frontend. It gives me a structured frontend setup and lets me keep the dashboard components and API responses type-safe.

## FastAPI

I used FastAPI for the backend because the project is Python-based and the framework makes it straightforward to define API routes, validate inputs, and return proper HTTP responses.

## PostgreSQL

I used PostgreSQL as the database because the assignment requires a relational database and does not allow SQLite, MongoDB, or in-memory storage.

## SQLAlchemy 2.x

I used SQLAlchemy 2.x for database access and ORM models. This keeps the database models and queries organized while working cleanly with PostgreSQL.

## Separate Frontend and Backend

I kept the Next.js frontend and FastAPI backend as separate applications. The frontend is responsible for the UI, while the backend handles database access, business logic, filtering, analytics, and rewards.

## Server-Side Transaction Queries

I implemented transaction filtering, searching, sorting, and pagination on the backend instead of loading all 10,000 transactions into the browser. The API only returns the page of data that the user requests.

## Internal Transaction ID

The source JSON contains duplicate transaction IDs, so I did not use the source `id` as the database primary key. I use an internal database ID as the primary key and keep the original JSON ID as `source_transaction_id` with an index.

This allows duplicate source records to be preserved instead of being rejected during seeding.

## Financial Amounts

I store transaction amounts using PostgreSQL `NUMERIC(14,2)` and normalize them with Python `Decimal`. I chose this instead of floating-point values because these are financial amounts and should not be affected by floating-point rounding.

I also kept negative amounts because they exist in the supplied source data rather than silently changing them.

## Timestamp Normalization

The source contains several timestamp formats, including ISO timestamps, date/time strings, date-only values, and epoch milliseconds.

I normalize these during seeding and store them as timezone-aware PostgreSQL timestamps. Values that contain an explicit timezone are converted to UTC. Values without timezone information are treated as UTC because the source does not provide a timezone.

## Source Data Normalization

I kept the original JSON unchanged and perform normalization during the seed process.

The seed pipeline converts numeric amount strings to `Decimal`, normalizes statuses, and converts null, empty, or missing categories to SQL `NULL`.

If a required value cannot be safely normalized, the seed process stops and reports the record index, source ID, and field that caused the problem.

## Database Tables

I created four main tables:

- `transactions`
- `rewards`
- `wallets`
- `redemptions`

The `redemptions.reward_id` column references `rewards.id`.

The assignment does not require user authentication, so I kept a single demo wallet rather than adding unnecessary user/account tables.

## Deterministic Seeding

The seed script validates the source data before changing the database. It then clears the application tables, resets their identities, inserts the normalized transactions and demo reward data, and validates the resulting counts.

This makes it possible to rerun the seed without accumulating duplicate data.

## Safe Transaction Queries

The transaction API performs filtering, searching, sorting, and pagination directly in PostgreSQL through SQLAlchemy.

The API uses an allowlist for sortable columns instead of accepting arbitrary column names from the request.

## Atomic Reward Redemption

For redemption, I lock the wallet row using `SELECT ... FOR UPDATE` inside a database transaction.

The balance deduction and redemption record are created in the same transaction. This means either both operations succeed or neither is saved, which prevents the wallet from being deducted without a corresponding redemption record.

## Frontend State

I used local React state for the dashboard instead of adding Redux or another global state library. The application is primarily a single dashboard, so global state would add unnecessary complexity.

The frontend uses a typed API client for backend communication. Transaction requests are also cancelled when filters change, and search requests use a 300ms debounce.

## Analytics

I created separate analytics endpoints for the dashboard summary, category spending, and monthly spending.

The aggregation is performed in PostgreSQL using `GROUP BY` queries instead of sending all 10,000 transactions to the browser and calculating everything there.

## Responsive Transaction Table

I kept the transaction table as a normal semantic HTML table. On smaller screens, the table's container can scroll horizontally so that the financial columns remain readable without making the entire page wider than the viewport.
