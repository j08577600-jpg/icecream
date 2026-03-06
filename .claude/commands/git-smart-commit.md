Create a well-crafted git commit for the current changes:

1. Run `git status` and `git diff` to understand all changes
2. Run `ruff check src/ tests/` to verify no lint errors
3. Run `pytest` to make sure tests pass
4. If lint or tests fail, report the failures and stop — do NOT commit broken code
5. If everything passes:
   - Stage the relevant files (use specific filenames, not `git add .`)
   - Write a commit message that:
     - Has a concise subject line (imperative mood, under 72 chars)
     - Includes a body if the change is non-trivial
   - Create the commit
6. Show the final `git log --oneline -3` to confirm
