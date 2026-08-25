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

## Stage 1 Scope Boundary

Stage 1 establishes structure and documents facts only. The relational schema, seed script, routes, services, repositories, and UI will be implemented incrementally in later stages.
