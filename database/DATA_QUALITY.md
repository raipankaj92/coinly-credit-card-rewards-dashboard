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
- Categories: 11 named values plus 200 blank/missing values: `Education`, `Entertainment`, `Food & Dining`, `Fuel`, `Groceries`, `Health`, `Insurance`, `Shopping`, `Travel`, `Utilities`
- Payment methods: `Credit Card`, `Debit Card`, `Netbanking`, `UPI`

## Field Completeness and Runtime Types

| Field | Missing or blank | Observed runtime types | Distinct values |
| --- | ---: | --- | ---: |
| `id` | 0 | string | 9,960 |
| `timestamp` | 0 | string, integer | 9,611 |
| `merchant` | 0 | string | 49 |
| `category` | 200 | string | 11 non-blank |
| `amount` | 0 | decimal number, string | 9,422 |
| `currency` | 0 | string | 1 |
| `status` | 0 | string | 3 |
| `payment_method` | 0 | string | 4 |

The distinct-value count for `timestamp` is lower than the record count, so timestamp values also repeat.

## Timestamp Formats

- 7,437 values are ISO-like strings containing `T`, including examples such as `2025-10-03T21:03:27Z`.
- 841 values are space-separated or date-only strings containing a space or no time separator, including examples such as `2025-07-03` and `2025-09-22`.
- 1,722 values are in the `other` bucket. This includes 1,007 integer timestamp values, with examples `1768265109000`, `1766522125000`, and `1781995324000`, plus values that do not match the simple text classification above.

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
