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

## Dashboard Product Decisions

- The dashboard displays the seeded wallet balance as the source of truth. It does not calculate coins client-side or optimistically subtract them during redemption.
- All reward eligibility is based on the last balance confirmed by the API; a failed redemption triggers a wallet refetch where possible.
- Analytics sum signed transaction amounts. Negative amounts therefore reduce category, monthly, and overall totals, preserving the financial meaning of refunds/adjustments in the supplied data.
- Category and monthly chart selections apply the corresponding table filter. Aggregate chart values otherwise represent the full transaction set, not the currently filtered table subset.
