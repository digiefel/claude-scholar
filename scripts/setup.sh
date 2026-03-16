#!/usr/bin/env bash
# ============================================================
# Claude Scholar — Unified Installer
# Supports: Claude Code, Codex CLI, or both
# ============================================================
# Usage: bash scripts/setup.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

# --- Colors ---
green()  { printf "\033[32m%s\033[0m" "$1"; }
red()    { printf "\033[31m%s\033[0m" "$1"; }
yellow() { printf "\033[33m%s\033[0m" "$1"; }
bold()   { printf "\033[1m%s\033[0m" "$1"; }
info()   { echo -e "\033[1;34m[INFO]\033[0m $*"; }
warn()   { echo -e "\033[1;33m[WARN]\033[0m $*"; }
error()  { echo -e "\033[1;31m[ERROR]\033[0m $*"; exit 1; }

# ============================================================
# CLI detection
# ============================================================
detect_clis() {
  HAS_CLAUDE=false
  HAS_CODEX=false
  command -v claude >/dev/null 2>&1 && HAS_CLAUDE=true
  command -v codex  >/dev/null 2>&1 && HAS_CODEX=true
}

choose_install_target() {
  if [ "$HAS_CLAUDE" = true ] && [ "$HAS_CODEX" = true ]; then
    echo ""
    bold "Both Claude Code and Codex CLI are installed."
    echo ""
    echo "  1) Claude Code only"
    echo "  2) Codex CLI only"
    echo "  3) Both"
    echo ""
    read -rp "Select install target [1-3] (default: 3): " choice
    choice="${choice:-3}"
    case "$choice" in
      1) INSTALL_CLAUDE=true;  INSTALL_CODEX=false ;;
      2) INSTALL_CLAUDE=false; INSTALL_CODEX=true  ;;
      3) INSTALL_CLAUDE=true;  INSTALL_CODEX=true  ;;
      *) error "Invalid choice: $choice" ;;
    esac
  elif [ "$HAS_CLAUDE" = true ]; then
    INSTALL_CLAUDE=true
    INSTALL_CODEX=false
  elif [ "$HAS_CODEX" = true ]; then
    INSTALL_CLAUDE=false
    INSTALL_CODEX=true
  else
    warn "Neither 'claude' nor 'codex' found in PATH."
    echo ""
    echo "  1) Install for Claude Code anyway"
    echo "  2) Install for Codex CLI anyway"
    echo "  3) Abort"
    echo ""
    read -rp "Select [1-3] (default: 3): " choice
    choice="${choice:-3}"
    case "$choice" in
      1) INSTALL_CLAUDE=true;  INSTALL_CODEX=false ;;
      2) INSTALL_CLAUDE=false; INSTALL_CODEX=true  ;;
      *) error "Aborted." ;;
    esac
  fi
}

# ============================================================
# Claude Code install
# ============================================================
CLAUDE_COMPONENTS=(skills commands agents rules hooks plugins utils scripts CLAUDE.md AGENTS.md)

install_claude() {
  echo ""
  echo "──────────────────────────────────────────"
  bold "  Installing for Claude Code → $CLAUDE_DIR"
  echo "──────────────────────────────────────────"
  echo ""

  command -v python3 >/dev/null || error "Python 3 is required for hooks. Install it first."

  mkdir -p "$CLAUDE_DIR"
  link_components
  merge_settings

  echo ""
  info "Claude Code install complete. Restart Claude Code CLI to activate."
}

# Symlink a single file: create parent dirs, back up conflicts, replace stale links
link_file() {
  local src="$1"
  local dst="$2"

  mkdir -p "$(dirname "$dst")"

  # Already correct — skip
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    return
  fi

  # Real file/dir exists — back it up
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    mv "$dst" "${dst}.bak"
    warn "Backed up: $(basename "$dst") → $(basename "$dst").bak"
  fi

  # Stale symlink — remove
  [ -L "$dst" ] && rm "$dst"

  ln -s "$src" "$dst"
}

