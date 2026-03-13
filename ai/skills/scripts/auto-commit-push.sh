#!/usr/bin/env bash
set -euo pipefail

# Auto-commit and push changes inside a target directory.
# Usage:
#   ./scripts/auto-commit-push.sh [watch_dir] [interval_seconds]
# Example:
#   ./scripts/auto-commit-push.sh /home/hom/services/knowledge/ai/skills 5

WATCH_DIR="${1:-$(pwd)}"
INTERVAL="${2:-5}"

if ! [[ "$INTERVAL" =~ ^[0-9]+$ ]] || [ "$INTERVAL" -lt 1 ]; then
  echo "[error] interval must be a positive integer (seconds)."
  exit 1
fi

if [ ! -d "$WATCH_DIR" ]; then
  echo "[error] watch_dir does not exist: $WATCH_DIR"
  exit 1
fi

if ! command -v git >/dev/null 2>&1; then
  echo "[error] git is required but not found."
  exit 1
fi

WATCH_ABS="$(cd "$WATCH_DIR" && pwd)"
REPO_ROOT="$(git -C "$WATCH_ABS" rev-parse --show-toplevel 2>/dev/null || true)"

if [ -z "$REPO_ROOT" ]; then
  echo "[error] watch_dir is not inside a git repository: $WATCH_ABS"
  exit 1
fi

# Ensure author identity exists for commits.
if ! git -C "$REPO_ROOT" config user.name >/dev/null 2>&1; then
  echo "[error] git user.name is not configured."
  echo "Run: git config user.name \"Your Name\""
  exit 1
fi
if ! git -C "$REPO_ROOT" config user.email >/dev/null 2>&1; then
  echo "[error] git user.email is not configured."
  echo "Run: git config user.email \"you@example.com\""
  exit 1
fi

REL_PATH="$(realpath --relative-to="$REPO_ROOT" "$WATCH_ABS")"
if [ "$REL_PATH" = "." ]; then
  PATHSPEC="."
else
  PATHSPEC="$REL_PATH"
fi

echo "[info] repo:       $REPO_ROOT"
echo "[info] watch path: $PATHSPEC"
echo "[info] interval:   ${INTERVAL}s"
echo "[info] Press Ctrl+C to stop."

has_changes() {
  git -C "$REPO_ROOT" status --porcelain -- "$PATHSPEC" | grep -q .
}

while true; do
  if has_changes; then
    echo "[info] changes detected. committing..."

    git -C "$REPO_ROOT" add -- "$PATHSPEC"

    # Skip if nothing staged (can happen with ignored files only).
    if git -C "$REPO_ROOT" diff --cached --quiet -- "$PATHSPEC"; then
      sleep "$INTERVAL"
      continue
    fi

    TS="$(date -u +"%Y-%m-%d %H:%M:%SZ")"
    MSG="chore(auto): sync $PATHSPEC @ $TS"

    if git -C "$REPO_ROOT" commit -m "$MSG" -- "$PATHSPEC"; then
      BRANCH="$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD)"
      if git -C "$REPO_ROOT" rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1; then
        git -C "$REPO_ROOT" push
      else
        git -C "$REPO_ROOT" push -u origin "$BRANCH"
      fi
      echo "[info] pushed: $BRANCH"
    else
      echo "[warn] commit failed. will retry on next change check."
    fi
  fi

  sleep "$INTERVAL"
done
