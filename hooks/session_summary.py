#!/usr/bin/env python3
"""SessionEnd Hook: Write work log and display change summary."""

import json
import os
import sys
import time
from datetime import datetime
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
session_id = inp.get("session_id", "unknown")
transcript_path = inp.get("transcript_path", "")
now = datetime.now()
home_dir = Path.home()
project_name = Path(cwd).name

# Create log directory
log_dir = Path(cwd) / ".claude" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

date_str = now.strftime("%Y%m%d")
log_file = log_dir / f"session-{date_str}-{session_id[:8]}.md"

git = common.get_git_info(cwd)
changes = common.get_changes_details(cwd) if git["is_repo"] else {"added": 0, "modified": 0, "deleted": 0}

# Build log content
lines = []
lines.append(f"# 📝 Work Log - {project_name}")
lines.append("")
lines.append(f"**Session ID**: {session_id}")
lines.append(f"**Time**: {common.format_datetime(now)}")
lines.append(f"**Directory**: {cwd}")
lines.append("")

lines.append("## 📊 Session Changes")
if git["is_repo"]:
    lines.append(f"**Branch**: {git['branch']}")
    lines.append("")
    lines.append("```")
    if git["has_changes"]:
        lines.extend(git["changes"])
    else:
        lines.append("No changes")
    lines.append("```")
    lines.append("")
    lines.append("| Type | Count |")
    lines.append("|------|-------|")
    lines.append(f"| Added | {changes['added']} |")
    lines.append(f"| Modified | {changes['modified']} |")
    lines.append(f"| Deleted | {changes['deleted']} |")
else:
    lines.append("Not a Git repository")
lines.append("")

# Transcript tool usage
if transcript_path and Path(transcript_path).exists():
    try:
        transcript = Path(transcript_path).read_text(encoding="utf-8")
        import re
        tool_matches = re.findall(r"Tool used: [A-Z][a-z]*", transcript)
        if tool_matches:
            from collections import Counter
            counts = Counter(t.replace("Tool used: ", "") for t in tool_matches)
            top = counts.most_common(10)
            lines.append("## 🔧 Key Operations")
            lines.append("")
            for tool, cnt in top:
                lines.append(f"| {tool} | {cnt} times |")
            lines.append("")
    except Exception:
        pass

# Next steps
lines.append("## 🎯 Next Steps")
lines.append("")
if git["has_changes"]:
    lines.append(f"- ⚠️ Uncommitted changes detected ({git['changes_count']} files)")
else:
    lines.append("- ✅ Working directory clean")

todo = common.get_todo_info(cwd)
if todo["found"]:
    lines.append(f"- Update todos: {todo['file']} ({todo['pending']} pending)")

claude_check = common.check_claude_md_update(str(home_dir))
if claude_check["needsUpdate"]:
    n = len(claude_check["changedFiles"])
    lines.append(f"- ⚠️ **CLAUDE.md memory needs updating** ({n} source files changed)")
    lines.append('  Run "/update-memory" to sync latest memory')
    lines.append("")
    lines.append("### CLAUDE.md Change Details")
    lines.append("")
    lines.append("| Type | File | Modified |")
    lines.append("|------|------|----------|")
    for f in claude_check["changedFiles"][:10]:
        lines.append(f"| {f['type']} | {f['relativePath']} | {f['mtime']} |")
    if n > 10:
        lines.append(f"| ... | {n - 10} more files | ... |")
else:
    lines.append("- ✅ CLAUDE.md memory is up to date")

lines.append("- View context snapshot: `cat .claude/session-context-*.md`")
lines.append("")

log_file.write_text("\n".join(lines), encoding="utf-8")

# Clean up logs older than 30 days
try:
    max_age = 30 * 24 * 3600
    for f in log_dir.glob("session-*.md"):
        if time.time() - f.stat().st_mtime > max_age:
            f.unlink()
except Exception:
    pass

# Build display message
msg = ["\n---"]
msg.append("✅ **Session ended** | Work log saved")
msg.append("")
msg.append("**Changes**: ")
if git["is_repo"]:
    if git["has_changes"]:
        msg[-1] += f"{git['changes_count']} files"
        msg.append("")
        msg.append("**Suggested actions**:")
        msg.append(f"- View log: cat .claude/logs/{log_file.name}")
        msg.append('- Commit code: git add . && git commit -m "feat: xxx"')
    else:
        msg[-1] += "None\n\nWorking directory clean"
else:
    msg[-1] += "Not a Git repository"

if claude_check["needsUpdate"]:
    n = len(claude_check["changedFiles"])
    msg.append("")
    msg.append("**⚠️ CLAUDE.md memory needs updating**")
    msg.append(f"- {n} source files changed")
    msg.append("- Run `/update-memory` to sync latest memory")

msg.append("\n---")

result = {"continue": True, "systemMessage": "\n".join(msg)}
print(json.dumps(result))
sys.exit(0)
