#!/usr/bin/env python3
"""
BibTeX and LaTeX Format Checker

A standalone format checking tool for validating BibTeX and LaTeX citation formats.

Features:
1. BibTeX format check - validate entry structure, required fields, field format
2. LaTeX citation check - extract citations, check consistency
3. Quick format validation - fast check without API calls

Usage:
    python format-checker.py references.bib
    python format-checker.py paper.tex --check-latex
    python format-checker.py references.bib --strict
"""

import argparse
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# Attempt to import bibtexparser
try:
    import bibtexparser
    from bibtexparser.bparser import BibTexParser
    BIBTEX_AVAILABLE = True
except ImportError:
    print("Warning: bibtexparser not installed, BibTeX parsing is limited")
    print("Run: pip install bibtexparser")
    BIBTEX_AVAILABLE = False


class ErrorLevel(Enum):
    """Error level"""
    ERROR = "error"      # critical error, must fix
    WARNING = "warning"  # warning, recommended to fix
    INFO = "info"        # informational, optional fix


@dataclass
class FormatError:
    """Format error data class"""
    level: ErrorLevel
    location: str        # file location (e.g., "entry:smith2020" or "line:42")
    field: Optional[str] # field name (e.g., "author", "year")
    message: str         # error description
    suggestion: Optional[str] = None  # fix suggestion


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Check BibTeX and LaTeX citation formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s references.bib
  %(prog)s paper.tex --check-latex
  %(prog)s references.bib --strict --output report.txt
  %(prog)s references.bib --fix-common
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
        help='check LaTeX citations (requires a .tex file)'
    )

    parser.add_argument(
        '--strict',
        action='store_true',
        help='strict mode - treat warnings as errors'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='output report file path'
    )

    parser.add_argument(
        '--fix-common',
        action='store_true',
        help='automatically fix common format issues'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='show detailed information'
    )

    parser.add_argument(
        '--entry-type',
        type=str,
        help='only check entries of a specific type (e.g., article, inproceedings)'
    )

    return parser.parse_args()


def load_bibtex_file(file_path: str) -> List[Dict]:
    """Load BibTeX file

    Args:
        file_path: BibTeX file path

    Returns:
        list of BibTeX entries

    Raises:
        FileNotFoundError: file not found
        ValueError: file format error
    """
    if not BIBTEX_AVAILABLE:
        raise ImportError("bibtexparser required: pip install bibtexparser")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            parser = BibTexParser(common_strings=True)
            bib_database = bibtexparser.load(f, parser)
            return bib_database.entries
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Cannot parse BibTeX file: {e}")


