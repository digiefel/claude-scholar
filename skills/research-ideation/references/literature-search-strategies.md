# Literature Search Strategies

Systematic literature search methods to help researchers efficiently find relevant papers.

## 1. Keyword Construction

### 1.1 Core Concept Identification

Extract core concepts from research interests:

**Example**: Research interest "Interpretability of Transformer models"
- Core concept 1: Transformer
- Core concept 2: Interpretability / Explainability

### 1.2 Synonyms and Variants

List synonyms and variants for each core concept:

| Core Concept | Synonyms/Variants |
|-------------|-------------------|
| Transformer | Attention mechanism, Self-attention, BERT, GPT |
| Interpretability | Explainability, Transparency, Understanding |

### 1.3 Boolean Operators

Combine keywords using Boolean operators:

```
(Transformer OR "attention mechanism" OR BERT OR GPT)
AND
(interpretability OR explainability OR transparency)
```

### 1.4 Domain-Specific Terms

Add domain-specific terminology:

- **Method terms**: probing, attention visualization, saliency maps
- **Application domains**: NLP, computer vision, speech recognition
- **Evaluation metrics**: faithfulness, plausibility, human evaluation

## 2. Selecting Academic Databases

### 2.1 Major Databases

| Database | Characteristics | Use Case |
|----------|----------------|----------|
| **arXiv** | Preprints, fast updates | Get the latest research advances |
| **Semantic Scholar** | AI-driven, citation analysis | Discover related papers, analyze impact |
| **Google Scholar** | Broad coverage | Comprehensive search, catch missing papers |
| **ACL Anthology** | NLP specialized | Deep search in NLP domain |
| **IEEE Xplore** | Engineering/technology | Computer vision, hardware-related |

### 2.2 Search Strategies

**arXiv search**:
```
cat:cs.LG AND (transformer OR attention) AND (interpretability OR explainability)
```

**Semantic Scholar search**:
- Use natural language queries
- Filter using "Highly Influential Citations"
- Check "Related Papers" to discover related work

**Google Scholar search**:
- Use quotes for exact match: "transformer interpretability"
- Limit time range: 2020-2024
- Exclude patents: -patent

## 3. Search Techniques

### 3.1 Iterative Search

1. **Initial search** - Use core keywords
2. **Analyze results** - Check keywords from highly-cited papers
3. **Refine query** - Add newly discovered terms
4. **Repeat** - Until enough relevant papers are found

### 3.2 Citation Tracking

**Forward citation**:
- Check which newer papers cite a given paper
- Understand subsequent developments of the research

**Backward citation**:
- Check which papers a given paper cites
- Understand the foundations and background of the research

### 3.3 Author Tracking

- Identify key researchers in the field
- Check their other related work
- Follow their latest research

## 4. Paper Screening Criteria

### 4.1 Initial Screening (Based on Title and Abstract)

**Inclusion criteria**:
- Directly relevant to the research topic
- Published at top conferences/journals (NeurIPS, ICML, ICLR, ACL, AAAI)
- High citation count (relative to publication date)
- Authors from well-known institutions or research groups

**Exclusion criteria**:
- Unrelated to the research topic
- Published in low-quality conferences/journals
- Clearly outdated methods (unless a classic paper)

### 4.2 Deep Screening (Based on Full Text)

**Quality evaluation**:
1. **Methodological innovation** - Does it propose a new method or perspective
2. **Experimental rigor** - Is the experimental design sound and results credible
3. **Writing quality** - Is the paper clear and readable
4. **Reproducibility** - Does it provide code and data

**Relevance evaluation**:
1. **Directly relevant** - Core method or problem is directly related
2. **Indirectly relevant** - Related techniques or application scenarios
3. **Background knowledge** - Provides necessary background and foundations

### 4.3 Literature Management

**Integration tools**:
- **Zotero** (primary tool, integrated via MCP)
  - Automatically add papers via `add_items_by_doi` to get complete metadata
  - Automatically create and organize collections via `create_collection`
  - Automatically attach OA PDFs via `find_and_attach_pdfs`
  - Read PDF full text for analysis via `get_item_fulltext`
  - Search existing papers to avoid duplicates via `search_library`
- Mendeley - social features, PDF annotation (alternative)
- Papers - Mac-native, elegant interface (alternative)

**Organization strategy**:

Use Zotero collection structure to organize literature:

```
Research-{topic}-{date}
  ├── Core Papers
  ├── Methods
  ├── Applications
  ├── Baselines
  └── To-Read
```

- Core Papers: Directly relevant, highly-cited key papers
- Methods: Technical method references, methodological approaches to borrow
- Applications: Application scenario references, domain practices
- Baselines: Experimental comparison baselines, work to reproduce
- To-Read: Initial screening, pending detailed reading

## 5. DOI Extraction and Automatic Import

### 5.1 DOI Extraction Methods

Common ways to extract DOIs from WebSearch results:

**DOI in URL**:
- `https://doi.org/10.xxxx/xxxxx` - Direct DOI link
- `https://dl.acm.org/doi/10.xxxx/xxxxx` - ACM Digital Library
- `https://ieeexplore.ieee.org/document/xxxxx` - IEEE (extract from page)
- `https://arxiv.org/abs/xxxx.xxxxx` - arXiv (DOI format: `10.48550/arXiv.xxxx.xxxxx`)

**Common DOI formats**:
- `10.xxxx/xxxxx` - Standard DOI prefix
- Starts with `10.`, contains `/` separator
- Example: `10.1038/s41586-023-06747-5` (Nature)
- Example: `10.48550/arXiv.2301.00234` (arXiv)

### 5.2 Automatic Import Workflow

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

**Operation example**:

1. Use WebSearch to search `"transformer interpretability" site:arxiv.org OR site:doi.org`
2. Collect DOI list from results
3. Call `add_items_by_doi` for batch import (recommend no more than 10 per batch to avoid API rate limits)
4. Call `find_and_attach_pdfs` to attach PDFs to imported papers
5. Use `get_item_fulltext` to read key paper full texts

### 5.3 Handling Papers Without DOI

Some papers may not have a standard DOI:
- **arXiv preprints**: Use `10.48550/arXiv.{id}` format
- **Conference proceedings**: Try to get DOI from publisher page
- **Cannot get DOI**: Use `add_web_item` to save webpage link, or use `import_pdf_to_zotero` to import PDF directly
