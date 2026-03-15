# Zotero MCP Integration Guide

Automated literature management integration via the Zotero MCP server.

## 1. Available Tools

### 1.1 Browsing Tools

| Tool | Function | Use Case |
|------|----------|----------|
| `get_collections` | List all collections | View existing research projects |
| `get_collection_items` | Get items in a collection | Browse papers in a specific collection |
| `search_library` | Search items in the library | Find existing papers by keyword |
| `get_items_details` | Batch get item metadata | Get detailed paper information |
| `get_item_fulltext` | Get PDF full text | Read paper content |

### 1.2 Adding Tools

| Tool | Function | Use Case |
|------|----------|----------|
| `add_items_by_doi` | Add papers by DOI | Automatically get metadata and OA PDF |
| `add_web_item` | Save webpage as item | Save non-paper resources |
| `create_collection` | Create collection | Organize research projects |
| `import_pdf_to_zotero` | Import PDF | Upload local or online PDF |
| `find_and_attach_pdfs` | Batch attach OA PDFs | Find PDFs for existing items |
| `add_linked_url_attachment` | Attach URL link | Associate online resources |

### 1.3 Citation Tools

| Tool | Function | Use Case |
|------|----------|----------|
| `inject_citations` | Inject citations into Word | Generate citation format |

## 2. Collection Organization Strategy

### 2.1 Naming Convention

```
Research-{topic-keywords}-{YYYY}
```

Examples:
- `Research-TransformerInterpretability-2026`
- `Research-BrainDecoding-2026`
- `Research-RLHF-2026`

### 2.2 Standard Sub-Collection Structure

```
Research-{topic}-{date}
  ├── Core Papers
  ├── Methods
  ├── Applications
  ├── Baselines
  └── To-Read
```

Sub-collection purposes:

| Sub-collection | Inclusion Criteria | Typical Count |
|---------------|-------------------|---------------|
| Core Papers | Directly relevant, highly-cited key papers | 5-15 papers |
| Methods | Technical method references, approaches to borrow | 10-20 papers |
| Applications | Application scenario references, domain practices | 5-10 papers |
| Baselines | Experimental comparison baselines, work to reproduce | 3-8 papers |
| To-Read | Initial screening, pending detailed reading | Unlimited |

## 3. Automated Workflows

### 3.1 Paper Discovery and Import

```
WebSearch for papers
    |
Extract DOIs from search results
    |
add_items_by_doi batch-add to Zotero
    |
find_and_attach_pdfs auto-attach OA PDFs
    |
get_item_fulltext read full text for analysis
```

### 3.2 DOI Extraction Tips

**Identifying DOIs from search result URLs**:
- `https://doi.org/10.xxxx/xxxxx` — direct DOI link
- `https://dl.acm.org/doi/10.xxxx/xxxxx` — ACM Digital Library
- `https://arxiv.org/abs/xxxx.xxxxx` — arXiv (DOI: `10.48550/arXiv.xxxx.xxxxx`)

**Common DOI formats**:
- Starts with `10.`, contains `/` separator
- Example: `10.1038/s41586-023-06747-5` (Nature)
- Example: `10.48550/arXiv.2301.00234` (arXiv)
- Example: `10.1145/3580305.3599256` (ACM/KDD)

**CrossRef query**:
- When no obvious DOI in the URL, search CrossRef using the paper title to get the DOI

### 3.3 Full-Text Reading and Notes

```
get_item_fulltext to retrieve full text
    |
Analyze paper content
    |
Extract key information
    |
Generate structured notes
```

### 3.4 Notes Template

Structured notes for each paper should include:

```markdown
## [Paper Title]

**Basic Information**:
- Authors:
- Conference/Journal:
- Year:
- DOI:

**Research Question**:
- What problem does it solve?
- Why is it important?

**Core Method**:
- Main technical approach
- Key innovations

**Key Findings**:
- Main experimental results
- Important conclusions

**Limitations**:
- Method limitations
- Experimental limitations

**Relevance to This Research**:
- What can be borrowed
- Differences and room for improvement
```

## 4. Common Issues

### 4.1 API Rate Limits

Zotero API has rate limits; when batch-adding, it is recommended to:
- Add no more than 10 papers per batch
- Allow appropriate intervals between batches
- If a 429 error occurs, wait and retry

### 4.2 PDF Full-Text Indexing Delay

Newly uploaded PDFs take time to index:
- If `get_item_fulltext` returns empty, retry later
- Zotero client must be running to complete indexing
- Large PDFs take longer to index

### 4.3 DOI Not Recognized

Some papers may not have a standard DOI:
- arXiv preprints: use `10.48550/arXiv.{id}` format
- Workshop papers: try to get from publisher page
- Cannot get DOI: use `add_web_item` to save webpage link

### 4.4 OA PDF Unavailable

Non-open-access papers cannot be retrieved via Unpaywall:
- Check if the author's homepage has a preprint version
- Check if arXiv has a corresponding version
- If manual upload is needed, use `import_pdf_to_zotero`
