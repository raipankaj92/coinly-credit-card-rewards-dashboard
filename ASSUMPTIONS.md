# Assumptions

## Stage 1

- The supplied `Assignment (1).pdf` is the authoritative specification.
- The supplied transactions JSON is treated as source input, not as a clean production database export. Its inconsistencies will be handled by the Stage 2 normalization and seed work.
- Coinly is a working project name; the assignment permits the candidate to choose the product name.

## Stage 2

- Source transaction IDs are retained, including duplicates. An internal database ID is the transaction primary key.
- Null, empty-string, and absent categories are all stored as SQL `NULL`.
- Negative source amounts are retained unchanged; later business rules will determine their user-facing interpretation.
- The initial demo wallet balance is 2,500 coins. This is a product assumption, not a balance derived from source transactions.
- The demo catalogue is: Amazon Rs. 500 Voucher (5,000 coins), Swiggy Rs. 250 Voucher (2,750 coins), Myntra Rs. 500 Voucher (5,000 coins), Cashback Rs. 100 (1,200 coins), and Flipkart Rs. 500 Voucher (5,000 coins). These costs are product assumptions.
- Coin earning for successful transactions is deferred to a later business-rule/API stage; this stage stores only the foundation required for it.
- Rerunning the seed command deterministically truncates and reseeds the application tables inside one PostgreSQL transaction.

## To Decide Later

- The exact per-transaction coin cap and earning formula, because the brief requires a cap but does not specify its value.
- The final transaction pagination and detail-view interaction.
