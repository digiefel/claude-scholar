"""Shared utility library for Claude Scholar hooks."""

import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path


def _run(cmd, cwd=None):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        return r.stdout
    except Exception:
        return ""


def get_git_info(cwd):
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=cwd, capture_output=True, check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {"is_repo": False, "branch": "unknown",
                "changes_count": 0, "has_changes": False, "changes": []}

    branch = _run(["git", "branch", "--show-current"], cwd=cwd).strip() or "unknown"
    changes_raw = _run(["git", "status", "--porcelain"], cwd=cwd)
    changes = [l for l in changes_raw.strip().splitlines() if l]
    return {
        "is_repo": True,
        "branch": branch,
        "changes_count": len(changes),
        "has_changes": bool(changes),
        "changes": changes,
    }


def get_todo_info(cwd):
    candidates = [
        Path(cwd) / "docs" / "todo.md",
        Path(cwd) / "TODO.md",
        Path(cwd) / ".claude" / "todos.md",
        Path(cwd) / "TODO",
        Path(cwd) / "notes" / "todo.md",
    ]
    for fp in candidates:
        if fp.exists():
            try:
                content = fp.read_text(encoding="utf-8")
                total = len(re.findall(r"^[-*] \[[ x]\]", content, re.MULTILINE | re.IGNORECASE))
                done = len(re.findall(r"^[-*] \[x\]", content, re.MULTILINE | re.IGNORECASE))
                return {"found": True, "file": fp.name, "path": str(fp),
                        "total": total, "done": done, "pending": total - done}
            except Exception:
                continue
    return {"found": False, "file": None, "path": None, "total": 0, "done": 0, "pending": 0}


def get_changes_details(cwd):
    added = modified = deleted = 0

    def parse_name_status(output):
        nonlocal added, modified, deleted
        for line in output.strip().splitlines():
            if not line:
                continue
            s = line[0]
            if s == "A":
                added += 1
            elif s == "M":
                modified += 1
            elif s == "D":
                deleted += 1

    parse_name_status(_run(["git", "diff", "--name-status"], cwd=cwd))
    parse_name_status(_run(["git", "diff", "--cached", "--name-status"], cwd=cwd))

    for line in _run(["git", "status", "--porcelain"], cwd=cwd).strip().splitlines():
        if line.startswith("??"):
            added += 1

    return {"added": added, "modified": modified, "deleted": deleted}


def analyze_changes_by_type(cwd):
    git_info = get_git_info(cwd)
    empty = {"test_files": 0, "docs_files": 0, "sql_files": 0,
             "config_files": 0, "service_files": 0}
    if not git_info["is_repo"] or not git_info["has_changes"]:
        return empty

    files = [c[3:].strip() for c in git_info["changes"]]
    counts = {k: 0 for k in empty}
    for f in files:
        if re.search(r"(?:^|[/\\])tests?[/\\]|[/\\._]test[_.]|\.test\.|_test\.", f, re.IGNORECASE):
            counts["test_files"] += 1
        if re.search(r"\.(md|txt|rst)$", f, re.IGNORECASE):
            counts["docs_files"] += 1
        if re.search(r"\.sql$", f, re.IGNORECASE):
            counts["sql_files"] += 1
        if re.search(r"\.(json|yaml|yml|toml|ini|conf)$", f, re.IGNORECASE):
            counts["config_files"] += 1
        if re.search(r"(service|controller)", f, re.IGNORECASE):
            counts["service_files"] += 1
    return counts


def detect_temp_files(cwd):
    cwd_path = Path(cwd)
    temp_files = []
    git_info = get_git_info(cwd)

    if git_info["is_repo"]:
        for change in git_info["changes"]:
            if change.startswith("??"):
                f = change[3:].strip()
                if re.search(r"plan|draft|tmp|temp|scratch", f, re.IGNORECASE):
                    temp_files.append(f)

    for temp_dir in ["plan", "docs/plans", ".claude/temp", "tmp", "temp"]:
        dir_path = cwd_path / temp_dir
        if dir_path.exists():
            for fp in _get_all_files(dir_path):
                temp_files.append(str(fp.relative_to(cwd_path)))

    return {"files": temp_files, "count": len(temp_files)}


def _get_all_files(dir_path):
    result = []
    for item in Path(dir_path).iterdir():
        if item.is_dir():
            result.extend(_get_all_files(item))
        else:
            result.append(item)
    return result


def get_all_files(dir_path):
    return [str(f) for f in _get_all_files(dir_path)]


def generate_recommendations(cwd, git_info):
    recs = []
    if git_info["is_repo"] and git_info["has_changes"]:
        details = get_changes_details(cwd)
        types = analyze_changes_by_type(cwd)
        if details["added"] > 0 or details["modified"] > 0:
            recs.append('git add . && git commit -m "feat: xxx"')
        if types["test_files"] > 0:
            recs.append("Run test suite to verify changes")
        if types["docs_files"] > 0:
            recs.append("Check documentation is in sync with code")
        if types["sql_files"] > 0:
            recs.append("Update all related database scripts")
        if types["config_files"] > 0:
            recs.append("Check if environment variables need updating")
        if types["service_files"] > 0:
            recs.append("Update API documentation")

    todo = get_todo_info(cwd)
    if todo["found"] and todo["pending"] > 0:
        recs.append(f"Check todos: {todo['file']} ({todo['pending']} items remaining)")
    if not git_info["is_repo"]:
        recs.append("Remember to back up important files to a git repo or cloud storage")
    return recs


