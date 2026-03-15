# Citation Verification Reference Files

## File Purpose

The files in this directory provide **background knowledge and reference information** for understanding citation verification principles and common issues.

**Important**: These files are not part of the main workflow. Actual citation verification uses WebSearch and Google Scholar.

## File Descriptions

### common-errors.md

**Content**: Common citation error patterns and how to fix them

**Purpose**:
- Understand common citation errors in academic writing
- Learn how to identify and fix these errors
- Understand why citation verification is necessary

**When to consult**: When you need to understand types of citation errors and how to fix them

### verification-rules.md

**Content**: Detailed verification rules and matching algorithms

**Purpose**:
- Understand the complete citation verification logic
- Learn how to match titles, authors, years, and other information
- Learn the technical details of verification

**When to consult**: When you need to understand the verification logic in depth

### api-usage.md

**Content**: API usage guide (CrossRef, arXiv, Semantic Scholar)

**Purpose**:
- Understand how to use academic APIs
- Understand the principles of API-based verification
- Reference implementations for advanced use cases

**When to consult**: When you need to understand API verification methods (note: the main workflow uses WebSearch)

## Main Workflow

**For actual citation verification, use the Citation Workflow in the `paper-writing` skill:**

1. Use WebSearch to find papers
2. Verify on Google Scholar
3. Get BibTeX from Google Scholar
4. Verify claims (if needed)
5. Add to bibliography

See the "Citation Workflow (Hallucination Prevention)" section of the `paper-writing` skill.

## Usage Recommendations

**For day-to-day paper writing**:
- Use the `paper-writing` skill's Citation Workflow
- Use WebSearch and Google Scholar
- Consult these files for background knowledge
- Do not use API methods as the main workflow

**For understanding verification principles**:
- Read `common-errors.md` for common errors
- Read `verification-rules.md` for verification logic
- Read `api-usage.md` for API methods (for reference)

## More Information

See the SKILL.md file in the `citation-verification` skill.