def load_latex_file(file_path: str) -> str:
    """Load LaTeX file

    Args:
        file_path: LaTeX file path

    Returns:
        file contents

    Raises:
        FileNotFoundError: file not found
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Cannot read LaTeX file: {e}")


# ============================================================================
# BibTeX format check functions
# ============================================================================

def get_required_fields(entry_type: str) -> List[str]:
    """Get required fields for a BibTeX entry type

    Args:
        entry_type: entry type (e.g., 'article', 'inproceedings')

    Returns:
        list of required fields
    """
    required_fields = {
        'article': ['author', 'title', 'journal', 'year'],
        'inproceedings': ['author', 'title', 'booktitle', 'year'],
        'book': ['title', 'publisher', 'year'],
        'incollection': ['author', 'title', 'booktitle', 'publisher', 'year'],
        'inbook': ['author', 'title', 'chapter', 'publisher', 'year'],
        'proceedings': ['title', 'year'],
        'phdthesis': ['author', 'title', 'school', 'year'],
        'mastersthesis': ['author', 'title', 'school', 'year'],
        'techreport': ['author', 'title', 'institution', 'year'],
        'manual': ['title'],
        'misc': ['title'],
        'unpublished': ['author', 'title', 'note'],
    }
    return required_fields.get(entry_type.lower(), ['title'])


def get_optional_fields(entry_type: str) -> List[str]:
    """Get optional fields for a BibTeX entry type

    Args:
        entry_type: entry type

    Returns:
        list of optional fields
    """
    optional_fields = {
        'article': ['volume', 'number', 'pages', 'month', 'doi', 'url'],
        'inproceedings': ['editor', 'volume', 'series', 'pages', 'address',
                         'month', 'organization', 'publisher', 'doi', 'url'],
        'book': ['author', 'editor', 'volume', 'series', 'address',
                'edition', 'month', 'isbn', 'doi', 'url'],
    }
    return optional_fields.get(entry_type.lower(), [])


def check_entry_structure(entry: Dict) -> List[FormatError]:
    """Check BibTeX entry basic structure

    Args:
        entry: BibTeX entry dictionary

    Returns:
        list of errors
    """
    errors = []

    # Check entry type
    if 'ENTRYTYPE' not in entry:
        errors.append(FormatError(
            level=ErrorLevel.ERROR,
            location=f"entry:{entry.get('ID', 'unknown')}",
            field='ENTRYTYPE',
            message="Missing entry type",
            suggestion="Add an entry type such as @article, @inproceedings"
        ))
        return errors

    # Check ID
    if 'ID' not in entry or not entry['ID'].strip():
        errors.append(FormatError(
            level=ErrorLevel.ERROR,
            location="entry:unknown",
            field='ID',
            message="Missing citation key",
            suggestion="Add a unique citation key"
        ))

    # Check required fields
    entry_type = entry.get('ENTRYTYPE', '')
    required = get_required_fields(entry_type)
    for field in required:
        if field not in entry or not entry[field].strip():
            errors.append(FormatError(
                level=ErrorLevel.ERROR,
                location=f"entry:{entry.get('ID', 'unknown')}",
                field=field,
                message=f"Missing required field: {field}",
                suggestion=f"Add the {field} field"
            ))

    return errors


def check_field_formats(entry: Dict) -> List[FormatError]:
    """Check field formats

    Args:
        entry: BibTeX entry dictionary

    Returns:
        list of errors
    """
    errors = []
    entry_id = entry.get('ID', 'unknown')

    # Year format check
    if 'year' in entry:
        year = entry['year'].strip()
        if not year.isdigit():
            errors.append(FormatError(
                level=ErrorLevel.ERROR,
                location=f"entry:{entry_id}",
                field='year',
                message=f"Invalid year format: {year} (should be 4 digits)",
                suggestion="Use a 4-digit year, e.g., 2023"
            ))
        elif len(year) != 4:
            errors.append(FormatError(
                level=ErrorLevel.ERROR,
                location=f"entry:{entry_id}",
                field='year',
                message=f"Invalid year format: {year} (should be 4 digits)",
                suggestion="Use a 4-digit year, e.g., 2023"
            ))
        else:
            year_int = int(year)
            if year_int < 1900 or year_int > 2030:
                errors.append(FormatError(
                    level=ErrorLevel.WARNING,
                    location=f"entry:{entry_id}",
                    field='year',
                    message=f"Year outside reasonable range: {year}",
                    suggestion="Verify that the year is correct"
                ))

    # DOI format check
    if 'doi' in entry:
        doi = entry['doi'].strip()
        if not doi.startswith('10.'):
            errors.append(FormatError(
                level=ErrorLevel.ERROR,
                location=f"entry:{entry_id}",
                field='doi',
                message=f"Invalid DOI format: {doi}",
                suggestion="DOI should start with '10.', e.g., 10.1038/nature12345"
            ))
        # Check for URL prefix
        if 'doi.org' in doi or 'dx.doi.org' in doi:
            errors.append(FormatError(
                level=ErrorLevel.WARNING,
                location=f"entry:{entry_id}",
                field='doi',
                message=f"DOI contains URL prefix: {doi}",
                suggestion="Keep only the DOI itself, remove the https://doi.org/ prefix"
            ))

    # Author name format check
    if 'author' in entry:
        author = entry['author'].strip()
        # Check for empty value
        if not author:
            errors.append(FormatError(
                level=ErrorLevel.ERROR,
                location=f"entry:{entry_id}",
                field='author',
                message="Author field is empty",
                suggestion="Add author information"
            ))
        # Check format consistency
        elif ' and ' in author:
            authors = author.split(' and ')
            formats = []
            for a in authors:
                if ',' in a:
                    formats.append('last_first')  # "Last, First"
                else:
                    formats.append('first_last')  # "First Last"

            if len(set(formats)) > 1:
                errors.append(FormatError(
                    level=ErrorLevel.WARNING,
                    location=f"entry:{entry_id}",
                    field='author',
                    message="Inconsistent author name format",
                    suggestion="Use either 'Last, First' or 'First Last' format consistently"
                ))

    # Page number format check
    if 'pages' in entry:
        pages = entry['pages'].strip()
        # Check for correct separator
        if '-' in pages and '--' not in pages:
            errors.append(FormatError(
                level=ErrorLevel.INFO,
                location=f"entry:{entry_id}",
                field='pages',
                message=f"Pages using single hyphen: {pages}",
                suggestion="Use double hyphen '--', e.g., 123--145"
            ))

    # URL format check
    if 'url' in entry:
        url = entry['url'].strip()
        if not url.startswith(('http://', 'https://')):
            errors.append(FormatError(
                level=ErrorLevel.WARNING,
                location=f"entry:{entry_id}",
                field='url',
                message=f"URL missing protocol prefix: {url}",
                suggestion="Add http:// or https:// prefix"
            ))

    return errors


def check_consistency(entries: List[Dict]) -> List[FormatError]:
    """Check consistency between entries

    Args:
        entries: list of BibTeX entries

    Returns:
        list of errors
    """
    errors = []

    # Check for duplicate citation keys
    ids = [e.get('ID', '') for e in entries]
    duplicates = [id for id in ids if ids.count(id) > 1]
    if duplicates:
        for dup_id in set(duplicates):
            errors.append(FormatError(
                level=ErrorLevel.ERROR,
                location=f"entry:{dup_id}",
                field='ID',
                message=f"Duplicate citation key: {dup_id}",
                suggestion="Use a unique citation key"
            ))

    # Check author name format consistency
    author_formats = {}
    for entry in entries:
        if 'author' in entry and ' and ' in entry['author']:
            entry_id = entry.get('ID', 'unknown')
            authors = entry['author'].split(' and ')
            for author in authors:
                if ',' in author:
                    author_formats[entry_id] = 'last_first'
                else:
                    author_formats[entry_id] = 'first_last'
                break

    if len(set(author_formats.values())) > 1:
        errors.append(FormatError(
            level=ErrorLevel.WARNING,
            location="global",
            field='author',
            message="Different entries use different author name formats",
            suggestion="Use either 'Last, First' or 'First Last' format consistently"
        ))

    return errors


# ============================================================================
# LaTeX citation check functions
# ============================================================================

def extract_latex_citations(tex_content: str) -> List[str]:
    """Extract citations from a LaTeX file

    Args:
        tex_content: LaTeX file content

    Returns:
        list of citation keys
    """
    # Match \cite{...} commands
    cite_pattern = r'\\cite(?:\[[^\]]*\])?(?:\[[^\]]*\])?\{([^}]+)\}'
    citations = re.findall(cite_pattern, tex_content)

    # Expand multiple citations
    all_keys = []
    for cite in citations:
        keys = [k.strip() for k in cite.split(',')]
        all_keys.extend(keys)

    return list(set(all_keys))  # deduplicate


def check_latex_consistency(tex_keys: List[str], bib_keys: List[str]) -> List[FormatError]:
    """Check consistency between LaTeX citations and BibTeX

    Args:
        tex_keys: list of citation keys in LaTeX
        bib_keys: list of keys in BibTeX

    Returns:
        list of errors
    """
    errors = []

    tex_set = set(tex_keys)
    bib_set = set(bib_keys)

    # Undefined citations
    undefined = tex_set - bib_set
    if undefined:
        for key in sorted(undefined):
            errors.append(FormatError(
                level=ErrorLevel.ERROR,
                location=f"latex:cite",
                field=key,
                message=f"Undefined citation: {key}",
                suggestion=f"Add a {key} entry to the BibTeX file"
            ))

    # Unused citations
    unused = bib_set - tex_set
    if unused:
        for key in sorted(unused):
            errors.append(FormatError(
                level=ErrorLevel.WARNING,
                location=f"bibtex:entry",
                field=key,
                message=f"Unused citation: {key}",
                suggestion=f"Cite {key} in the LaTeX file or remove it from BibTeX"
            ))

    return errors


# ============================================================================
# Report generation functions
# ============================================================================

def print_errors(errors: List[FormatError], verbose: bool = False):
    """Print list of errors

    Args:
        errors: list of errors
        verbose: whether to show detailed information
    """
    if not errors:
        print("No format errors found")
        return

    # Group by level
    errors_by_level = {
        ErrorLevel.ERROR: [],
        ErrorLevel.WARNING: [],
        ErrorLevel.INFO: []
    }

    for error in errors:
        errors_by_level[error.level].append(error)

    # Print summary
    print("\n" + "="*60)
    print("Format Check Results")
    print("="*60)
    print(f"Errors: {len(errors_by_level[ErrorLevel.ERROR])}")
    print(f"Warnings: {len(errors_by_level[ErrorLevel.WARNING])}")
    print(f"Info: {len(errors_by_level[ErrorLevel.INFO])}")
    print("="*60)

    # Print detailed errors
    for level in [ErrorLevel.ERROR, ErrorLevel.WARNING, ErrorLevel.INFO]:
        level_errors = errors_by_level[level]
        if not level_errors:
            continue

        level_label = {
            ErrorLevel.ERROR: "ERROR",
            ErrorLevel.WARNING: "WARNING",
            ErrorLevel.INFO: "INFO"
        }[level]

        print(f"\n{level_label} ({len(level_errors)}):\n")

        for error in level_errors:
            print(f"  [{error.location}]", end="")
            if error.field:
                print(f" {error.field}:", end="")
            print(f" {error.message}")

            if verbose and error.suggestion:
                print(f"    Suggestion: {error.suggestion}")
            print()


def generate_report(errors: List[FormatError], output_file: str):
    """Generate a text format check report

    Args:
        errors: list of errors
        output_file: output file path
    """
    # Group by level
    errors_by_level = {
        ErrorLevel.ERROR: [],
        ErrorLevel.WARNING: [],
        ErrorLevel.INFO: []
    }

    for error in errors:
        errors_by_level[error.level].append(error)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# BibTeX/LaTeX Format Check Report\n\n")

        # Overall statistics
        f.write("## Summary\n\n")
        f.write(f"- **Errors**: {len(errors_by_level[ErrorLevel.ERROR])}\n")
        f.write(f"- **Warnings**: {len(errors_by_level[ErrorLevel.WARNING])}\n")
        f.write(f"- **Info**: {len(errors_by_level[ErrorLevel.INFO])}\n\n")

        # Detailed errors
        for level in [ErrorLevel.ERROR, ErrorLevel.WARNING, ErrorLevel.INFO]:
            level_errors = errors_by_level[level]
            if not level_errors:
                continue

            level_name = {
                ErrorLevel.ERROR: "Errors",
                ErrorLevel.WARNING: "Warnings",
                ErrorLevel.INFO: "Info"
            }[level]

            f.write(f"## {level_name} ({len(level_errors)})\n\n")

            for error in level_errors:
                f.write(f"### [{error.location}]")
                if error.field:
                    f.write(f" {error.field}")
                f.write("\n\n")
                f.write(f"**Problem**: {error.message}\n\n")
                if error.suggestion:
                    f.write(f"**Suggestion**: {error.suggestion}\n\n")

    print(f"\nReport saved to: {output_file}")
