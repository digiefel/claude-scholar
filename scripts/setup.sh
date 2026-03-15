#!/usr/bin/env bash
set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
COMPONENTS=(skills commands agents rules hooks plugins utils scripts CLAUDE.md)

info()  { echo -e "\033[1;34m[INFO]\033[0m $*"; }
warn()  { echo -e "\033[1;33m[WARN]\033[0m $*"; }
error() { echo -e "\033[1;31m[ERROR]\033[0m $*"; exit 1; }

check_deps() {
  command -v git  >/dev/null || error "Git is required. Install it first."
  command -v node >/dev/null || error "Node.js is required (hooks depend on it). Install it first."
}

# Merge hooks, mcpServers, enabledPlugins from template into existing settings.json
merge_settings() {
  local template="$SRC_DIR/settings.json.template"
  local target="$CLAUDE_DIR/settings.json"

  [ -f "$template" ] || return 0

  if [ ! -f "$target" ]; then
    cp "$template" "$target"
    info "Created settings.json from template."
    info "  → Edit $target to add your API keys."
    return 0
  fi

  cp "$target" "${target}.bak"
  info "Backed up settings.json → settings.json.bak"

  node -e "
    const fs = require('fs');
    const existing = JSON.parse(fs.readFileSync('$target', 'utf8'));
    const template = JSON.parse(fs.readFileSync('$template', 'utf8'));
    if (template.hooks) existing.hooks = template.hooks;
    if (template.mcpServers) {
      existing.mcpServers = existing.mcpServers || {};
      for (const [k, v] of Object.entries(template.mcpServers)) {
        if (!existing.mcpServers[k]) existing.mcpServers[k] = v;
      }
    }
    if (template.enabledPlugins) {
      existing.enabledPlugins = existing.enabledPlugins || {};
      for (const [k, v] of Object.entries(template.enabledPlugins)) {
        if (!(k in existing.enabledPlugins)) existing.enabledPlugins[k] = v;
      }
    }
    fs.writeFileSync('$target', JSON.stringify(existing, null, 2) + '\n');
  " || { warn "Auto-merge failed. Please manually copy settings from settings.json.template."; return 0; }

  info "Merged hooks/mcpServers/enabledPlugins into settings.json."
}

# Symlink each component from the repo into ~/.claude
link_components() {
  mkdir -p "$CLAUDE_DIR"
  for comp in "${COMPONENTS[@]}"; do
    local src="$SRC_DIR/$comp"
    local dst="$CLAUDE_DIR/$comp"

    [ -e "$src" ] || { warn "Skipping $comp (not found in repo)."; continue; }

    # Already a correct symlink — nothing to do
    if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
      info "Already linked: $comp"
      continue
    fi

    # Existing real file or directory — back it up
    if [ -e "$dst" ] && [ ! -L "$dst" ]; then
      mv "$dst" "${dst}.bak"
      warn "Backed up existing $comp → ${comp}.bak"
    fi

    # Stale symlink — remove it
    [ -L "$dst" ] && rm "$dst"

    ln -s "$src" "$dst"
    info "Linked: $comp → $src"
  done
}

main() {
  echo ""
  echo "╔══════════════════════════════════════╗"
  echo "║       Claude Scholar Installer       ║"
  echo "╚══════════════════════════════════════╝"
  echo ""

  check_deps

  info "Installing from: $SRC_DIR"
  link_components
  merge_settings
  info "Your existing env/permissions are preserved."

  echo ""
  info "Done! Restart Claude Code CLI to activate."
  echo ""
}

main "$@"
