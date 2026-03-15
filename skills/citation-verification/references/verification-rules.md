# Verification Rules

This document explains in detail the specific rules and matching algorithms for the four-layer verification mechanism.

## Layer 1: Format Validation

### BibTeX Format Check

**Required field validation:**

Different BibTeX entry types have different required field requirements:

**@article (journal paper):**
- Required: `author`, `title`, `journal`, `year`
- Optional: `volume`, `number`, `pages`, `doi`

**@inproceedings (conference paper):**
- Required: `author`, `title`, `booktitle`, `year`
- Optional: `pages`, `organization`, `doi`

**@book (book):**
- Required: `author` or `editor`, `title`, `publisher`, `year`
- Optional: `volume`, `series`, `address`

**@misc (other):**
- Required: `title`
- Optional: `author`, `howpublished`, `year`, `note`

### Format Check Rules

**1. Entry structure check**
```python
def check_bibtex_structure(entry):
    """Check BibTeX entry structure"""
    errors = []

    # Check for entry type
    if not entry.get('ENTRYTYPE'):
        errors.append("Missing entry type")

    # Check for ID
    if not entry.get('ID'):
        errors.append("Missing citation key")

    # Check required fields
    required = get_required_fields(entry.get('ENTRYTYPE'))
    for field in required:
        if not entry.get(field):
            errors.append(f"Missing required field: {field}")

    return errors
```

**2. Field format check**
```python
def check_field_format(entry):
    """Check field format"""
    errors = []

    # Year format check
    if 'year' in entry:
        year = entry['year']
        if not year.isdigit() or len(year) != 4:
            errors.append(f"Invalid year format: {year}")
        if int(year) < 1900 or int(year) > 2030:
            errors.append(f"Year out of reasonable range: {year}")

    # DOI format check
    if 'doi' in entry:
        doi = entry['doi']
        if not doi.startswith('10.'):
            errors.append(f"Invalid DOI format: {doi}")

    return errors
```

### LaTeX Citation Check

**1. Citation command check**
```python
def check_latex_citations(tex_content):
    """Check LaTeX citation commands"""
    import re

    # Find all citation commands
    cite_pattern = r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}'
    citations = re.findall(cite_pattern, tex_content)

    # Expand multiple citations
    all_keys = []
    for cite in citations:
        keys = [k.strip() for k in cite.split(',')]
        all_keys.extend(keys)

    return all_keys
```

**2. Citation consistency check**
```python
def check_citation_consistency(tex_keys, bib_keys):
    """Check citation consistency"""
    tex_set = set(tex_keys)
    bib_set = set(bib_keys)

    # Undefined citations
    undefined = tex_set - bib_set

    # Unused citations
    unused = bib_set - tex_set

    return {
        'undefined': list(undefined),
        'unused': list(unused)
    }
```

## Layer 2: Existence Verification

### API Verification Process

**Verification steps:**
1. Select API based on citation information (DOI -> CrossRef, arXiv ID -> arXiv, other -> Semantic Scholar)
2. Call API to retrieve paper information
3. Determine whether the paper exists

**Verification results:**
- `exists` - paper exists
- `not_found` - paper does not exist
- `api_error` - API call failed, requires manual verification

### Verification Code Example

```python
def verify_existence(citation_info):
    """Verify paper existence"""
    # Prefer DOI
    if citation_info.get('doi'):
        result = verify_with_crossref(citation_info['doi'])
        if result['status'] == 'success':
            return {'exists': True, 'source': 'crossref', 'data': result['data']}

    # arXiv ID
    if citation_info.get('arxiv_id'):
        result = verify_with_arxiv(citation_info['arxiv_id'])
        if result['status'] == 'success':
            return {'exists': True, 'source': 'arxiv', 'data': result['data']}

    # General search
    if citation_info.get('title'):
        result = verify_with_semantic_scholar(citation_info['title'])
        if result['status'] == 'success' and result['data']:
            return {'exists': True, 'source': 'semantic_scholar', 'data': result['data']}

    return {'exists': False, 'source': None}
```

## Layer 3: Information Matching

### Matching Algorithms

**1. Title matching**

Uses fuzzy matching algorithm to allow minor differences:

```python
from difflib import SequenceMatcher

def match_title(title1, title2, threshold=0.85):
    """Title matching"""
    # Normalize: lowercase, remove punctuation
    def normalize(text):
        import re
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return ' '.join(text.split())

    t1 = normalize(title1)
    t2 = normalize(title2)

    # Calculate similarity
    ratio = SequenceMatcher(None, t1, t2).ratio()

    return {
        'match': ratio >= threshold,
        'similarity': ratio
    }
```

**2. Author matching**

Accounts for author order and name format differences:

