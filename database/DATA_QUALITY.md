# Transaction Data Quality

Inspected on 2026-08-25 from the supplied `transactions (2) (1).json`. The source file was not modified.

## Overview

- Records: 10,000
- Fields: `id`, `timestamp`, `merchant`, `category`, `amount`, `currency`, `status`, `payment_method`
- Distinct IDs: 9,960
- Duplicate ID groups: 40; 80 records are involved because each group contains two records
- Distinct merchants: 49
- Currency: `INR` only

## Distinct Categorical Values

- Statuses: `FAILED`, `PENDING`, `SUCCESS`
- Categories: 10 named values: `Shopping` (1,209), `Travel` (1,213), `Utilities` (1,014), `Food & Dining` (1,009), `Health` (998), `Education` (992), `Entertainment` (983), `Groceries` (979), `Fuel` (780), and `Insurance` (623). There are also 100 explicit `null` category values, 50 empty-string (`""`) category values, and 50 records where the `category` key is absent.
- Payment methods: `Credit Card`, `Debit Card`, `Netbanking`, `UPI`

## Field Completeness and Runtime Types

| Field | Missing or blank | Observed runtime types | Distinct values |
| --- | ---: | --- | ---: |
| `id` | 0 | string | 9,960 |
| `timestamp` | 0 | string, integer | 9,611 |
| `merchant` | 0 | string | 49 |
| `category` | 200 (100 `null`, 50 empty string, 50 absent) | string, null, absent | 10 named categories |
| `amount` | 0 | decimal number, string | 9,422 |
| `currency` | 0 | string | 1 |
| `status` | 0 | string | 3 |
| `payment_method` | 0 | string | 4 |

The distinct-value count for `timestamp` is lower than the record count, so timestamp values also repeat.

## Timestamp Formats

- 8,993 timestamp values are strings, and 1,007 are integers.
- 7,437 values are ISO-like strings containing `T`, including examples such as `2025-10-03T21:03:27Z`.
- 841 values are space-separated datetime strings, including examples such as `2025-09-22 21:03:27`.
- 715 values are date-only strings, including examples such as `2025-07-03`.
- 1,007 values are numeric epoch-like integers, including examples `1768265109000`, `1766522125000`, and `1781995324000`.

A date parsing and timezone policy is required during normalization.

## Amount Anomalies

- Minimum amount: `-53652.71`
- Maximum amount: `999999999`
- Arithmetic average across all records: `106966.848871`
- Negative amounts: 148
- Zero amounts: 0
- String-encoded amounts: 20

The negative values and the extreme maximum are unexpected for ordinary payment spending and require an explicit Stage 2 normalization/product policy.

## Duplicate IDs

There are 40 duplicate-ID groups, all observed as two records per group. Examples include `TXN2025000336`, `TXN2025000371`, and `TXN2025009277`. The seed process must decide whether to preserve a source occurrence key while generating a relational identifier, or otherwise define a deterministic duplicate policy.

## Normalization Notes

The source data is usable for analysis but is not uniformly typed or clean enough to insert blindly into a strict relational schema. Stage 2 should normalize timestamps and amounts, handle blank categories, make duplicate handling deterministic, and record any rejected or transformed rows. No normalization has been performed in Stage 1.

## Stage 2 Handling

- The seed pipeline preserves every source occurrence by using an internal database primary key and keeping the original ID in a non-unique indexed `source_transaction_id` column.
- Null, empty-string, and absent categories are normalized to SQL `NULL`.
- Amounts are converted to `Decimal` and stored as fixed-precision `NUMERIC(14,2)`; negative values are retained.
- ISO-like, `DD/MM/YYYY HH:MM:SS`, date-only, and epoch-millisecond timestamps are normalized to timezone-aware UTC timestamps. An unsupported value fails the seed with record context.
- Statuses are normalized to the supported uppercase values. The protected source JSON is never modified.
