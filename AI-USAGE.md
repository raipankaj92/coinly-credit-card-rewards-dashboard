# AI Usage

AI tools were used as a development aid throughout the project, mainly for:

- Understanding the assignment requirements and supplied dataset.
- Exploring implementation approaches before coding.
- Drafting parts of the project structure and initial implementation.
- Reviewing API, database, and frontend code for potential issues.
- Debugging errors during local development.
- Generating test cases and helping interpret test failures.
- Checking implementation details during final integration testing.

I reviewed the generated suggestions before using them and validated the implementation locally through tests, API requests, database checks, and manual UI testing. AI was used to reduce repetitive work and speed up investigation, but implementation decisions and final changes were reviewed by me.

## AI Output We Rejected or Corrected

1. **PostgreSQL connection debugging**

   During local integration testing, an AI-assisted diagnosis initially focused on the database credential/environment setup. After checking the actual backend traceback, I found that the issue was the SQLAlchemy URL format: the application expected `postgresql+psycopg://`, while the environment value used `postgresql://`. I corrected the environment value and verified that `/api/wallet` returned `200` with the expected 2,500-coin balance.

2. **Next.js development server cleanup**

   An initial AI-assisted cleanup approach attempted to remove the `.next` directory automatically, but Windows returned an `ENOTEMPTY` error because generated files were still in use. I stopped the running Node processes, removed the generated directory manually, restarted Next.js, and verified that the dashboard returned `200` and rendered correctly.
