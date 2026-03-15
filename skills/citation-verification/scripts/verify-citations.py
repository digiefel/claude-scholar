#!/usr/bin/env python3
"""
Citation Verification Script

Four-layer verification mechanism:
1. Format Validation - BibTeX format check
2. Existence Verification - API verification of paper existence
3. Information Matching - information matching (title, authors, year)
4. Content Validation - composite scoring and judgment

Usage:
    python verify-citations.py references.bib
    python verify-citations.py paper.tex --check-latex
    python verify-citations.py references.bib --verbose --output report.md
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import re
from difflib import SequenceMatcher

# Try to import bibtexparser
try:
    import bibtexparser
    from bibtexparser.bparser import BibTexParser
except ImportError:
    print("Error: bibtexparser is required")
    print("Run: pip install bibtexparser")
    sys.exit(1)

# Try to import API client libraries
try:
    from semanticscholar import SemanticScholar
except ImportError:
    print("Warning: semanticscholar not installed, Semantic Scholar verification will be skipped")
    print("Run: pip install semanticscholar")

try:
    import arxiv
except ImportError:
    print("Warning: arxiv not installed, arXiv verification will be skipped")
    print("Run: pip install arxiv")

try:
    import requests
except ImportError:
    print("Error: requests is required")
    print("Run: pip install requests")
    sys.exit(1)


@dataclass
class VerificationResult:
    """Verification result data class"""
    citation_key: str
    status: str  # verified, partial_match, low_match, failed, not_found
    confidence: str  # high_confidence, medium_confidence, low_confidence, no_confidence
    match_score: float
    format_errors: List[str]
    api_source: Optional[str]  # crossref, arxiv, semantic_scholar
    message: str


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Verify the accuracy and completeness of BibTeX citations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s references.bib
  %(prog)s paper.tex --check-latex
  %(prog)s references.bib --verbose --output report.md
  %(prog)s references.bib --api-only
        """
    )

    parser.add_argument(
        'input_file',
        type=str,
        help='BibTeX file (.bib) or LaTeX file (.tex)'
    )

    parser.add_argument(
        '--check-latex',
        action='store_true',
        help='Check LaTeX citation consistency (requires a .tex file)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed verification information'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='Output report file path (Markdown format)'
    )

    parser.add_argument(
        '--api-only',
        action='store_true',
        help='Perform API verification only, skip format check'
    )

    parser.add_argument(
        '--format-only',
        action='store_true',
        help='Perform format check only, skip API verification'
    )

    parser.add_argument(
        '--threshold',
        type=float,
        default=0.85,
        help='Match threshold (0.0-1.0), default 0.85'
    )

    return parser.parse_args()


