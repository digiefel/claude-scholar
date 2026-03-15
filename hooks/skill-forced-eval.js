#!/usr/bin/env node
/**
 * UserPromptSubmit Hook: Forced skill activation flow (cross-platform version)
 *
 * Event: UserPromptSubmit
 * Function: Force AI to evaluate available skills and begin implementation after activation
 */

const path = require('path');
const fs = require('fs');
const os = require('os');
const common = require('./hook-common');

// Read stdin input
let input = {};
try {
  const stdinData = require('fs').readFileSync(0, 'utf8');
  if (stdinData.trim()) {
    input = JSON.parse(stdinData);
  }
} catch {
  // Use default empty object
}

const userPrompt = input.user_prompt || '';

// Check if it is a slash command (escape)
if (userPrompt.startsWith('/')) {
  // Distinguish commands from paths:
  // - Commands: /commit, /update-github (no second slash after the first)
  // - Paths: /Users/xxx, /path/to/file (contains path separators)
  const rest = userPrompt.substring(1);
  if (rest.includes('/')) {
    // This is a path, continue with skill scanning
  } else {
    // This is a command, skip skill evaluation
    console.log(JSON.stringify({ continue: true }));
    process.exit(0);
  }
}

const homeDir = os.homedir();

// Dynamically collect skill list
function collectSkills() {
  const skills = [];
  const skillsDir = path.join(homeDir, '.claude', 'skills');

  // 1. Collect local skills
  if (fs.existsSync(skillsDir)) {
    const skillDirs = fs.readdirSync(skillsDir, { withFileTypes: true })
      .filter(d => d.isDirectory())
      .map(d => d.name);

    for (const skillName of skillDirs) {
      skills.push(skillName);
    }
  }

  // 2. Collect plugin skills
  const pluginsCache = path.join(homeDir, '.claude', 'plugins', 'cache');

  if (fs.existsSync(pluginsCache)) {
    const marketplaces = fs.readdirSync(pluginsCache, { withFileTypes: true })
      .filter(d => d.isDirectory())
      .map(d => d.name);

    for (const marketplace of marketplaces) {
      const marketplacePath = path.join(pluginsCache, marketplace);
      const plugins = fs.readdirSync(marketplacePath, { withFileTypes: true })
        .filter(d => d.isDirectory() && !d.name.startsWith('.'))
        .map(d => d.name);

      for (const plugin of plugins) {
        const pluginPath = path.join(marketplacePath, plugin);
        const versions = fs.readdirSync(pluginPath, { withFileTypes: true })
          .filter(d => d.isDirectory())
          .map(d => d.name)
          .sort()
          .reverse();

        if (versions.length > 0) {
          const latestVersion = versions[0];
          const skillsDirPath = path.join(pluginPath, latestVersion, 'skills');

          if (fs.existsSync(skillsDirPath)) {
            const skillDirs = fs.readdirSync(skillsDirPath, { withFileTypes: true })
              .filter(d => d.isDirectory())
              .map(d => d.name);

            for (const skillName of skillDirs) {
              skills.push(`${plugin}:${skillName}`);
            }
          }
        }
      }
    }
  }

  // Deduplicate
  return [...new Set(skills)].sort();
}

// Categorize skills into groups
function categorizeSkills(skills) {
  const categories = {
    'Research & Writing': /research|paper|writing|citation|review-response|rebuttal|post-acceptance|doc-coauthoring|latex|daily-paper|ml-paper|results-analysis|brainstorm/,
    'Development': /coding|git|code-review|bug|architecture|verification|tdd|uv-package|webapp-testing|kaggle|driven-development|development-branch|planning|dispatching|executing|using-superpowers/,
    'Plugin Dev': /skill-|command-|hook-|mcp-|agent-identifier|command-name/,
    'Design & UI': /frontend|ui-ux|web-design|canvas|brand|theme|algorithmic-art|slack-gif|figma/,
    'Documents': /docx|xlsx|pptx|pdf|internal-comms|web-artifacts/,
  };

  const grouped = {};
  for (const cat of Object.keys(categories)) {
    grouped[cat] = [];
  }
  grouped['Other'] = [];

  for (const skill of skills) {
    let matched = false;
    for (const [cat, regex] of Object.entries(categories)) {
      if (regex.test(skill)) {
        grouped[cat].push(skill);
        matched = true;
        break;
      }
    }
    if (!matched) {
      grouped['Other'].push(skill);
    }
  }

  return grouped;
}

