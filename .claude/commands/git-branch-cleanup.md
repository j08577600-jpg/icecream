Clean up merged git branches:

1. Run `git branch --merged main` to find branches already merged into main
2. Show the list and ask for confirmation before deleting anything
3. Do NOT delete `main` or the current branch
4. Use `git branch -d` (safe delete) — never force delete