# Recursively symlink all files under src/ into dst/, creating dirs as needed
link_tree() {
  local src="$1"
  local dst="$2"
  local count=0

  while IFS= read -r -d '' file; do
    local rel="${file#"$src"/}"
    link_file "$file" "$dst/$rel"
    count=$((count + 1))
  done < <(find "$src" -type f -print0)

  echo "$count"
}

link_components() {
  local total=0
  for comp in "${CLAUDE_COMPONENTS[@]}"; do
    local src="$SRC_DIR/$comp"

    [ -e "$src" ] || { warn "Skipping $comp (not found in repo)."; continue; }

    if [ -f "$src" ]; then
      link_file "$src" "$CLAUDE_DIR/$comp"
      info "Linked file: $comp"
      total=$((total + 1))
    elif [ -d "$src" ]; then
      local n
      n=$(link_tree "$src" "$CLAUDE_DIR/$comp")
      info "Linked dir:  $comp/ ($n files)"
      total=$((total + n))
    fi
  done
  info "Total: $total symlinks created/verified"
}

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

  python3 - "$target" "$template" << 'PYEOF' || { warn "Auto-merge failed. Please manually copy settings from settings.json.template."; return 0; }
import json, sys
target, template = sys.argv[1], sys.argv[2]
with open(target) as f: existing = json.load(f)
with open(template) as f: tmpl = json.load(f)
if 'hooks' in tmpl: existing['hooks'] = tmpl['hooks']
if 'mcpServers' in tmpl:
    existing.setdefault('mcpServers', {})
    for k, v in tmpl['mcpServers'].items():
        existing['mcpServers'].setdefault(k, v)
if 'enabledPlugins' in tmpl:
    existing.setdefault('enabledPlugins', {})
    for k, v in tmpl['enabledPlugins'].items():
        existing['enabledPlugins'].setdefault(k, v)
with open(target, 'w') as f: json.dump(existing, f, indent=2); f.write('\n')
PYEOF

  info "Merged hooks/mcpServers/enabledPlugins into settings.json."
}

# ============================================================
# Codex CLI install
# ============================================================

# --- State flags ---
SKIP_PROVIDER=false
SKIP_AUTH=false
PROVIDER_NAME=""
PROVIDER_URL=""
MODEL=""
API_KEY=""

# --- Provider presets ---
declare -a PRESET_NAMES=("openai" "custom")
declare -a PRESET_LABELS=("OpenAI (official)" "Custom provider")
declare -a PRESET_URLS=("https://api.openai.com/v1" "")
declare -a PRESET_MODELS=("gpt-4o" "")

install_codex() {
  echo ""
  echo "──────────────────────────────────────────"
  bold "  Installing for Codex CLI → $CODEX_HOME"
  echo "──────────────────────────────────────────"
  echo ""

  mkdir -p "$CODEX_HOME"

  detect_existing_codex
  choose_provider
  configure_api_key
  generate_config
  write_auth
  copy_components_codex
  configure_mcp

  echo ""
  info "Codex CLI install complete."
  echo ""
  echo "  Config:  $CODEX_HOME/config.toml"
  echo "  Auth:    $CODEX_HOME/auth.json"
  echo "  Skills:  $CODEX_HOME/skills/"
  echo "  Agents:  $CODEX_HOME/agents/"
  echo ""
  echo "  Run $(bold 'codex') to start."
}