def load_bibtex(file_path: str) -> List[Dict]:
    """Load a BibTeX file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            parser = BibTexParser(common_strings=True)
            bib_database = bibtexparser.load(f, parser)
            return bib_database.entries
    except FileNotFoundError:
        print(f"Error: file does not exist: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: cannot parse BibTeX file: {e}")
        sys.exit(1)


def extract_latex_citations(tex_file: str) -> List[str]:
    """Extract citations from a LaTeX file"""
    try:
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match \cite{...} commands
        cite_pattern = r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}'
        citations = re.findall(cite_pattern, content)

        # Expand multiple citations
        all_keys = []
        for cite in citations:
            keys = [k.strip() for k in cite.split(',')]
            all_keys.extend(keys)

        return list(set(all_keys))  # deduplicate
    except FileNotFoundError:
        print(f"Error: file does not exist: {tex_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: cannot parse LaTeX file: {e}")
        sys.exit(1)


# ============================================================================
# Layer 1: Format Validation
# ============================================================================

def get_required_fields(entry_type: str) -> List[str]:
    """Get required fields for a BibTeX entry type"""
    required_fields = {
        'article': ['author', 'title', 'journal', 'year'],
        'inproceedings': ['author', 'title', 'booktitle', 'year'],
        'book': ['title', 'publisher', 'year'],
        'misc': ['title'],
        'phdthesis': ['author', 'title', 'school', 'year'],
        'mastersthesis': ['author', 'title', 'school', 'year'],
        'techreport': ['author', 'title', 'institution', 'year'],
    }
    return required_fields.get(entry_type.lower(), ['title'])


def check_bibtex_format(entry: Dict) -> List[str]:
    """Check BibTeX entry format

    Returns:
        List of errors
    """
    errors = []

    # Check entry type
    if 'ENTRYTYPE' not in entry:
        errors.append("Missing entry type")
        return errors

    # Check ID
    if 'ID' not in entry:
        errors.append("Missing citation key")

    # Check required fields
    entry_type = entry.get('ENTRYTYPE', '')
    required = get_required_fields(entry_type)
    for field in required:
        if field not in entry or not entry[field].strip():
            errors.append(f"Missing required field: {field}")

    # Year format check
    if 'year' in entry:
        year = entry['year'].strip()
        if not year.isdigit() or len(year) != 4:
            errors.append(f"Invalid year format: {year}")
        else:
            year_int = int(year)
            if year_int < 1900 or year_int > 2030:
                errors.append(f"Year out of reasonable range: {year}")

    # DOI format check
    if 'doi' in entry:
        doi = entry['doi'].strip()
        if not doi.startswith('10.'):
            errors.append(f"Invalid DOI format: {doi}")

    return errors


def check_citation_consistency(tex_keys: List[str], bib_keys: List[str]) -> Dict:
    """Check consistency between LaTeX citations and BibTeX entries

    Returns:
        {'undefined': [...], 'unused': [...]}
    """
    tex_set = set(tex_keys)
    bib_set = set(bib_keys)

    return {
        'undefined': list(tex_set - bib_set),
        'unused': list(bib_set - tex_set)
    }


# ============================================================================
# Layer 2: Existence Verification
# ============================================================================

def verify_with_crossref(doi: str) -> Optional[Dict]:
    """Verify a DOI via the CrossRef API"""
    try:
        url = f"https://api.crossref.org/works/{doi}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('message')
        return None
    except Exception as e:
        print(f"CrossRef API error: {e}")
        return None


def verify_with_arxiv(arxiv_id: str) -> Optional[Dict]:
    """Verify via the arXiv API"""
    try:
        search = arxiv.Search(id_list=[arxiv_id])
        paper = next(search.results())
        return {
            'title': paper.title,
            'authors': [a.name for a in paper.authors],
            'year': paper.published.year,
            'arxiv_id': arxiv_id
        }
    except Exception as e:
        print(f"arXiv API error: {e}")
        return None


def verify_with_semantic_scholar(title: str, authors: Optional[List[str]] = None) -> Optional[Dict]:
    """Verify via the Semantic Scholar API"""
    try:
        sch = SemanticScholar()
        results = sch.search_paper(title, limit=5)

        if not results:
            return None

        # Return the first result
        paper = results[0]
        return {
            'title': paper.title,
            'authors': [a.name for a in paper.authors] if paper.authors else [],
            'year': paper.year,
            'paperId': paper.paperId
        }
    except Exception as e:
        print(f"Semantic Scholar API error: {e}")
        return None


def verify_existence(entry: Dict) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """Verify paper existence

    Returns:
        (exists, api_source, api_data)
    """
    # Strategy 1: DOI first
    if 'doi' in entry:
        data = verify_with_crossref(entry['doi'])
        if data:
            return True, 'crossref', data

    # Strategy 2: arXiv ID
    if 'eprint' in entry or 'arxiv' in entry.get('note', '').lower():
        arxiv_id = entry.get('eprint', '')
        if not arxiv_id:
            # Try to extract from note field
            match = re.search(r'arXiv:(\d{4}\.\d{4,5})', entry.get('note', ''))
            if match:
                arxiv_id = match.group(1)

        if arxiv_id:
            data = verify_with_arxiv(arxiv_id)
            if data:
                return True, 'arxiv', data

    # Strategy 3: general search
    if 'title' in entry:
        authors = entry.get('author', '').split(' and ') if 'author' in entry else None
        data = verify_with_semantic_scholar(entry['title'], authors)
        if data:
            return True, 'semantic_scholar', data

    return False, None, None


# ============================================================================
# Layer 3 & 4: Information Matching & Content Validation
# ============================================================================

def normalize_text(text: str) -> str:
    """Normalize text for matching"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return ' '.join(text.split())


def match_title(title1: str, title2: str, threshold: float = 0.85) -> Dict:
    """Match titles"""
    t1 = normalize_text(title1)
    t2 = normalize_text(title2)

    ratio = SequenceMatcher(None, t1, t2).ratio()

    return {
        'match': ratio >= threshold,
        'similarity': ratio
    }


def normalize_author_name(name: str) -> str:
    """Normalize an author name"""
    parts = name.replace(',', '').split()
    return ' '.join(sorted(parts)).lower()


