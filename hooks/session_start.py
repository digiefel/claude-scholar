#!/usr/bin/env python3
"""SessionStart Hook: Display project status at session start."""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
import hook_common as common

# Read stdin
try:
    data = sys.stdin.read().strip()
    inp = json.loads(data) if data else {}
except Exception:
    inp = {}

cwd = inp.get("cwd", os.getcwd())
project_name = Path(cwd).name
home_dir = Path.home()

out = []
out.append(f"🚀 {project_name} Session started")
out.append(f"▸ Time: {common.format_datetime()}")
out.append(f"▸ Directory: {cwd}")
out.append("")

# Git status
git = common.get_git_info(cwd)
if git["is_repo"]:
    out.append(f"▸ Git branch: {git['branch']}")
    out.append("")
    if git["has_changes"]:
        out.append(f"⚠️  Uncommitted changes ({git['changes_count']} files):")
        icons = {"M": "📝", "A": "➕", "D": "❌", "R": "🔄", "??": "❓"}
        for change in git["changes"][:10]:
            status = change[:2].strip()
            fname = change[3:].strip()
            icon = icons.get(status, "•")
            out.append(f"  {icon} {fname}")
        if git["changes_count"] > 10:
            out.append(f"  ... ({git['changes_count'] - 10} more files)")
    else:
        out.append("✅ Working directory clean")
    out.append("")
else:
    out.append("▸ Git: Not a repository")
    out.append("")

# uv check
try:
    import shutil
    if shutil.which("uv"):
        out.append("📦 Package manager: uv")
    else:
        out.append("📦 Package manager: uv not found — install from https://docs.astral.sh/uv/")
    out.append("")
except Exception:
    pass

# Todos
out.append("📋 Todos:")
todo = common.get_todo_info(cwd)
if todo["found"]:
    out.append(f"  - {todo['pending']} pending / {todo['done']} completed")
    if todo["path"] and Path(todo["path"]).exists():
        try:
            content = Path(todo["path"]).read_text(encoding="utf-8")
            import re
            pending_items = re.findall(r"^[-*] \[ \].+$", content, re.MULTILINE)
            if pending_items:
                out.append("")
                out.append("  Recent todos:")
                for item in pending_items[:5]:
                    text = re.sub(r"^[-*] \[ \]\s*", "", item)[:60]
                    out.append(f"  - {text}")
        except Exception:
            pass
else:
    out.append("  No todo file found (TODO.md, docs/todo.md etc)")
out.append("")

# Enabled plugins
out.append("🔌 Enabled plugins:")
plugins = common.get_enabled_plugins(str(home_dir))
if plugins:
    for p in plugins[:5]:
        out.append(f"  - {p['name']}")
    if len(plugins) > 5:
        out.append(f"  ... and {len(plugins) - 5} more plugins")
else:
    out.append("  None")
out.append("")

# Available commands
out.append("💡 Available commands:")
commands = common.get_available_commands(str(home_dir))
if commands:
    for cmd in commands[:5]:
        desc = common.get_command_description(cmd["path"]) or f"{cmd['plugin']} command"
        desc = desc[:40] + "..." if len(desc) > 40 else desc
        out.append(f"  /{cmd['name']:<20} {desc}")
    if len(commands) > 5:
        out.append(f"  ... and {len(commands) - 5} more commands, use /help to list all")
else:
    out.append("  No commands found")

result = {"continue": True, "systemMessage": "\n".join(out)}
print(json.dumps(result))
sys.exit(0)
