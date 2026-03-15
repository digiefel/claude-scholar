---
name: paper-writing
description: Write publication-ready academic and technical papers. Use when drafting papers from research or code, conducting literature reviews, finding related work, verifying citations, or preparing submissions. Covers general academic paper structure, clarity/logic guidance, and citation best practices.
version: 2.0.0
author: Orchestra Research
license: MIT
tags: [Academic Writing, Paper Writing, Citations, Research, Technical Writing]
dependencies: [semanticscholar, arxiv, habanero, requests]
---

# Paper Writing

Expert-level guidance for writing clear, well-structured academic and technical papers. This skill covers writing philosophy, paper structure, citation practices, and quality refinement for any research domain.

## Core Philosophy: Collaborative Writing

**Paper writing is collaborative, but Claude should be proactive in delivering drafts.**

The typical workflow starts with a research repository containing code, results, and documentation. Claude's role is to:

1. **Understand the project** by exploring the repo, results, and existing documentation
2. **Deliver a complete first draft** when confident about the contribution
3. **Search literature** using web search and APIs to find relevant citations
4. **Refine through feedback cycles** when the researcher provides input
5. **Ask for clarification** only when genuinely uncertain about key decisions

## Paper Structure

### Standard Academic Structure

A well-structured paper follows this progression:

1. **Abstract** — Concisely state the problem, approach, and key results (150–250 words)
2. **Introduction** — Motivate the problem, summarize the contribution, outline the paper
3. **Related Work** — Survey relevant prior work; position your contribution clearly
4. **Methodology / Approach** — Describe what you did with enough detail to reproduce
5. **Results / Evaluation** — Present findings clearly; use tables and figures
6. **Discussion** — Interpret results, acknowledge limitations, discuss implications
7. **Conclusion** — Summarize contributions and suggest future directions
8. **References** — Accurate, complete citations

### The 5-Sentence Abstract Formula

A strong abstract covers:
1. What is the problem and why does it matter?
2. What are the limitations of existing approaches?
3. What is your key idea or approach?
4. What are your main results?
5. What is the broader implication?

## Writing Principles

### Clarity First
- Write for a reader familiar with the field but unfamiliar with your specific work
- Prefer simple, direct sentences over complex constructions
- Define every term before using it
- Avoid jargon unless it's standard in the field

### Logical Structure
- Each paragraph should have one clear point
- Use topic sentences to signal what each paragraph covers
- Ensure each section flows naturally to the next
- Claims must be supported by evidence or citations

### Narrative Framing
- Frame the paper as a story: problem → challenge → insight → solution → validation
- The introduction should make a reader want to read the rest
- Every design decision should be explained, not just described

## Citation Practices

### Finding References
- Use WebSearch to find relevant papers on arXiv, Google Scholar, Semantic Scholar
- Search both for directly related work and for foundational papers the reader may expect
- Verify that cited claims actually appear in the cited paper

### Citation Verification Workflow
Use the `citation-verification` skill for multi-layer validation:
1. **Format check** — correct author names, year, venue, title
2. **API check** — paper exists (Semantic Scholar / arXiv API)
3. **Information check** — cited claim matches paper content
4. **Content check** — paper actually supports the point being made

### Reference Management
- Export references in BibTeX format for version control
- Use consistent citation keys (AuthorYearKeyword format)
- Keep a `references.bib` file alongside the manuscript

## Quality Refinement

### Anti-AI Writing Pass
Use `writing-anti-ai` skill to remove:
- Inflated symbolism and promotional language ("groundbreaking", "revolutionary")
- Vague attributions ("studies show", "it is widely known")
- Hedging without substance ("it could potentially be argued that")

### Self-Review Checklist
Use `paper-self-review` skill for systematic quality assessment:
- [ ] Logical flow: does each section follow naturally?
- [ ] Argument soundness: are all claims supported?
- [ ] Citation accuracy: do references say what you claim?
- [ ] Figure quality: are figures readable and well-captioned?
- [ ] Writing clarity: can a field-knowledgeable reader follow?
- [ ] Length: is every section earning its space?

## Workflow

### Starting from a Research Repository

```
Explore repo → Understand contribution → Draft outline → Write introduction first
→ Fill remaining sections → Literature search → Insert citations
→ Write abstract last → Revise and polish
```

### Iterative Refinement

```
First draft (structure) → Content pass (completeness) → Argument pass (logic)
→ Citation pass (accuracy) → Writing pass (clarity) → Self-review → Submission
```

## When to Use This Skill

- Drafting any section of an academic or technical paper
- Structuring arguments and organizing content
- Finding and integrating related work
- Verifying citations and polishing prose
- Preparing a paper for submission or internal review

## Additional Resources

### Reference Files

Detailed guides available on demand:

- **`references/writing-philosophy.md`** — Core writing principles from experienced researchers
- **`references/paper-structure-guide.md`** — Section-by-section guidance with examples
- **`references/literature-search-strategies.md`** — Search techniques for academic databases
- **`references/citation-best-practices.md`** — Citation verification and reference management
- **`references/knowledge/structure.md`** — Paper organization patterns from successful papers
- **`references/knowledge/writing-techniques.md`** — Sentence templates and transitions
- **`references/knowledge/review-response.md`** — Strategies for responding to reviewer feedback

### Related Skills

- `citation-verification` — Multi-layer citation validation
- `writing-anti-ai` — Remove AI writing patterns
- `paper-self-review` — 6-item quality checklist
- `review-response` — Systematic rebuttal writing
