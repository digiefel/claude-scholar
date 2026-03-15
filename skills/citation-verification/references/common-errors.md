# Common Citation Error Patterns

This document summarizes common types of citation errors, how to identify them, and how to fix them.

## Error Categories

### 1. Format Errors

#### 1.1 Missing Required Fields

**Error example:**
```bibtex
@article{smith2020,
  title={Deep Learning for NLP},
  year={2020}
}
```

**Problem:** Missing `author` and `journal` fields

**Fix:**
```bibtex
@article{smith2020,
  author={Smith, John and Doe, Jane},
  title={Deep Learning for NLP},
  journal={Nature},
  year={2020}
}
```

#### 1.2 Year Format Errors

**Error examples:**
```bibtex
year={20}          # incomplete year
year={2020-2021}   # year range format error
year={circa 2020}  # contains non-numeric characters
```

**Fix:**
```bibtex
year={2020}        # use four-digit year
```

#### 1.3 DOI Format Errors

**Error examples:**
```bibtex
doi={doi:10.1038/nature12345}     # contains "doi:" prefix
doi={https://doi.org/10.1038/...} # contains full URL
doi={10.1038/nature12345.}        # trailing period
```

**Fix:**
```bibtex
doi={10.1038/nature12345}         # keep only the DOI itself
```

#### 1.4 Inconsistent Author Name Format

**Error examples:**
```bibtex
author={John Smith and Jane Doe and Bob}  # inconsistent format
author={Smith, J. and Doe, Jane}          # mixed format
```

**Fix:**
```bibtex
author={Smith, John and Doe, Jane and Brown, Bob}  # unified format
# or
author={Smith, J. and Doe, J. and Brown, B.}       # unified abbreviation
```

### 2. Information Errors

#### 2.1 Misspelled Author Names

**Error example:**
```bibtex
author={Vaswani, Ashish}  # correct
author={Vaswani, Asish}   # misspelling
```

**Identification:**
- Low author match score in API verification
- Search on Google Scholar to confirm correct spelling

**Fix recommendations:**
- Get BibTeX from reliable sources (Google Scholar, Semantic Scholar)
- Carefully verify author name spelling

#### 2.2 Title Errors

**Error examples:**
```bibtex
title={Attention is All You Need}           # correct
title={Attention Is All You Need}           # capitalization error
title={Attention is all you need}           # capitalization error
title={Attention Mechanism for Transformers} # completely wrong title
```

**Identification:**
- Title match score below threshold
- Title returned by API does not match BibTeX

**Fix recommendations:**
- Get the accurate title from the original paper or DOI
- Preserve the original capitalization format

#### 2.3 Year Errors

**Common situations:**
- Using the preprint year instead of the formal publication year
- Using the conference year instead of the proceedings publication year

**Error example:**
```bibtex
# Paper published on arXiv in 2017, officially at NeurIPS in 2018
year={2017}  # used preprint year
year={2018}  # correct: use official publication year
```

**Fix recommendations:**
- Prefer the formal publication year
- If citing a preprint, note this in the note field

#### 2.4 Journal/Conference Name Errors

**Error examples:**
```bibtex
booktitle={NeurIPS}                    # abbreviation
booktitle={Neural Information Processing Systems}  # incomplete name
booktitle={Advances in Neural Information Processing Systems}  # correct full name
```

**Fix recommendations:**
- Use the official full name or standard abbreviation
- Maintain consistent naming throughout the reference list

### 3. Fake Citations

#### 3.1 Completely Fabricated Papers

**Characteristics:**
- Paper does not exist in any database
- All API verifications fail
- Cannot be found via Google Scholar

**Identification:**
```python
# All APIs return not_found
if not crossref_found and not arxiv_found and not semantic_scholar_found:
    return "possibly fake citation"
```

**Fix recommendations:**
- Remove the fake citation
- If a citation is truly needed, find a real related paper

#### 3.2 Citations with Severely Wrong Information

**Characteristics:**
- Paper exists but information does not match at all
- Author, title, and year are all wrong
- Likely a copy-paste error

**Error example:**
```bibtex
@article{smith2020deep,
  author={Smith, John},
  title={Deep Learning for NLP},
  journal={Nature},
  year={2020}
}
```

**Actual paper:**
- Author: Brown, Tom et al.
- Title: Language Models are Few-Shot Learners
- Venue: NeurIPS
- Year: 2020

**Fix recommendations:**
- Search again for the correct paper
- Get the correct BibTeX from a reliable source

#### 3.3 Citing Non-existent Versions

