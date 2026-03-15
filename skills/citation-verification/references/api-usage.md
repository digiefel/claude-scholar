# API Usage Guide

This document explains in detail how to use three main APIs for citation verification.

## Semantic Scholar API

### Overview

Semantic Scholar is a free academic search engine that provides a powerful API for paper retrieval and metadata access.

**Advantages:**
- Free to use, no API key required
- Covers a wide range of academic disciplines
- Provides rich metadata
- Supports fuzzy search

**Limitations:**
- Rate limit: 100 requests/5min
- Some papers may be missing

### API Endpoints

**1. Get paper by Paper ID**
```
GET https://api.semanticscholar.org/graph/v1/paper/{paper_id}
```

**2. Search papers**
```
GET https://api.semanticscholar.org/graph/v1/paper/search?query={query}
```

### Python Example

**Installation:**
```bash
pip install semanticscholar
```

**Basic usage:**
```python
from semanticscholar import SemanticScholar

sch = SemanticScholar()

# Search by title
results = sch.search_paper("Attention is All You Need", limit=5)
for paper in results:
    print(f"Title: {paper.title}")
    print(f"Authors: {[a.name for a in paper.authors]}")
    print(f"Year: {paper.year}")
    print(f"DOI: {paper.externalIds.get('DOI', 'N/A')}")
    print("---")
```

**Get by DOI:**
```python
# DOI format: DOI:10.48550/arXiv.1706.03762
paper = sch.get_paper("DOI:10.48550/arXiv.1706.03762")
print(f"Title: {paper.title}")
print(f"Citations: {paper.citationCount}")
```

### Field Descriptions

**Main returned fields:**
- `paperId` - Semantic Scholar internal ID
- `title` - paper title
- `authors` - list of authors
- `year` - publication year
- `venue` - publication venue (conference/journal)
- `externalIds` - external identifiers (DOI, arXiv, PubMed, etc.)
- `citationCount` - citation count
- `abstract` - abstract

### Error Handling

```python
try:
    paper = sch.get_paper("invalid_id")
except Exception as e:
    print(f"Error: {e}")
    # Handle error: flag for manual verification
```

## arXiv API

### Overview

arXiv is a preprint repository that provides a free API for accessing paper metadata.

**Advantages:**
- Completely free, no authentication required
- Covers physics, mathematics, computer science, and more
- Provides full paper PDFs
- Updated promptly

**Limitations:**
- Limited to preprint papers
- Does not include published journal version information

### API Endpoint

**Query interface:**
```
GET http://export.arxiv.org/api/query?search_query={query}&start={start}&max_results={max}
```

### Python Example

**Installation:**
```bash
pip install arxiv
```

**Basic usage:**
```python
import arxiv

# Get by arXiv ID
paper = next(arxiv.Search(id_list=["1706.03762"]).results())
print(f"Title: {paper.title}")
print(f"Authors: {[a.name for a in paper.authors]}")
print(f"Published: {paper.published}")
print(f"PDF URL: {paper.pdf_url}")

# Search by title
search = arxiv.Search(
    query="Attention is All You Need",
    max_results=5,
    sort_by=arxiv.SortCriterion.Relevance
)

for result in search.results():
    print(f"Title: {result.title}")
    print(f"arXiv ID: {result.entry_id.split('/')[-1]}")
    print("---")
```

### arXiv ID Format

**Identifying arXiv IDs:**
- New format: `YYMM.NNNNN` (e.g., 2301.12345)
- Old format: `arch-ive/YYMMNNN` (e.g., cs/0703001)

**Extracting from URL:**
```python
import re

def extract_arxiv_id(text):
    # Match new format
    match = re.search(r'\d{4}\.\d{4,5}', text)
    if match:
        return match.group()
    # Match old format
    match = re.search(r'[a-z-]+/\d{7}', text)
    if match:
        return match.group()
    return None
```

## CrossRef API

### Overview

CrossRef is a DOI registration agency that provides authoritative academic literature metadata.

**Advantages:**
- DOI is the most reliable unique identifier
- Covers almost all formally published papers
- High data quality and authority
- Supports direct BibTeX retrieval

**Limitations:**
- Limited to papers with a DOI
- Preprints generally do not have DOIs

