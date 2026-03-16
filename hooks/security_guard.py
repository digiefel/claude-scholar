#!/usr/bin/env python3
"""PreToolUse Hook: Security guard — block catastrophic commands, confirm dangerous ones."""

import json
import os
import re
import sys
from pathlib import Path

# Read stdin
try:
    data = sys.stdin.read().strip()
    inp = json.loads(data) if data else {}
except Exception:
    inp = {}

tool_name = inp.get("tool_name", "")
cwd = inp.get("cwd", os.getcwd())
tool_input = inp.get("tool_input", {})

decision = "allow"
reason = ""
confirm_label = ""

# ── Bash command security ────────────────────────────────────────────────────
if tool_name == "Bash":
    command = tool_input.get("command", "")

    # Tier 1: Block — catastrophic, no recovery
    block_patterns = [
        (r"rm\s+-rf\s+/(\s|$)",                            "rm -rf /"),
        (r"rm\s+--no-preserve-root",                       "rm --no-preserve-root"),
        (r"dd\s+if=/dev/(zero|random)",                    "dd from /dev/zero or /dev/random"),
        (r">\s*/dev/(sd|nvme|vda)",                        "write to block device"),
        (r"mkfs\.",                                         "format filesystem"),
        (r"rm\s+-rf?\s+/(etc|usr|bin|sbin)(/|\s|$)",      "remove system directory"),
        (r"rm\s+-rf\s+/home/[^/\s]*/?(\s|$)",             "remove user home directory"),
        (r"rm\s+-rf\s+/Users/[^/\s]*/?(\s|$)",            "remove macOS user directory"),
    ]
    for pattern, label in block_patterns:
        if re.search(pattern, command):
            decision = "deny"
            reason = f"Catastrophic command detected: {label}"
            break

    # Tier 2: Confirm — dangerous but sometimes legitimate
    if decision == "allow":
        confirm_patterns = [
            (r"git\s+push\s+.*(-f|--force)",              "git push --force (overwrites remote history)"),
            (r"git\s+reset\s+--hard",                     "git reset --hard (discards all uncommitted changes)"),
            (r"git\s+clean\s+-[a-z]*f",                   "git clean -f (permanently deletes untracked files)"),
            (r"git\s+(checkout|restore)\s+\.",             "git checkout/restore . (discards all working tree changes)"),
            (r"rm\s+-[rf]",                                "rm -rf (recursive/force delete)"),
            (r"chmod\s+(-R\s+)?777",                       "chmod 777 (world-writable permissions)"),
            (r"npm\s+publish",                             "npm publish (publishes package to registry)"),
            (r"pip\s+upload|twine\s+upload",               "pip/twine upload (publishes package to PyPI)"),
            (r"docker\s+system\s+prune",                   "docker system prune (removes all unused resources)"),
            (r"DROP\s+(DATABASE|TABLE)",                   "SQL DROP (destroys database/table)"),
            (r"DELETE\s+FROM\s+(?!.*WHERE)",               "DELETE without WHERE (deletes all rows)"),
            (r"UPDATE\s+\S+\s+SET\s+(?!.*WHERE)",          "UPDATE without WHERE (updates all rows)"),
            (r"TRUNCATE\s+TABLE",                          "SQL TRUNCATE (empties entire table)"),
        ]
        for pattern, label in confirm_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                confirm_label = label
                break

# ── File write security ───────────────────────────────────────────────────────
elif tool_name in ("Write", "Edit"):
    file_path = tool_input.get("file_path", "")

    # Tier 1: Block — system paths
    sensitive_paths = [
        "/etc/", "/usr/bin/", "/usr/sbin/",
        "/bin/", "/sbin/", "/System/",
        "/dev/", "/proc/", "/sys/",
    ]
    for sp in sensitive_paths:
        if file_path.startswith(sp):
            decision = "deny"
            reason = f"Writing to system path denied: {sp}"
            break

    # Block — path traversal
    if decision == "allow" and file_path:
        home_dir = str(Path.home())
        resolved = str(Path(cwd) / file_path)
        if not resolved.startswith(cwd) and not resolved.startswith(home_dir):
            decision = "deny"
            reason = "Path traversal detected: resolved path is outside allowed directories"

    # Tier 2: Confirm — sensitive files
    if decision == "allow":
        fname = Path(file_path).name
        if fname.startswith(".env"):
            confirm_label = f".env file ({fname})"
        if not confirm_label:
            for sf in ["credentials.json", "key.pem", "key.json", "id_rsa"]:
                if fname == sf:
                    confirm_label = f"sensitive file ({sf})"
                    break
        if not confirm_label:
            for sp in [".aws/credentials", ".npmrc"]:
                if sp in file_path:
                    confirm_label = f"sensitive path ({sp})"
                    break

# ── Output ────────────────────────────────────────────────────────────────────
if decision == "deny":
    error_output = {
        "hookSpecificOutput": {"permissionDecision": "deny"},
        "systemMessage": f"🛑 Blocked: {reason}\n\nTo perform this operation, run it manually in the terminal.",
    }
    print(json.dumps(error_output), file=sys.stderr)
    sys.exit(2)
else:
    result: dict = {"continue": True}
    if confirm_label:
        result["systemMessage"] = (
            f"⚠️ CONFIRM REQUIRED: {confirm_label}\n\n"
            "You MUST ask the user for explicit confirmation before executing this operation. "
            "Do NOT proceed without user approval."
        )
    print(json.dumps(result))
    sys.exit(0)