```python
def match_authors(authors1, authors2, threshold=0.7):
    """Author matching"""
    def normalize_name(name):
        # Handle "Last, First" and "First Last" formats
        parts = name.replace(',', '').split()
        return ' '.join(sorted(parts)).lower()

    names1 = [normalize_name(a) for a in authors1]
    names2 = [normalize_name(a) for a in authors2]

    # Calculate intersection ratio
    set1 = set(names1)
    set2 = set(names2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)

    if union == 0:
        return {'match': False, 'similarity': 0}

    ratio = intersection / union

    return {
        'match': ratio >= threshold,
        'similarity': ratio
    }
```

**3. Year matching**

Allows a tolerance of ±1 year (accounting for preprint vs. formal publication timing):

```python
def match_year(year1, year2, tolerance=1):
    """Year matching"""
    try:
        y1 = int(year1)
        y2 = int(year2)
        diff = abs(y1 - y2)
        return {
            'match': diff <= tolerance,
            'difference': diff
        }
    except (ValueError, TypeError):
        return {'match': False, 'difference': None}
```

## Layer 4: Content Validation

### Composite Match Score

Combine all match results to calculate an overall match score:

```python
def calculate_match_score(citation, api_data):
    """Calculate composite match score"""
    scores = {}
    weights = {
        'title': 0.4,
        'authors': 0.3,
        'year': 0.2,
        'venue': 0.1
    }

    # Title match
    if citation.get('title') and api_data.get('title'):
        result = match_title(citation['title'], api_data['title'])
        scores['title'] = result['similarity']

    # Author match
    if citation.get('authors') and api_data.get('authors'):
        result = match_authors(citation['authors'], api_data['authors'])
        scores['authors'] = result['similarity']

    # Year match
    if citation.get('year') and api_data.get('year'):
        result = match_year(citation['year'], api_data['year'])
        scores['year'] = 1.0 if result['match'] else 0.0

    # Calculate weighted total score
    total_score = 0
    total_weight = 0
    for key, weight in weights.items():
        if key in scores:
            total_score += scores[key] * weight
            total_weight += weight

    if total_weight == 0:
        return 0

    return total_score / total_weight
```

### Verification Result Judgment

Determine the verification result based on the match score:

```python
def judge_verification_result(match_score):
    """Determine verification result"""
    if match_score >= 0.9:
        return {
            'status': 'verified',
            'level': 'high_confidence',
            'message': 'Verification passed - information matches completely'
        }
    elif match_score >= 0.7:
        return {
            'status': 'partial_match',
            'level': 'medium_confidence',
            'message': 'Partial match - minor differences in information, manual confirmation recommended'
        }
    elif match_score >= 0.5:
        return {
            'status': 'low_match',
            'level': 'low_confidence',
            'message': 'Low match score - significant differences in information, manual verification required'
        }
    else:
        return {
            'status': 'failed',
            'level': 'no_confidence',
            'message': 'Verification failed - information severely mismatched or paper does not exist'
        }
```

## Complete Verification Flow

### Main Verification Function

```python
def verify_citation_complete(citation):
    """Complete citation verification flow"""
    result = {
        'citation_key': citation.get('ID'),
        'layers': {}
    }

    # Layer 1: Format validation
    format_errors = check_bibtex_structure(citation)
    format_errors.extend(check_field_format(citation))
    result['layers']['format'] = {
        'passed': len(format_errors) == 0,
        'errors': format_errors
    }

    # Layer 2: Existence verification
    existence = verify_existence(citation)
    result['layers']['existence'] = existence

    if not existence['exists']:
        result['final_status'] = 'not_found'
        return result

    # Layers 3 & 4: Information matching and content validation
    api_data = existence['data']
    match_score = calculate_match_score(citation, api_data)
    judgment = judge_verification_result(match_score)

    result['layers']['matching'] = {
        'score': match_score,
        'judgment': judgment
    }

    result['final_status'] = judgment['status']
    result['confidence'] = judgment['level']

    return result
```

## Verification Threshold Configuration

### Adjustable Threshold Parameters

```python
VERIFICATION_THRESHOLDS = {
    # Matching thresholds
    'title_similarity': 0.85,      # title similarity threshold
    'author_similarity': 0.70,     # author similarity threshold
    'year_tolerance': 1,           # year tolerance

    # Judgment thresholds
    'high_confidence': 0.90,       # high confidence threshold
    'medium_confidence': 0.70,     # medium confidence threshold
    'low_confidence': 0.50,        # low confidence threshold

    # Weight configuration
    'weights': {
        'title': 0.4,
        'authors': 0.3,
        'year': 0.2,
        'venue': 0.1
    }
}
```

### Threshold Adjustment Recommendations

**Strict mode** (for formal publication):
- title_similarity: 0.90
- author_similarity: 0.80
- high_confidence: 0.95

**Lenient mode** (for drafts):
- title_similarity: 0.80
- author_similarity: 0.60
- high_confidence: 0.85
