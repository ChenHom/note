# Auto-activate Python virtualenv when entering a directory tree containing .venv
# Source this from ~/.zshrc, e.g.:
#   [[ -f "$HOME/.config/zsh/auto-venv.zsh" ]] && source "$HOME/.config/zsh/auto-venv.zsh"
# or directly:
#   source /path/to/auto-venv.zsh

autoload -U add-zsh-hook

typeset -g VENV_AUTO_DIR=""

_find_venv_root() {
  local cur="$PWD"
  while [[ "$cur" != "/" ]]; do
    if [[ -f "$cur/.venv/bin/activate" ]]; then
      print -r -- "$cur/.venv"
      return 0
    fi
    cur="${cur:h}"
  done
  return 1
}

_auto_venv_sync() {
  local target_venv=""
  target_venv="$(_find_venv_root 2>/dev/null || true)"

  if [[ -n "$VIRTUAL_ENV" && -n "$VENV_AUTO_DIR" ]]; then
    if [[ -z "$target_venv" || "$target_venv" != "$VENV_AUTO_DIR" ]]; then
      if typeset -f deactivate >/dev/null 2>&1; then
        deactivate
      fi
      unset VENV_AUTO_DIR
    fi
  fi

  if [[ -n "$target_venv" ]]; then
    if [[ "$VIRTUAL_ENV" != "$target_venv" ]]; then
      [[ -n "$VIRTUAL_ENV" ]] && typeset -f deactivate >/dev/null 2>&1 && deactivate || true
      source "$target_venv/bin/activate"
    fi
    typeset -g VENV_AUTO_DIR="$target_venv"
  fi
}

add-zsh-hook chpwd _auto_venv_sync
_auto_venv_sync
