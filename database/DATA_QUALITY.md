## Timestamp Formats

- 8,993 timestamp values are strings, and 1,007 are integers.
- 7,437 values are ISO-like strings containing `T`, including examples such as `2025-10-03T21:03:27Z`.
- 841 values are space-separated datetime strings, including examples such as `2025-09-22 21:03:27`.
- 715 values are date-only strings, including examples such as `2025-07-03`.
- 1,007 values are epoch-millisecond integers, including examples such as `1768265109000`, `1766522125000`, and `1781995324000`.

The mixed timestamp formats needed a single parsing and timezone policy before the data could be stored consistently.

## Amount Anomalies

- Minimum amount: `-53652.71`
- Maximum amount: `999999999`
- Arithmetic average across all records: `106966.848871`
- Negative amounts: 148
- Zero amounts: 0
- String-encoded amounts: 20

The negative values and unusually large maximum required an explicit normalization decision. Negative amounts are retained rather than silently converted because they may represent refunds or other adjustments in the source data.

## Duplicate IDs

There are 40 duplicate-ID groups, all observed as two records per group. Examples include `TXN2025000336`, `TXN2025000371`, and `TXN2025009277`.

Because the source IDs are not unique, the database uses its own internal primary key while preserving the original JSON ID as `source_transaction_id`.

## Stage 1 Assessment

The source data is usable for analysis but is not uniformly typed or clean enough to insert directly into a strict relational schema.

The main issues identified were mixed timestamp and amount types, missing categories, duplicate source IDs, negative amounts, and the unusually large maximum amount.

These findings were used to define the normalization approach implemented in Stage 2. The original JSON file was not modified.

## How the Data Is Handled in Stage 2

- The seed pipeline preserves every source occurrence by using an internal database primary key and keeping the original ID in a non-unique indexed `source_transaction_id` column.
- Null, empty-string, and absent categories are normalized to SQL `NULL`.
- Amounts are converted to `Decimal` and stored as fixed-precision `NUMERIC(14,2)`; negative values are retained.
- ISO-like, `DD/MM/YYYY HH:MM:SS`, date-only, and epoch-millisecond timestamps are normalized to timezone-aware UTC timestamps. An unsupported value fails the seed with the record index, source ID, field, and reason.
- Statuses are normalized to the supported uppercase values.
- The protected source JSON is never modified.