# Technical Decisions

## Next.js + TypeScript

Use Next.js with the App Router and TypeScript for the frontend. This matches the preferred framework, provides a clear application structure, and supports typed reusable UI components.

## FastAPI

Use FastAPI for the Python API. It provides typed request and response contracts, validation, sensible HTTP error handling, and a small surface suitable for the assignment.

## PostgreSQL

Use PostgreSQL as the production database because the assignment requires a real relational database and explicitly excludes SQLite, MongoDB, and in-memory storage.

## SQLAlchemy 2.x

Use SQLAlchemy 2.x for database access and schema-aligned relational queries. It keeps the data-access layer explicit while supporting PostgreSQL cleanly.

## Separated Frontend and Backend

Keep the Next.js frontend and FastAPI backend as separate applications. This preserves clear ownership boundaries and allows each side to be developed and deployed independently.

## Planned Server-Side Transaction Querying

Transaction filtering, merchant search, sorting, and pagination are planned for the backend. Server-side querying avoids shipping all approximately 10,000 rows to the browser and gives the table a predictable performance path.

## Internal Transaction Primary Key

Use an internal PostgreSQL primary key for `transactions` and store the JSON `id` as a non-unique, indexed `source_transaction_id`. The source contains duplicate IDs, so treating it as a primary key would discard or reject legitimate source occurrences.

## Decimal Financial Amounts

Store transaction amounts as `NUMERIC(14,2)` and normalize source values with Python `Decimal`. This safely accommodates the observed `999999999` maximum without binary floating-point rounding and retains negative source amounts.

## Timezone-Aware Timestamp Normalization

Store timestamps as PostgreSQL timezone-aware timestamps. ISO values preserve their offset and normalize to UTC; epoch milliseconds convert to UTC; date-only and source local-looking values are interpreted as UTC because the source provides no timezone.

## Seed-Time Source Normalization

Normalize source records in the seed pipeline rather than editing the protected JSON. The seed converts numeric strings to `Decimal`, normalizes statuses, converts null, empty, and absent categories to SQL `NULL`, and fails with a record index, source ID, and field name if a value cannot be safely normalized.

## PostgreSQL Foundation

Use SQLAlchemy metadata to create the `transactions`, `rewards`, `wallets`, and `redemptions` tables. `redemptions.reward_id` is a foreign key to `rewards.id`; the wallet is intentionally a single demo wallet because the assignment does not require authentication. The transaction internal ID uses PostgreSQL `BIGSERIAL` semantics through SQLAlchemy's `BigInteger` primary key.

## Deterministic Reseeding

The seed command validates all source records before truncating application tables. It then truncates, resets identities, inserts the full dataset and demo records, and validates counts in one PostgreSQL transaction. This prevents accumulated duplicate imports on rerun.

## Server-Side Transaction Queries

Transaction pagination, filtering, merchant/source-ID search, and sorting are implemented as SQLAlchemy PostgreSQL queries. The API counts and fetches only the requested page, rather than loading all 10,000 records into application memory. Sort columns are restricted to an allowlist to keep query construction safe and predictable.

## Atomic Redemption

Reward redemption locks the single wallet row with `SELECT ... FOR UPDATE` inside one database transaction. The balance deduction and redemption insert either both commit or both roll back, preventing concurrent requests from overspending the same wallet balance.

## Stage Scope Boundary

Stage 3 adds the backend API only. Frontend pages, transaction-table UI, charts, and deployment remain for later stages.