def get_enabled_plugins(home_dir):
    settings_file = Path(home_dir) / ".claude" / "settings.json"
    if not settings_file.exists():
        return []
    try:
        settings = json.loads(settings_file.read_text(encoding="utf-8"))
        enabled = settings.get("enabledPlugins", {})
        return [{"id": pid, "name": pid.split("@")[0]}
                for pid, on in enabled.items() if on]
    except Exception:
        return []


def get_available_commands(home_dir):
    commands_dir = Path(home_dir) / ".claude" / "commands"
    if not commands_dir.exists():
        return []
    return [
        {"plugin": "local", "name": f.stem, "path": str(f)}
        for f in commands_dir.iterdir()
        if f.suffix == ".md"
    ]


def get_command_description(cmd_path):
    try:
        content = Path(cmd_path).read_text(encoding="utf-8")
        lines = content.splitlines()
        in_frontmatter = False
        for line in lines:
            if line.strip() == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    break
                continue
            if in_frontmatter and line.strip().startswith("description:"):
                m = re.match(r'description:\s*["\']?(.+?)["\']?\s*$', line)
                if m:
                    return m.group(1).strip()
        for line in lines:
            m = re.match(r'^#+\s*(.+)$', line)
            if m:
                return m.group(1).strip()[:50]
    except Exception:
        pass
    return ""


def collect_local_skills(home_dir):
    skills_dir = Path(home_dir) / ".claude" / "skills"
    if not skills_dir.exists():
        return []
    skills = []
    for d in skills_dir.iterdir():
        if not d.is_dir():
            continue
        description = ""
        skill_file = d / "skill.md"
        if skill_file.exists():
            try:
                m = re.search(r"^description:\s*(.+)$",
                              skill_file.read_text(encoding="utf-8"),
                              re.MULTILINE | re.IGNORECASE)
                if m:
                    description = m.group(1).strip()
            except Exception:
                pass
        skills.append({"name": d.name, "description": description, "type": "local"})
    return skills


def collect_plugin_skills(home_dir):
    plugins_cache = Path(home_dir) / ".claude" / "plugins" / "cache"
    if not plugins_cache.exists():
        return []
    skills = []
    for marketplace in plugins_cache.iterdir():
        if not marketplace.is_dir() or marketplace.name == "ai-research-skills":
            continue
        for plugin in marketplace.iterdir():
            if not plugin.is_dir() or plugin.name.startswith("."):
                continue
            versions = sorted([v.name for v in plugin.iterdir() if v.is_dir()], reverse=True)
            if not versions:
                continue
            skills_dir = plugin / versions[0] / "skills"
            if skills_dir.exists():
                for s in skills_dir.iterdir():
                    if s.is_dir():
                        skills.append({
                            "name": f"{plugin.name}:{s.name}",
                            "plugin": plugin.name,
                            "skill": s.name,
                            "type": "plugin",
                        })
    return skills


def format_datetime(dt=None):
    dt = dt or datetime.now()
    return dt.strftime("%Y/%m/%d %H:%M:%S")


def check_claude_md_update(home_dir):
    home = Path(home_dir)
    claude_md = home / ".claude" / "CLAUDE.md"
    if not claude_md.exists():
        return {"needsUpdate": False, "reason": "CLAUDE.md not found"}

    claude_md_mtime = claude_md.stat().st_mtime_ns // 1_000_000  # ms

    last_sync_path = home / ".claude" / ".last-memory-sync"
    if last_sync_path.exists():
        try:
            last_sync_mtime = int(last_sync_path.read_text().strip())
        except Exception:
            last_sync_mtime = claude_md_mtime
    else:
        last_sync_mtime = claude_md_mtime

    reference_ms = max(claude_md_mtime, last_sync_mtime)

    source_dirs = [
        (home / ".claude" / "skills",   re.compile(r"skill\.md$"),       "skill"),
        (home / ".claude" / "commands", re.compile(r"\.md$"),             "command"),
        (home / ".claude" / "agents",   re.compile(r"\.md$"),             "agent"),
        (home / ".claude" / "hooks",    re.compile(r"\.(py|json)$"),      "hook"),
    ]

    changed_files = []
    stats = {"skills": 0, "commands": 0, "agents": 0, "hooks": 0}

    for src_dir, pattern, ftype in source_dirs:
        if not src_dir.exists():
            continue
        key = ftype + "s"
        for fp in _get_all_files(src_dir):
            if not pattern.search(fp.name):
                continue
            stats[key] = stats.get(key, 0) + 1
            mtime_ms = fp.stat().st_mtime_ns // 1_000_000
            if mtime_ms > reference_ms:
                changed_files.append({
                    "path": str(fp),
                    "type": ftype,
                    "relativePath": str(fp.relative_to(home)),
                    "mtime": datetime.fromtimestamp(mtime_ms / 1000).strftime("%m/%d/%Y, %H:%M:%S"),
                })

    return {
        "needsUpdate": bool(changed_files),
        "changedFiles": changed_files,
        "stats": stats,
    }


def update_sync_timestamp(home_dir):
    last_sync_path = Path(home_dir) / ".claude" / ".last-memory-sync"
    try:
        import time
        last_sync_path.write_text(str(int(time.time() * 1000)), encoding="utf-8")
    except Exception:
        pass