**Error example:**
```bibtex
# Citing a journal version that does not exist
@article{vaswani2017attention,
  author={Vaswani, Ashish and others},
  title={Attention is All You Need},
  journal={Nature Machine Intelligence},  # wrong: this paper has no journal version
  year={2017}
}
```

**Correct citation:**
```bibtex
@inproceedings{vaswani2017attention,
  author={Vaswani, Ashish and others},
  title={Attention is All You Need},
  booktitle={Advances in Neural Information Processing Systems},
  year={2017}
}
```

### 4. Consistency Errors

#### 4.1 LaTeX Citation and BibTeX Mismatch

**Error example:**

LaTeX file:
```latex
\cite{smith2020deep}
```

BibTeX file:
```bibtex
@article{smith2020deeplearning,  # key does not match
  author={Smith, John},
  title={Deep Learning for NLP},
  year={2020}
}
```

**Identification:**
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

**Fix recommendations:**
- Ensure citation keys in LaTeX exactly match IDs in BibTeX
- Delete unused BibTeX entries
- Add missing BibTeX entries

#### 4.2 Inconsistent Citation Format

**Error example:**
```bibtex
# Mixed formats in the same reference list
@article{paper1,
  author={Smith, John and Doe, Jane},  # full name
  ...
}

@article{paper2,
  author={Brown, T. and Lee, S.},      # abbreviation
  ...
}

@article{paper3,
  author={John Wilson and Mary Johnson},  # First Last format
  ...
}
```

**Fix recommendations:**
- Unify author name format (full name or abbreviation)
- Unify journal/conference name format (full name or standard abbreviation)
- Unify page number format (1-10 or 1--10)

#### 4.3 Duplicate Citations

**Error example:**
```bibtex
@article{vaswani2017,
  author={Vaswani, Ashish and others},
  title={Attention is All You Need},
  booktitle={NeurIPS},
  year={2017}
}

@inproceedings{vaswani2017attention,
  author={Vaswani, A. and others},
  title={Attention is All You Need},
  booktitle={Advances in Neural Information Processing Systems},
  year={2017}
}
```

**Problem:** The same paper is cited twice with different citation keys

**Identification:**
- Titles are highly similar (similarity > 0.9)
- High author overlap
- Same year

**Fix recommendations:**
- Keep the more complete and accurate entry
- Delete the duplicate entry
- Update citations in the LaTeX file

## Best Practices for Error Prevention

### 1. Use Reliable Sources

Recommended sources:
- Google Scholar - get BibTeX
- Semantic Scholar - verify paper information
- Official publisher websites - get accurate metadata
- DOI system - most reliable identifier

Avoid:
- Manually entering BibTeX
- Copying from unreliable websites
- Using outdated citation management tools

### 2. Verify Promptly

**When to verify:**
- Verify immediately after adding a citation
- Comprehensive verification after completing a draft
- Final verification before submission

**What to verify:**
- Format completeness
- Information accuracy
- Citation consistency

### 3. Maintain Consistency

**Unified standards:**
- Consistent author name format (full name or abbreviation)
- Consistent journal/conference name format (full name or standard abbreviation)
- Consistent page number format
- Consistent capitalization rules

### 4. Use Tools

**Recommended tools:**
- BibTeX format checker
- LaTeX compiler (detects undefined citations)
- Citation verification scripts
- Reference management software (Zotero, Mendeley)

## Common Errors Summary

| Error Type | Severity | Detection Difficulty | Fix Difficulty |
|-----------|----------|---------------------|----------------|
| Missing required fields | High | Low | Low |
| Year format error | Medium | Low | Low |
| DOI format error | Medium | Low | Low |
| Misspelled author name | High | Medium | Medium |
| Title error | High | Medium | Medium |
| Completely fabricated paper | Critical | High | High |
| Severely wrong information | Critical | Medium | High |
| LaTeX-BibTeX mismatch | High | Low | Low |
| Inconsistent format | Low | Low | Medium |
| Duplicate citation | Medium | Medium | Medium |

## Quick Verification Checklist

Before submitting a paper, ensure the following checks are complete:

- [ ] All BibTeX entries contain required fields
- [ ] Year format is correct (four digits)
- [ ] DOI format is correct (no prefix, no URL)
- [ ] Author name format is consistent
- [ ] Title capitalization is correct
- [ ] All citations pass API verification
- [ ] LaTeX citations are consistent with BibTeX
- [ ] No duplicate citations
- [ ] Consistent format (author names, journal names, page numbers)
- [ ] No fake or severely erroneous citations

Following these best practices can effectively prevent common citation errors and improve paper quality and credibility.