detect_existing_codex() {
  if [ -f "$CODEX_HOME/config.toml" ]; then
    info "Existing config.toml found at $CODEX_HOME/config.toml"
    local cur_model cur_provider
    cur_model=$(grep '^model ' "$CODEX_HOME/config.toml" 2>/dev/null | head -1 | sed 's/.*= *"//;s/".*//' || true)
    cur_provider=$(grep '^model_provider ' "$CODEX_HOME/config.toml" 2>/dev/null | head -1 | sed 's/.*= *"//;s/".*//' || true)
    [ -n "$cur_model" ]    && info "  Current model: $cur_model"
    [ -n "$cur_provider" ] && info "  Current provider: $cur_provider"
    echo ""
    read -rp "Keep existing provider/model config? [Y/n]: " keep_config
    if [ "$keep_config" != "n" ] && [ "$keep_config" != "N" ]; then
      SKIP_PROVIDER=true
      info "Keeping existing provider/model configuration"
    fi
  fi

  if [ -f "$CODEX_HOME/auth.json" ]; then
    local existing_key
    existing_key=$(grep -o '"OPENAI_API_KEY"[[:space:]]*:[[:space:]]*"[^"]*"' "$CODEX_HOME/auth.json" 2>/dev/null | sed 's/.*: *"//;s/"$//' || true)
    if [ -n "$existing_key" ]; then
      local masked="${existing_key:0:8}...${existing_key: -4}"
      info "Existing API key found: $masked"
      read -rp "Keep existing API key? [Y/n]: " keep_key
      if [ "$keep_key" != "n" ] && [ "$keep_key" != "N" ]; then
        SKIP_AUTH=true
        info "Keeping existing API key"
      fi
    fi
  fi
}

choose_provider() {
  if [ "$SKIP_PROVIDER" = true ]; then
    return
  fi

  echo ""
  bold "Select API provider:"
  echo ""
  for i in "${!PRESET_LABELS[@]}"; do
    echo "  $((i+1))) ${PRESET_LABELS[$i]}"
  done
  echo ""

  local choice
  read -rp "Enter choice [1-2] (default: 1): " choice
  choice="${choice:-1}"

  local idx=$((choice - 1))
  if [ "$idx" -lt 0 ] || [ "$idx" -ge "${#PRESET_NAMES[@]}" ]; then
    error "Invalid choice: $choice"
  fi

  PROVIDER_NAME="${PRESET_NAMES[$idx]}"
  PROVIDER_URL="${PRESET_URLS[$idx]}"
  MODEL="${PRESET_MODELS[$idx]}"

  if [ "$PROVIDER_NAME" = "custom" ]; then
    read -rp "Provider name: " PROVIDER_NAME
    read -rp "Base URL: " PROVIDER_URL
    read -rp "Model name: " MODEL
  else
    echo ""
    read -rp "Model name (default: $MODEL): " input_model
    MODEL="${input_model:-$MODEL}"
  fi

  info "Provider: $PROVIDER_NAME | URL: $PROVIDER_URL | Model: $MODEL"
}

configure_api_key() {
  if [ "$SKIP_AUTH" = true ]; then
    return
  fi

  echo ""
  read -rp "Enter API key (OPENAI_API_KEY, or press Enter to skip): " API_KEY
  if [ -z "$API_KEY" ]; then
    warn "No API key set. Make sure OPENAI_API_KEY is in your environment."
    SKIP_AUTH=true
  fi
}

generate_config() {
  local template="$SRC_DIR/config.toml"
  local target="$CODEX_HOME/config.toml"

  [ -f "$template" ] || error "Template config.toml not found at $template"

  if [ "$SKIP_PROVIDER" = true ]; then
    merge_scholar_config "$target" "$template"
  else
    if [ -f "$target" ]; then
      cp "$target" "${target}.bak"
      info "Backed up config.toml → config.toml.bak"
    fi
    sed -e "s|__MODEL__|$MODEL|g" \
        -e "s|__PROVIDER_NAME__|$PROVIDER_NAME|g" \
        -e "s|__PROVIDER_URL__|$PROVIDER_URL|g" \
        "$template" > "$target"
    info "Generated config.toml (model=$MODEL, provider=$PROVIDER_NAME)"
  fi
}