// Keyword-to-skill mapping for pre-matching
// English keywords use \b for word boundary precision
const KEYWORD_SKILL_MAP = [
  { keywords: /\b(git|github|commit|push|pull|merge|rebase|branch|tag|stash|cherry.?pick|develop|master|main)\b/i, skills: ['git-workflow'] },
  { keywords: /\b(debug|bug|error|broken|failing|traceback|exception)\b/i, skills: ['bug-detective'] },
  { keywords: /\b(tdd|test.?driven)\b/i, skills: ['superpowers:test-driven-development'] },
  { keywords: /\b(code.?review|review code)\b/i, skills: ['code-review-excellence'] },
  { keywords: /\b(paper|manuscript|draft)\b/i, skills: ['ml-paper-writing'] },
  { keywords: /\b(research|idea|brainstorm)\b/i, skills: ['research-ideation'] },
  { keywords: /\b(rebuttal|reviewer|response to reviewer)\b/i, skills: ['review-response'] },
  { keywords: /\b(frontend|landing.?page|dashboard)\b/i, skills: ['frontend-design'] },
  { keywords: /\b(create|write|develop|improve).*skill/i, skills: ['skill-development'] },
  { keywords: /\b(create|write|develop).*hook/i, skills: ['hook-development'] },
  { keywords: /\b(create|write|develop).*command|slash.*command/i, skills: ['command-development'] },
  { keywords: /\b(create|write|develop).*agent/i, skills: ['agent-identifier'] },
  { keywords: /\b(mcp)\b|mcp.*server/i, skills: ['mcp-integration'] },
  { keywords: /\b(architecture|factory|registry)\b/i, skills: ['architecture-design'] },
  { keywords: /\b(uv|pip|package.*manager|venv)\b/i, skills: ['uv-package-manager'] },
  { keywords: /\b(kaggle|competition)\b/i, skills: ['kaggle-learner'] },
  { keywords: /\b(citation|reference.*check)\b/i, skills: ['citation-verification'] },
  { keywords: /\b(latex.*template|overleaf)\b/i, skills: ['latex-conference-template-organizer'] },
  { keywords: /\b(ablation|results.*analysis)\b/i, skills: ['results-analysis'] },
  { keywords: /\b(poster|presentation|promote)\b/i, skills: ['post-acceptance'] },
  { keywords: /\b(plan|planning)\b/i, skills: ['planning-with-files'] },
  { keywords: /\b(verify|verification)\b/i, skills: ['verification-loop'] },
  { keywords: /\b(self.?review)\b/i, skills: ['paper-self-review'] },
  { keywords: /\b(anti.?ai|humanize)\b/i, skills: ['writing-anti-ai'] },
  { keywords: /\b(implement|write code|add feature|modify|refactor)\b/i, skills: ['daily-coding'] },
];

// Pre-match user prompt against keyword map
function suggestSkills(prompt) {
  const suggested = new Set();
  for (const { keywords, skills } of KEYWORD_SKILL_MAP) {
    if (keywords.test(prompt)) {
      for (const s of skills) suggested.add(s);
    }
  }
  return [...suggested];
}

// Generate skill list
const SKILL_LIST = collectSkills();
const SKILL_GROUPS = categorizeSkills(SKILL_LIST);
const suggestedSkills = suggestSkills(userPrompt);

// Format grouped skills (skip empty groups)
const groupedDisplay = Object.entries(SKILL_GROUPS)
  .filter(([, skills]) => skills.length > 0)
  .map(([cat, skills]) => `[${cat}] ${skills.join(', ')}`)
  .join('\n');

// Build suggested skills hint
const suggestedHint = suggestedSkills.length > 0
  ? `\n**Pre-matched skills (MUST activate these)**: ${suggestedSkills.join(', ')}\nThese skills matched keywords in the user's prompt. You MUST activate them via Skill tool.\n`
  : '';

// Generate output
const output = `## Instruction: Forced Skill Activation (Mandatory)

Silently scan the user's request against available skills. Do NOT list every skill with Yes/No.

Available skills:
${groupedDisplay}
${suggestedHint}
**Action**:
- If any skill matches → Activate via Skill tool, then output: "Activating: [skill-name] — [reason]"
- If no skill matches → Output: "No skills needed"
- Begin implementation only after activation is complete.
- When multiple skills match, activate all of them.
`;

console.log(output);

process.exit(0);
