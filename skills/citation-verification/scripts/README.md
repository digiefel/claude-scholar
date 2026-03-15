# Citation Verification Scripts

## Status

**These scripts are reference implementations, not part of the main workflow.**

The Python scripts in this directory provide API-based citation verification implementations, but **the actual citation verification workflow uses WebSearch and Google Scholar**, not these scripts.

## Why Keep These Scripts?

These scripts are retained as **reference implementations** for:

1. **Understanding verification logic** - demonstrates the complete logic and steps of citation verification
2. **Learning API usage** - shows how to use CrossRef, arXiv, Semantic Scholar, and other APIs
3. **Advanced use cases** - for scenarios requiring batch verification or automation, these implementations can serve as references

## Main Workflow

**For actual citation verification, use the Citation Workflow in the `paper-writing` skill:**

1. Use WebSearch to find papers
2. Verify on Google Scholar
3. Get BibTeX from Google Scholar
4. Verify claims (if needed)
5. Add to bibliography

See the "Citation Workflow (Hallucination Prevention)" section of the `paper-writing` skill.

## Script Descriptions

### verify-citations.py

A complete citation verification script including:
- Four-layer verification mechanism (format, existence, information matching, content validation)
- Multi-API support (CrossRef, arXiv, Semantic Scholar)
- Report generation

**Purpose**: Reference implementation to understand the complete verification logic

### api-clients.py

An API client library including:
- CrossRefClient - DOI verification
- ArXivClient - arXiv paper verification
- SemanticScholarClient - general academic search
- CitationAPIManager - unified API management

**Purpose**: Reference implementation to understand how to use academic APIs

### format-checker.py

A BibTeX and LaTeX format checking tool including:
- BibTeX format validation
- LaTeX citation check
- Format error reporting

**Purpose**: Reference implementation to understand format checking logic

## Usage Recommendations

**For day-to-day paper writing**:
- Use the `paper-writing` skill's Citation Workflow
- Use WebSearch and Google Scholar
- Do not use these Python scripts

**For batch verification or automation**:
- These script implementations can be used as references
- Modify and use as needed
- Be aware of API rate limits

## Dependency Installation

If you need to run these scripts (for reference or advanced use cases only):

```bash
pip install bibtexparser requests semanticscholar arxiv
```

## More Information

See the SKILL.md file in the `citation-verification` skill.
