# Claude Scholar Configuration

## Project Overview

**Claude Scholar** - Personal Claude Code configuration system for academic research and software development

**Mission**: Cover the complete academic research lifecycle (from ideation to publication) and software development workflows, with plugin development and project management capabilities.

---

## Tech Stack & Git Standards

**Python**: use `uv` as the package manager.

**Git Standards**:
- **Commit convention**: Conventional Commits
  ```
  Type: feat, fix, docs, style, refactor, perf, test, chore
  ```
- **Branch strategy**: master/develop/feature/bugfix/hotfix/release
- **Merge strategy**: rebase for feature branch sync, merge --no-ff for integration

---

## Global Configuration

### Language Settings
- **Respond in English to the user**
- Keep technical terms in English (e.g. TDD, Git, DOI, LaTeX)
- Do not translate proper nouns or names

### Working Directory Standards
- Plan documents: `/plan` folder
- Temporary files: `/temp` folder
- Auto-create folders if they don't exist

### Task Execution Principles
- Discuss approach before breaking down complex tasks
- Run example tests after implementation
- Make backups, avoid breaking existing functionality
- Clean up temporary files after completion

### Work Style
- **Task management**: Use TodoWrite to track progress, plan before executing complex tasks, prefer existing skills
- **Communication**: Ask proactively when uncertain, confirm before important operations, follow hook-enforced workflows
- **Code style**: Python follows PEP 8, comments in English, identifiers in English

---

## Core Workflows

### Research Lifecycle (5 Stages)

```
Ideation → Development → Paper Writing → Self-Review → Submission/Rebuttal
```

| Stage | Core Tools |
|-------|-----------|
| 1. Research Ideation | `research-ideation` skill + `literature-reviewer` agent + Zotero MCP |
| 2. Project Dev | `architecture-design` skill + `code-reviewer` agent |
| 3. Paper Writing | `paper-writing` skill + `paper-miner` agent |
| 4. Self-Review | `paper-self-review` skill |
| 5. Submission & Rebuttal | `review-response` skill + `rebuttal-writer` agent |

### Supporting Workflows

- **Automation**: 5 Hooks auto-trigger at session lifecycle stages (skill evaluation, env init, work summary, security check)
- **Zotero Integration**: Automated paper import, collection management, full-text reading, and citation export via Zotero MCP
- **Knowledge Extraction**: `paper-miner` agent continuously extracts writing knowledge from papers
- **Skill Evolution**: `skill-development` → `skill-quality-reviewer` → `skill-improver` three-step improvement loop

---

## Skills Directory

### Research & Writing

- **research-ideation**: Research startup (5W1H, literature review, gap analysis, research question formulation)
- **citation-verification**: Citation verification (multi-layer: format→API→info→content)
- **paper-writing**: Academic and technical paper writing assistance (structure, logic, citations)
- **writing-anti-ai**: Remove AI writing patterns
- **paper-self-review**: Paper self-review (6-item quality checklist)
- **review-response**: Systematic rebuttal writing
- **doc-coauthoring**: Document co-authoring workflow

### Development

- **git-workflow**: Git workflow standards (Conventional Commits, branch management)
- **bug-detective**: Debugging and error investigation
- **uv-package-manager**: uv package manager usage
- **planning-with-files**: Planning and progress tracking with Markdown files

### Plugin Development

- **skill-development**: Skill development guide
- **skill-improver**: Skill improvement tool
- **skill-quality-reviewer**: Skill quality review
- **agent-identifier**: Agent development configuration
- **hook-development**: Hook development and event handling
- **mcp-integration**: MCP server integration

---

## Agents

### Research Workflow

- **literature-reviewer** - Literature search, classification, and trend analysis (Zotero MCP integration)
- **data-analyst** - Data analysis and visualization
- **rebuttal-writer** - Systematic rebuttal writing with tone optimization
- **paper-miner** - Extract writing knowledge from successful papers

### Development Workflow

- **architect** - System architecture design
- **build-error-resolver** - Build error fixing
- **bug-analyzer** - Deep code execution flow analysis and root cause investigation
- **code-reviewer** - Code review
- **refactor-cleaner** - Code refactoring and cleanup

---

## Hooks (5 Hooks)

Cross-platform Node.js hooks for automated workflow execution:

| Hook | Trigger | Function |
|------|---------|----------|
| `session-start.js` | Session start | Show Git status, todos, available commands |
| `skill-forced-eval.js` | Every user input | Force evaluate all available skills |
| `session-summary.js` | Session end | Generate work log, detect CLAUDE.md updates |
| `stop-summary.js` | Session stop | Quick status check, temp file detection |
| `security-guard.js` | File operations | Security validation (key detection, dangerous command interception) |

---

## Rules (4 Rules)

Global constraints, always active:

| Rule File | Purpose |
|-----------|---------|
| `coding-style.md` | Code standards: file size, type hints, patterns |
| `agents.md` | Agent orchestration: auto-invocation timing, parallel execution, multi-perspective analysis |
| `security.md` | Security standards: key management, sensitive file protection, pre-commit security checks |
| `experiment-reproducibility.md` | Experiment reproducibility: config recording, environment recording, result management |

---

## Naming Conventions

### Skill Naming
- Format: kebab-case (lowercase + hyphens)
- Form: prefer gerund form (verb+ing)
- Example: `scientific-writing`, `git-workflow`, `bug-detective`

### Tags Naming
- Format: Title Case
- Abbreviations all caps: TDD, DOI, API, Git
- Example: `[Writing, Research, Academic]`

### Description Standards
- Person: third person
- Content: include purpose and use cases
- Example: "Provides guidance for academic paper writing, covering top-venue submission requirements"

---

## Task Completion Summary

After each task, proactively provide a brief summary:

```
📋 Operation Review
1. [Main operation]
2. [Modified files]

📊 Current Status
• [Git/filesystem/runtime status]

💡 Next Steps
1. [Targeted suggestions]
```