merge_scholar_config() {
  local target="$1"
  local template="$2"
  local added=0

  cp "$target" "${target}.bak"
  info "Backed up config.toml → config.toml.bak"

  if ! grep -q '^\[features\]' "$target" 2>/dev/null; then
    cat >> "$target" << 'FEATURES'

# ============================================================
# Features (added by Claude Scholar)
# ============================================================
[features]
multi_agent = true
memories = true
skill_approval = true
FEATURES
    added=$((added + 1))
  fi

  if ! grep -q '\[mcp_servers\.zotero\]' "$target" 2>/dev/null; then
    cat >> "$target" << 'MCP'

# ============================================================
# MCP Servers (added by Claude Scholar)
# ============================================================
[mcp_servers.zotero]
command = "zotero-mcp"
args = ["serve"]
enabled = false
[mcp_servers.zotero.env]
ZOTERO_LOCAL = "true"
NO_PROXY = "localhost,127.0.0.1"
MCP
    added=$((added + 1))
  fi

  if ! grep -q '^\[agents\.' "$target" 2>/dev/null; then
    sed -n '/^# --- Research Workflow/,$ p' "$template" >> "$target"
    added=$((added + 1))
  fi

  if [ "$added" -gt 0 ]; then
    info "Merged $added Scholar section(s) into existing config.toml"
  else
    info "Config already has all Scholar sections, no changes needed"
  fi
}

write_auth() {
  if [ "$SKIP_AUTH" = true ]; then
    return
  fi

  local target="$CODEX_HOME/auth.json"
  [ -f "$target" ] && cp "$target" "${target}.bak"
  cat > "$target" << EOF
{
  "OPENAI_API_KEY": "$API_KEY"
}
EOF
  chmod 600 "$target"
  info "Wrote auth.json (permissions: 600)"
}

copy_components_codex() {
  if [ -d "$SRC_DIR/skills" ]; then
    mkdir -p "$CODEX_HOME/skills"
    cp -r "$SRC_DIR/skills/." "$CODEX_HOME/skills/"
    local count
    count=$(ls -d "$CODEX_HOME/skills"/*/ 2>/dev/null | wc -l | tr -d ' ')
    info "Synced skills: $count total"
  fi

  if [ -d "$SRC_DIR/agents" ]; then
    mkdir -p "$CODEX_HOME/agents"
    cp -r "$SRC_DIR/agents/." "$CODEX_HOME/agents/"
    local count
    count=$(ls -d "$CODEX_HOME/agents"/*/ 2>/dev/null | wc -l | tr -d ' ')
    info "Synced agents: $count total"
  fi

  if [ -f "$SRC_DIR/AGENTS.md" ]; then
    [ -f "$CODEX_HOME/AGENTS.md" ] && cp "$CODEX_HOME/AGENTS.md" "$CODEX_HOME/AGENTS.md.bak"
    cp "$SRC_DIR/AGENTS.md" "$CODEX_HOME/AGENTS.md"
    info "Synced AGENTS.md"
  fi

  if [ -d "$SRC_DIR/utils" ]; then
    mkdir -p "$CODEX_HOME/utils"
    cp -r "$SRC_DIR/utils/." "$CODEX_HOME/utils/"
    info "Synced utils/"
  fi
}

configure_mcp() {
  if grep -q 'enabled = true' "$CODEX_HOME/config.toml" 2>/dev/null; then
    info "Zotero MCP already enabled"
    return
  fi

  echo ""
  read -rp "Enable Zotero MCP server? [y/N]: " enable_zotero
  if [ "$enable_zotero" = "y" ] || [ "$enable_zotero" = "Y" ]; then
    sed -i.tmp 's/enabled = false/enabled = true/' "$CODEX_HOME/config.toml"
    rm -f "$CODEX_HOME/config.toml.tmp"
    info "Zotero MCP enabled"
    if ! command -v zotero-mcp >/dev/null 2>&1; then
      warn "zotero-mcp not found. Install: uv tool install git+https://github.com/Galaxy-Dawn/zotero-mcp.git"
    fi
  fi
}

# ============================================================
# Main
# ============================================================
main() {
  echo ""
  echo "╔══════════════════════════════════════╗"
  echo "║      Claude Scholar Installer        ║"
  echo "╚══════════════════════════════════════╝"
  echo ""

  command -v git >/dev/null || error "Git is required."

  info "Source: $SRC_DIR"

  detect_clis
  choose_install_target

  [ "$INSTALL_CLAUDE" = true ] && install_claude
  [ "$INSTALL_CODEX"  = true ] && install_codex

  echo ""
  echo "============================================================"
  info "All done!"
  echo "============================================================"
}

main "$@"
