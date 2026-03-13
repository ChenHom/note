# Auto Commit + Push

This project includes a helper script:

- `scripts/auto-commit-push.sh`

It watches a directory and automatically runs `git add`, `git commit`, and `git push` when changes are detected.

## Quick start

```bash
cd /home/hom/services/knowledge/ai/skills
./scripts/auto-commit-push.sh /home/hom/services/knowledge/ai/skills 5
```

Arguments:

1. `watch_dir` (optional): directory to watch. Default is current directory.
2. `interval_seconds` (optional): polling interval. Default is `5`.

## Before running

Make sure git identity is configured:

```bash
git config user.name "Your Name"
git config user.email "you@example.com"
```

Also ensure your repo has a valid remote named `origin`.

## Notes

- Press `Ctrl+C` to stop.
- It only commits/pushes changes inside the watched directory path.
- Commit message format:
  - `chore(auto): sync <path> @ <UTC timestamp>`
