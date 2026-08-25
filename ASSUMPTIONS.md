# Assumptions

## Stage 1

- I treated the supplied `Assignment (1).pdf` as the main specification for the project.
- I treated the supplied transactions JSON as raw source data rather than assuming it was already clean. The inconsistencies found in the dataset are handled during normalization and seeding.
- I used `Coinly` as the project name since the assignment allows the candidate to choose the product name.

## Stage 2

- I kept the original transaction IDs from the JSON, including duplicate IDs. The database uses its own internal ID as the primary key.
- I converted `null`, empty-string, and missing category values to SQL `NULL`.
- I kept negative transaction amounts as they appear in the source data instead of removing or changing them.
- I used a starting wallet balance of 2,500 coins for the demo wallet. This value is a product assumption and is not calculated from the transaction data.
- I used the following reward catalogue for the demo:
  - Amazon Rs. 500 Voucher — 5,000 coins
  - Swiggy Rs. 250 Voucher — 2,750 coins
  - Myntra Rs. 500 Voucher — 5,000 coins
  - Cashback Rs. 100 — 1,200 coins
  - Flipkart Rs. 500 Voucher — 5,000 coins
- I did not calculate coin earnings from transactions during the database stage. The transaction data is stored first, while the earning rules are handled separately by the rewards/business-logic layer.
- The seed script can be run again safely. It clears and reseeds the application tables inside one PostgreSQL transaction so the database does not accumulate duplicate seed data.

## Dashboard Product Decisions

- The wallet balance shown in the dashboard comes from the API. The frontend does not calculate or optimistically change the balance during redemption.
- After a redemption attempt, the frontend relies on the API response as the source of truth. If a redemption fails, the wallet can be fetched again to make sure the displayed balance is correct.
- Analytics use the signed transaction amounts from the source data. Therefore, negative amounts reduce the corresponding totals instead of being converted to positive values.
- Selecting a category or month in the charts applies the corresponding filter to the transaction table.
- The chart totals themselves represent the complete transaction dataset unless a specific chart interaction changes the selected filter.