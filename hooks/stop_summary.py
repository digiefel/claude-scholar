#!/usr/bin/env python3
"""Stop Hook: Display Git status and temp file summary."""

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

msg = ["\n---", "✅ Session ended", ""]

git = common.get_git_info(cwd)
if git["is_repo"]:
    msg.append("📁 Git repository")
    msg.append(f"  Branch: {git['branch']}")
    if git["has_changes"]:
        details = common.get_changes_details(cwd)
        msg.append("  Changes:")
        if details["added"]:
            msg.append(f"    Added: {details['added']} files")
        if details["modified"]:
            msg.append(f"    Modified: {details['modified']} files")
        if details["deleted"]:
            msg.append(f"    Deleted: {details['deleted']} files")
    else:
        msg.append("  Status: clean")
else:
    msg.append("📁 Not a Git repository")

msg.append("")

# Temp files
temp = common.detect_temp_files(cwd)
if temp["count"] > 0:
    msg.append(f"🧹 Temp files: {temp['count']}")
    grouped: dict = {}
    for f in temp["files"]:
        d = str(Path(f).parent)
        grouped.setdefault(d, []).append(Path(f).name)
    for d, files in grouped.items():
        msg.append(f"  📂 {d}/ ({len(files)})")
        for fname in files[:3]:
            msg.append(f"    • {fname}")
        if len(files) > 3:
            msg.append(f"    ... and {len(files) - 3} more")
else:
    msg.append("✅ No temp files")

msg.append("---")

result = {"continue": True, "systemMessage": "\n".join(msg)}
print(json.dumps(result))
sys.exit(0)
