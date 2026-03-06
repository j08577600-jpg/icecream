Create a pull request for the current branch:

1. Run `git log --oneline main..HEAD` to see all commits on this branch
2. Run `git diff main...HEAD --stat` to see changed files
3. Run `pytest` to confirm tests pass
4. Push the branch to remote with `git push -u origin HEAD`
5. Create a PR using `gh pr create` with:
   - A clear, concise title (under 70 chars)
   - A body with a Summary section (bullet points) and Test Plan section
6. Return the PR URL
