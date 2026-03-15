---
description: Check and update CLAUDE.md memory based on changes to skills, commands, agents, and hooks.
---

# Update Memory

Check and update the CLAUDE.md global memory file to ensure its content stays in sync with the source files for skills, commands, agents, and hooks.

## Feature Overview

CLAUDE.md is a consolidated memory file containing:
- Skills directory structure (from `skills/`)
- Command list (from `commands/`)
- Agent configuration (from `agents/`)
- Hook definitions (from `hooks/`)

When these source files change, CLAUDE.md needs to be updated accordingly.

## Detection Logic

1. **Scan source file modification times**
   - `~/.claude/skills/**/skill.md`
   - `~/.claude/commands/**/*.md`
   - `~/.claude/agents/**/*.md`
   - `~/.claude/hooks/**/*.{js,json}`

2. **Compare against CLAUDE.md last modification time**
   - If any source file is newer than CLAUDE.md → update needed
   - Record last sync timestamp (`~/.claude/.last-memory-sync`)

3. **Generate report**
   - List all changed source files
   - Show CLAUDE.md sections that need updating

## Update Workflow

### 1. Scan Phase

```
Scanning Skills: X items
Scanning Commands: Y items
Scanning Agents: Z items
Scanning Hooks: W items
```

### 2. Comparison Phase

```
Sections to update:
- [ ] Skills directory structure (3 skills changed)
- [ ] Command list (1 command added)
- [ ] Agent configuration (no changes)
- [ ] Hook definitions (2 hooks modified)
```

### 3. Confirm Update

Ask the user whether to execute the update:
```
Update CLAUDE.md? (yes/no/diff)
- yes: execute update
- no: cancel
- diff: show detailed diff
```

### 4. Execute Update

- Preserve user-edited content (e.g., "User Background", "Tech Stack Preferences")
- Only update sections marked AUTO-GENERATED
- Update timestamp

## Usage

```
/update-memory          # check and prompt to update
/update-memory --check  # check only, no update
/update-memory --force  # force update without prompting
/update-memory --diff   # show diff comparison
```

## Output Example

### Check Result

```
CLAUDE.md Memory Status Check

Source file status:
Skills: 24 items (most recently modified: paper-writing)
Commands: 14 items (most recently modified: update-readme)
Agents: 7 items (no changes)
Hooks: 5 items (most recently modified: session-summary)

Timestamp comparison:
- CLAUDE.md last updated: 2024-01-15 10:30
- Source files last modified: 2024-01-16 14:22

Changes detected, CLAUDE.md update recommended

Change details:
1. skills/paper-writing/skill.md (modified at 14:22)
2. commands/update-readme.md (modified at 13:15)
3. hooks/session-summary.js (modified at 11:45)

Execute update? (yes/no/diff)
```

### Update Complete

```
CLAUDE.md updated

Updated content:
- Skills directory: synced 24 skills
- Command list: synced 14 commands
- Agent configuration: no changes
- Hook definitions: synced 5 hooks

Next sync timestamp updated.
```

## Integration Recommendations

- Integrate check reminder in `session-summary.js`
- Detect in real time via PostToolUse hook
- Recommended to run periodically (e.g., at the end of each session)