### API Endpoints

**Get metadata by DOI:**
```
GET https://api.crossref.org/works/{doi}
```

**Get BibTeX by DOI:**
```
GET https://doi.org/{doi}
Headers: Accept: application/x-bibtex
```

### Python Example

**Get metadata by DOI:**
```python
import requests

def get_crossref_metadata(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['message']
    return None

# Example
doi = "10.48550/arXiv.1706.03762"
metadata = get_crossref_metadata(doi)
if metadata:
    print(f"Title: {metadata['title'][0]}")
    print(f"Authors: {[f\"{a['given']} {a['family']}\" for a in metadata['author']]}")
    print(f"Published: {metadata['published']['date-parts'][0]}")
```

**Get BibTeX by DOI:**
```python
def doi_to_bibtex(doi):
    url = f"https://doi.org/{doi}"
    headers = {"Accept": "application/x-bibtex"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

# Example
bibtex = doi_to_bibtex("10.48550/arXiv.1706.03762")
print(bibtex)
```

### DOI Format

**Standard format:**
- `10.XXXX/suffix` (e.g., 10.1038/nature12345)
- Prefix `10.` is fixed
- Middle part is the registrant code
- Suffix is defined by the publisher

**Extracting DOI from text:**
```python
import re

def extract_doi(text):
    # Match DOI format
    match = re.search(r'10\.\d{4,}/[^\s]+', text)
    if match:
        return match.group()
    return None
```

## API Selection Strategy

Choose the most appropriate API based on the available citation information:

### Decision Flow

```
Has DOI?
  |-- Yes --> CrossRef API (most reliable)
  +-- No  --> Has arXiv ID?
                  |-- Yes --> arXiv API
                  +-- No  --> Semantic Scholar API (general search)
```

### Implementation Example

```python
def verify_citation(citation_info):
    """
    Select the appropriate API for verification based on citation information

    Args:
        citation_info: dict with keys: doi, arxiv_id, title, authors

    Returns:
        verification result dictionary
    """
    # Strategy 1: prefer DOI
    if citation_info.get('doi'):
        return verify_with_crossref(citation_info['doi'])

    # Strategy 2: arXiv ID
    if citation_info.get('arxiv_id'):
        return verify_with_arxiv(citation_info['arxiv_id'])

    # Strategy 3: general search
    if citation_info.get('title'):
        return verify_with_semantic_scholar(
            citation_info['title'],
            citation_info.get('authors')
        )

    return {'status': 'insufficient_info'}
```

## Best Practices

### 1. Error Handling

```python
import time
from requests.exceptions import RequestException

def api_call_with_retry(func, max_retries=3):
    """API call with retry"""
    for i in range(max_retries):
        try:
            return func()
        except RequestException as e:
            if i == max_retries - 1:
                raise
            time.sleep(2 ** i)  # exponential backoff
```

### 2. Rate Limiting

```python
import time

class RateLimiter:
    def __init__(self, calls_per_minute):
        self.calls_per_minute = calls_per_minute
        self.last_call = 0

    def wait_if_needed(self):
        elapsed = time.time() - self.last_call
        min_interval = 60.0 / self.calls_per_minute
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self.last_call = time.time()

# Usage example
limiter = RateLimiter(calls_per_minute=20)
limiter.wait_if_needed()
result = api_call()
```

### 3. Caching Results

```python
import json
from pathlib import Path

class APICache:
    def __init__(self, cache_dir=".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def get(self, key):
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text())
        return None

    def set(self, key, value):
        cache_file = self.cache_dir / f"{key}.json"
        cache_file.write_text(json.dumps(value))
```

## Summary

### API Comparison

| API | Advantages | Limitations | Recommended when |
|-----|-----------|-------------|-----------------|
| **CrossRef** | Most authoritative, supports BibTeX | Only for papers with DOI | DOI is available |
| **arXiv** | Free, updated quickly | Preprints only | arXiv papers |
| **Semantic Scholar** | Wide coverage, fuzzy search | Some papers missing | General search |

### Verification Reliability Ranking

1. **CrossRef (DOI)** - Most reliable
2. **arXiv (arXiv ID)** - Reliable
3. **Semantic Scholar (title search)** - Fairly reliable, manual confirmation recommended
