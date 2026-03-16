#!/usr/bin/env python3
"""UserPromptSubmit Hook: Force skill evaluation against the user's prompt."""

import json
import os
import re
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

user_prompt = inp.get("user_prompt", "")

# Skip slash commands (but not file paths like /Users/...)
if user_prompt.startswith("/"):
    rest = user_prompt[1:]
    if "/" not in rest:
        print(json.dumps({"continue": True}))
        sys.exit(0)

home_dir = Path.home()


def collect_skills():
    skills = []
    # Local skills
    skills_dir = home_dir / ".claude" / "skills"
    if skills_dir.exists():
        skills.extend(d.name for d in skills_dir.iterdir() if d.is_dir())
    # Plugin skills
    plugins_cache = home_dir / ".claude" / "plugins" / "cache"
    if plugins_cache.exists():
        for marketplace in plugins_cache.iterdir():
            if not marketplace.is_dir():
                continue
            for plugin in marketplace.iterdir():
                if not plugin.is_dir() or plugin.name.startswith("."):
                    continue
                versions = sorted(
                    [v.name for v in plugin.iterdir() if v.is_dir()], reverse=True
                )
                if not versions:
                    continue
                sd = plugin / versions[0] / "skills"
                if sd.exists():
                    skills.extend(
                        f"{plugin.name}:{s.name}"
                        for s in sd.iterdir() if s.is_dir()
                    )
    return sorted(set(skills))


def categorize_skills(skills):
    categories = {
        "Research & Writing": re.compile(
            r"research|paper|writing|citation|review-response|rebuttal|"
            r"post-acceptance|doc-coauthoring|latex|daily-paper|ml-paper|"
            r"results-analysis|brainstorm"
        ),
        "Development": re.compile(
            r"coding|git|code-review|bug|architecture|verification|tdd|"
            r"uv-package|webapp-testing|kaggle|driven-development|"
            r"development-branch|planning|dispatching|executing|using-superpowers"
        ),
        "Plugin Dev": re.compile(
            r"skill-|command-|hook-|mcp-|agent-identifier|command-name"
        ),
        "Design & UI": re.compile(
            r"frontend|ui-ux|web-design|canvas|brand|theme|"
            r"algorithmic-art|slack-gif|figma"
        ),
        "Documents": re.compile(
            r"docx|xlsx|pptx|pdf|internal-comms|web-artifacts"
        ),
    }
    grouped = {cat: [] for cat in categories}
    grouped["Other"] = []
    for skill in skills:
        matched = False
        for cat, pattern in categories.items():
            if pattern.search(skill):
                grouped[cat].append(skill)
                matched = True
                break
        if not matched:
            grouped["Other"].append(skill)
    return grouped


KEYWORD_SKILL_MAP = [
    (re.compile(r"\b(git|github|commit|push|pull|merge|rebase|branch|tag|stash|cherry.?pick|develop|master|main)\b", re.I), ["git-workflow"]),
    (re.compile(r"\b(debug|bug|error|broken|failing|traceback|exception)\b", re.I), ["bug-detective"]),
    (re.compile(r"\b(tdd|test.?driven)\b", re.I), ["superpowers:test-driven-development"]),
    (re.compile(r"\b(code.?review|review code)\b", re.I), ["code-review-excellence"]),
    (re.compile(r"\b(paper|manuscript|draft)\b", re.I), ["ml-paper-writing"]),
    (re.compile(r"\b(research|idea|brainstorm)\b", re.I), ["research-ideation"]),
    (re.compile(r"\b(rebuttal|reviewer|response to reviewer)\b", re.I), ["review-response"]),
    (re.compile(r"\b(frontend|landing.?page|dashboard)\b", re.I), ["frontend-design"]),
    (re.compile(r"\b(create|write|develop|improve).*skill\b", re.I), ["skill-development"]),
    (re.compile(r"\b(create|write|develop).*hook\b", re.I), ["hook-development"]),
    (re.compile(r"\b(create|write|develop).*command|slash.*command\b", re.I), ["command-development"]),
    (re.compile(r"\b(create|write|develop).*agent\b", re.I), ["agent-identifier"]),
    (re.compile(r"\b(mcp)\b|mcp.*server", re.I), ["mcp-integration"]),
    (re.compile(r"\b(architecture|factory|registry)\b", re.I), ["architecture-design"]),
    (re.compile(r"\b(uv|pip|package.*manager|venv)\b", re.I), ["uv-package-manager"]),
    (re.compile(r"\b(kaggle|competition)\b", re.I), ["kaggle-learner"]),
    (re.compile(r"\b(citation|reference.*check)\b", re.I), ["citation-verification"]),
    (re.compile(r"\b(latex.*template|overleaf)\b", re.I), ["latex-conference-template-organizer"]),
    (re.compile(r"\b(ablation|results.*analysis)\b", re.I), ["results-analysis"]),
    (re.compile(r"\b(poster|presentation|promote)\b", re.I), ["post-acceptance"]),
    (re.compile(r"\b(plan|planning)\b", re.I), ["planning-with-files"]),
    (re.compile(r"\b(verify|verification)\b", re.I), ["verification-loop"]),
    (re.compile(r"\b(self.?review)\b", re.I), ["paper-self-review"]),
    (re.compile(r"\b(anti.?ai|humanize)\b", re.I), ["writing-anti-ai"]),
    (re.compile(r"\b(implement|write code|add feature|modify|refactor)\b", re.I), ["daily-coding"]),
]


def suggest_skills(prompt):
    suggested = []
    for pattern, skills in KEYWORD_SKILL_MAP:
        if pattern.search(prompt):
            suggested.extend(skills)
    return list(dict.fromkeys(suggested))  # deduplicate, preserve order


skill_list = collect_skills()
skill_groups = categorize_skills(skill_list)
suggested = suggest_skills(user_prompt)

grouped_display = "\n".join(
    f"[{cat}] {', '.join(skills)}"
    for cat, skills in skill_groups.items()
    if skills
)

suggested_hint = ""
if suggested:
    suggested_hint = (
        f"\n**Pre-matched skills (MUST activate these)**: {', '.join(suggested)}\n"
        "These skills matched keywords in the user's prompt. You MUST activate them via Skill tool.\n"
    )

output = f"""## Instruction: Forced Skill Activation (Mandatory)

Silently scan the user's request against available skills. Do NOT list every skill with Yes/No.

Available skills:
{grouped_display}
{suggested_hint}
**Action**:
- If any skill matches → Activate via Skill tool, then output: "Activating: [skill-name] — [reason]"
- If no skill matches → Output: "No skills needed"
- Begin implementation only after activation is complete.
- When multiple skills match, activate all of them.
"""

print(output)
sys.exit(0)