def match_authors(authors1: List[str], authors2: List[str], threshold: float = 0.7) -> Dict:
    """Match author lists"""
    names1 = [normalize_author_name(a) for a in authors1]
    names2 = [normalize_author_name(a) for a in authors2]

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


def match_year(year1: str, year2: int, tolerance: int = 1) -> Dict:
    """Match years"""
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


def calculate_match_score(entry: Dict, api_data: Dict, threshold: float) -> float:
    """Calculate composite match score"""
    scores = {}
    weights = {
        'title': 0.4,
        'authors': 0.3,
        'year': 0.2,
        'venue': 0.1
    }

    # Title matching
    if 'title' in entry and 'title' in api_data:
        result = match_title(entry['title'], api_data['title'], threshold)
        scores['title'] = result['similarity']

    # Author matching
    if 'author' in entry and 'authors' in api_data:
        entry_authors = entry['author'].split(' and ')
        result = match_authors(entry_authors, api_data['authors'])
        scores['authors'] = result['similarity']

    # Year matching
    if 'year' in entry and 'year' in api_data:
        result = match_year(entry['year'], api_data['year'])
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


def judge_verification_result(match_score: float) -> Dict:
    """Determine the verification result"""
    if match_score >= 0.9:
        return {
            'status': 'verified',
            'level': 'high_confidence',
            'message': '✅ Verified - information fully matches'
        }
    elif match_score >= 0.7:
        return {
            'status': 'partial_match',
            'level': 'medium_confidence',
            'message': '⚠️ Partial match - minor information discrepancies, manual review recommended'
        }
    elif match_score >= 0.5:
        return {
            'status': 'low_match',
            'level': 'low_confidence',
            'message': '❌ Low match - significant information discrepancies, manual verification required'
        }
    else:
        return {
            'status': 'failed',
            'level': 'no_confidence',
            'message': '❌ Verification failed - severe information mismatch or paper does not exist'
        }


def verify_citation(entry: Dict, args) -> VerificationResult:
    """Complete citation verification workflow"""
    citation_key = entry.get('ID', 'unknown')

    # Layer 1: Format validation
    format_errors = []
    if not args.api_only:
        format_errors = check_bibtex_format(entry)

    # Layer 2: Existence verification
    if args.format_only:
        return VerificationResult(
            citation_key=citation_key,
            status='format_checked',
            confidence='n/a',
            match_score=0.0,
            format_errors=format_errors,
            api_source=None,
            message='Format check only'
        )

    exists, api_source, api_data = verify_existence(entry)

    if not exists:
        return VerificationResult(
            citation_key=citation_key,
            status='not_found',
            confidence='no_confidence',
            match_score=0.0,
            format_errors=format_errors,
            api_source=None,
            message='❌ Paper not found - cannot be verified via any API'
        )

    # Layer 3 & 4: Information matching and content validation
    match_score = calculate_match_score(entry, api_data, args.threshold)
    judgment = judge_verification_result(match_score)

    return VerificationResult(
        citation_key=citation_key,
        status=judgment['status'],
        confidence=judgment['level'],
        match_score=match_score,
        format_errors=format_errors,
        api_source=api_source,
        message=judgment['message']
    )


# ============================================================================
# Report Generation
# ============================================================================

def print_summary(results: List[VerificationResult], verbose: bool = False):
    """Print verification summary"""
    total = len(results)
    verified = sum(1 for r in results if r.status == 'verified')
    partial = sum(1 for r in results if r.status == 'partial_match')
    low = sum(1 for r in results if r.status == 'low_match')
    failed = sum(1 for r in results if r.status in ['failed', 'not_found'])

    print("\n" + "="*60)
    print("Verification Summary")
    print("="*60)
    print(f"Total citations: {total}")
    print(f"✅ Verified: {verified} ({verified/total*100:.1f}%)")
    print(f"⚠️  Partial match: {partial} ({partial/total*100:.1f}%)")
    print(f"❌ Low match: {low} ({low/total*100:.1f}%)")
    print(f"❌ Verification failed: {failed} ({failed/total*100:.1f}%)")
    print("="*60)

    if verbose:
        print("\nDetailed Results:\n")
        for result in results:
            print(f"[{result.citation_key}]")
            print(f"  Status: {result.message}")
            print(f"  Match score: {result.match_score:.2f}")
            if result.api_source:
                print(f"  Verification source: {result.api_source}")
            if result.format_errors:
                print(f"  Format errors: {', '.join(result.format_errors)}")
            print()


def generate_markdown_report(results: List[VerificationResult], output_file: str):
    """Generate a Markdown format verification report"""
    total = len(results)
    verified = sum(1 for r in results if r.status == 'verified')
    partial = sum(1 for r in results if r.status == 'partial_match')
    low = sum(1 for r in results if r.status == 'low_match')
    failed = sum(1 for r in results if r.status in ['failed', 'not_found'])

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Citation Verification Report\n\n")

        # Overall statistics
        f.write("## Overall Statistics\n\n")
        f.write(f"- **Total citations**: {total}\n")
        f.write(f"- **✅ Verified**: {verified} ({verified/total*100:.1f}%)\n")
        f.write(f"- **⚠️ Partial match**: {partial} ({partial/total*100:.1f}%)\n")
        f.write(f"- **❌ Low match**: {low} ({low/total*100:.1f}%)\n")
        f.write(f"- **❌ Verification failed**: {failed} ({failed/total*100:.1f}%)\n\n")

        # Detailed results
        f.write("## Detailed Results\n\n")

        # Group by status
        for status, emoji, title in [
            ('verified', '✅', 'Verified'),
            ('partial_match', '⚠️', 'Partial Match'),
            ('low_match', '❌', 'Low Match'),
            ('failed', '❌', 'Verification Failed'),
            ('not_found', '❌', 'Paper Not Found')
        ]:
            status_results = [r for r in results if r.status == status]
            if status_results:
                f.write(f"### {emoji} {title} ({len(status_results)})\n\n")
                for result in status_results:
                    f.write(f"#### `{result.citation_key}`\n\n")
                    f.write(f"- **Status**: {result.message}\n")
                    f.write(f"- **Match score**: {result.match_score:.2f}\n")
                    f.write(f"- **Confidence**: {result.confidence}\n")
                    if result.api_source:
                        f.write(f"- **Verification source**: {result.api_source}\n")
                    if result.format_errors:
                        f.write(f"- **Format errors**:\n")
                        for error in result.format_errors:
                            f.write(f"  - {error}\n")
                    f.write("\n")

        # Recommended actions
        f.write("## Recommended Actions\n\n")
        if failed > 0:
            f.write("### Citations Requiring Correction\n\n")
            failed_results = [r for r in results if r.status in ['failed', 'not_found']]
            for result in failed_results:
                f.write(f"- `{result.citation_key}`: {result.message}\n")
            f.write("\n")

        if partial > 0 or low > 0:
            f.write("### Citations Requiring Manual Review\n\n")
            check_results = [r for r in results if r.status in ['partial_match', 'low_match']]
            for result in check_results:
                f.write(f"- `{result.citation_key}`: {result.message}\n")
            f.write("\n")

    print(f"\nReport saved to: {output_file}")


# ============================================================================
# Main Function
# ============================================================================

def main():
    """Main function"""
    args = parse_arguments()

    # Load BibTeX file
    print(f"Loading BibTeX file: {args.input_file}")
    entries = load_bibtex(args.input_file)
    print(f"Found {len(entries)} citation entries")

    # LaTeX consistency check
    if args.check_latex:
        tex_file = args.input_file.replace('.bib', '.tex')
        if Path(tex_file).exists():
            print(f"\nChecking LaTeX citation consistency: {tex_file}")
            tex_keys = extract_latex_citations(tex_file)
            bib_keys = [e['ID'] for e in entries]
            consistency = check_citation_consistency(tex_keys, bib_keys)

            if consistency['undefined']:
                print(f"⚠️  Undefined citations ({len(consistency['undefined'])}): {', '.join(consistency['undefined'])}")
            if consistency['unused']:
                print(f"⚠️  Unused citations ({len(consistency['unused'])}): {', '.join(consistency['unused'])}")
            if not consistency['undefined'] and not consistency['unused']:
                print("✅ LaTeX citations and BibTeX entries are fully consistent")

    # Verify each citation
    print("\nStarting citation verification...")
    results = []
    for i, entry in enumerate(entries, 1):
        citation_key = entry.get('ID', 'unknown')
        print(f"[{i}/{len(entries)}] Verifying {citation_key}...", end=' ')

        result = verify_citation(entry, args)
        results.append(result)

        # Short status output
        if result.status == 'verified':
            print("✅")
        elif result.status == 'partial_match':
            print("⚠️")
        else:
            print("❌")

    # Print summary
    print_summary(results, args.verbose)

    # Generate report
    if args.output:
        generate_markdown_report(results, args.output)

    # Return exit code
    failed_count = sum(1 for r in results if r.status in ['failed', 'not_found'])
    return 0 if failed_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
