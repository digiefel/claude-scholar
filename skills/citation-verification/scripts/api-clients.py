#!/usr/bin/env python3
"""
API Clients for Citation Verification

Provides three main API clients:
1. CrossRefClient - DOI verification
2. ArXivClient - arXiv paper verification
3. SemanticScholarClient - general academic search

Each client includes:
- Error handling
- Retry mechanism
- Rate limiting
- Result normalization
"""

import time
import requests
from typing import Dict, List, Optional
from abc import ABC, abstractmethod


class RateLimiter:
    """Rate limiter"""

    def __init__(self, calls_per_minute: int):
        self.calls_per_minute = calls_per_minute
        self.last_call = 0
        self.min_interval = 60.0 / calls_per_minute

    def wait_if_needed(self):
        """Wait if necessary to satisfy rate limit"""
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()


class APIClient(ABC):
    """Base API client class"""

    def __init__(self, rate_limit: int = 20):
        """
        Args:
            rate_limit: maximum requests per minute
        """
        self.rate_limiter = RateLimiter(rate_limit)

    @abstractmethod
    def search(self, **kwargs) -> Optional[Dict]:
        """Search for a paper"""
        pass

    def _retry_request(self, func, max_retries: int = 3):
        """Request with retry"""
        for i in range(max_retries):
            try:
                self.rate_limiter.wait_if_needed()
                return func()
            except requests.exceptions.RequestException as e:
                if i == max_retries - 1:
                    raise
                time.sleep(2 ** i)  # exponential backoff
        return None


class CrossRefClient(APIClient):
    """CrossRef API client

    Used to verify paper information via DOI

    API documentation: https://api.crossref.org/
    """

    def __init__(self, rate_limit: int = 50):
        """
        Args:
            rate_limit: maximum requests per minute (CrossRef limits are more lenient)
        """
        super().__init__(rate_limit)
        self.base_url = "https://api.crossref.org"

    def search_by_doi(self, doi: str) -> Optional[Dict]:
        """Search for a paper by DOI

        Args:
            doi: DOI identifier (e.g., 10.1038/nature12345)

        Returns:
            Normalized paper information dictionary, or None if not found
        """
        def request():
            url = f"{self.base_url}/works/{doi}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()

        try:
            data = self._retry_request(request)
            if data and 'message' in data:
                return self._normalize_result(data['message'])
            return None
        except Exception as e:
            print(f"CrossRef API error: {e}")
            return None

    def search(self, doi: str = None, **kwargs) -> Optional[Dict]:
        """Search for a paper (unified interface)"""
        if doi:
            return self.search_by_doi(doi)
        return None

    def _normalize_result(self, data: Dict) -> Dict:
        """Normalize CrossRef response"""
        # Extract title
        title = data.get('title', [''])[0] if 'title' in data else ''

        # Extract authors
        authors = []
        if 'author' in data:
            for author in data['author']:
                given = author.get('given', '')
                family = author.get('family', '')
                if given and family:
                    authors.append(f"{given} {family}")
                elif family:
                    authors.append(family)

        # Extract year
        year = None
        if 'published' in data:
            date_parts = data['published'].get('date-parts', [[]])[0]
            if date_parts:
                year = date_parts[0]
        elif 'created' in data:
            date_parts = data['created'].get('date-parts', [[]])[0]
            if date_parts:
                year = date_parts[0]

        # Extract journal/conference name
        venue = ''
        if 'container-title' in data:
            venue = data['container-title'][0] if data['container-title'] else ''

        return {
            'title': title,
            'authors': authors,
            'year': year,
            'venue': venue,
            'doi': data.get('DOI', ''),
            'type': data.get('type', ''),
            'source': 'crossref'
        }

    def get_bibtex(self, doi: str) -> Optional[str]:
        """Get BibTeX by DOI

        Args:
            doi: DOI identifier

        Returns:
            BibTeX string, or None if failed
        """
        def request():
            url = f"https://doi.org/{doi}"
            headers = {"Accept": "application/x-bibtex"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text

        try:
            return self._retry_request(request)
        except Exception as e:
            print(f"Failed to get BibTeX: {e}")
            return None


class ArXivClient(APIClient):
    """arXiv API client

    Used to verify arXiv preprint papers

    API documentation: https://info.arxiv.org/help/api/
    """

    def __init__(self, rate_limit: int = 20):
        """
        Args:
            rate_limit: maximum requests per minute
        """
        super().__init__(rate_limit)
        try:
            import arxiv
            self.arxiv = arxiv
        except ImportError:
            raise ImportError("arxiv library required: pip install arxiv")

    def search_by_id(self, arxiv_id: str) -> Optional[Dict]:
        """Search for a paper by arXiv ID

        Args:
            arxiv_id: arXiv identifier (e.g., 2301.12345 or cs/0703001)

        Returns:
            Normalized paper information dictionary, or None if not found
        """
        def request():
            search = self.arxiv.Search(id_list=[arxiv_id])
            paper = next(search.results())
            return paper

        try:
            self.rate_limiter.wait_if_needed()
            paper = request()
            return self._normalize_result(paper)
        except StopIteration:
            print(f"arXiv paper not found: {arxiv_id}")
            return None
        except Exception as e:
            print(f"arXiv API error: {e}")
            return None

    def search_by_title(self, title: str, max_results: int = 5) -> Optional[Dict]:
        """Search for a paper by title

        Args:
            title: paper title
            max_results: maximum number of results to return

        Returns:
            Normalized paper information dictionary (first result), or None if not found
        """
        def request():
            search = self.arxiv.Search(
                query=f'ti:"{title}"',
                max_results=max_results,
                sort_by=self.arxiv.SortCriterion.Relevance
            )
            results = list(search.results())
            return results[0] if results else None

        try:
            self.rate_limiter.wait_if_needed()
            paper = request()
            if paper:
                return self._normalize_result(paper)
            return None
        except Exception as e:
            print(f"arXiv API error: {e}")
            return None

    def search(self, arxiv_id: str = None, title: str = None, **kwargs) -> Optional[Dict]:
        """Search for a paper (unified interface)"""
        if arxiv_id:
            return self.search_by_id(arxiv_id)
        elif title:
            return self.search_by_title(title)
        return None

    def _normalize_result(self, paper) -> Dict:
        """Normalize arXiv response"""
        # Extract arXiv ID
        arxiv_id = paper.entry_id.split('/')[-1]

        return {
            'title': paper.title,
            'authors': [a.name for a in paper.authors],
            'year': paper.published.year,
            'venue': 'arXiv',
            'arxiv_id': arxiv_id,
            'doi': paper.doi if hasattr(paper, 'doi') else None,
            'abstract': paper.summary,
            'pdf_url': paper.pdf_url,
            'source': 'arxiv'
        }

    @staticmethod
    def extract_arxiv_id(text: str) -> Optional[str]:
        """Extract arXiv ID from text

        Args:
            text: text containing an arXiv ID

        Returns:
            arXiv ID, or None if not found
        """
        import re

        # Match new format: YYMM.NNNNN
        match = re.search(r'\d{4}\.\d{4,5}', text)
        if match:
            return match.group()

        # Match old format: arch-ive/YYMMNNN
        match = re.search(r'[a-z-]+/\d{7}', text)
        if match:
            return match.group()

        return None


class SemanticScholarClient(APIClient):
    """Semantic Scholar API client

    Used for general academic paper search and verification

    API documentation: https://api.semanticscholar.org/api-docs/
    """

    def __init__(self, rate_limit: int = 20):
        """
        Args:
            rate_limit: maximum requests per minute (Semantic Scholar limit: 100 requests/5min)
        """
        super().__init__(rate_limit)
        try:
            from semanticscholar import SemanticScholar
            self.sch = SemanticScholar()
        except ImportError:
            raise ImportError("semanticscholar library required: pip install semanticscholar")

    def search_by_title(self, title: str, max_results: int = 5) -> Optional[Dict]:
        """Search for a paper by title

        Args:
            title: paper title
            max_results: maximum number of results to return

        Returns:
            Normalized paper information dictionary (first result), or None if not found
        """
        try:
            self.rate_limiter.wait_if_needed()
            results = self.sch.search_paper(title, limit=max_results)

            if not results:
                return None

            # Return first result
            paper = results[0]
            return self._normalize_result(paper)
        except Exception as e:
            print(f"Semantic Scholar API error: {e}")
            return None

    def search_by_doi(self, doi: str) -> Optional[Dict]:
        """Search for a paper by DOI

        Args:
            doi: DOI identifier

        Returns:
            Normalized paper information dictionary, or None if not found
        """
        try:
            self.rate_limiter.wait_if_needed()
            paper = self.sch.get_paper(f"DOI:{doi}")
            if paper:
                return self._normalize_result(paper)
            return None
        except Exception as e:
            print(f"Semantic Scholar API error: {e}")
            return None

    def search(self, title: str = None, doi: str = None, **kwargs) -> Optional[Dict]:
        """Search for a paper (unified interface)"""
        if doi:
            return self.search_by_doi(doi)
        elif title:
            return self.search_by_title(title)
        return None

    def _normalize_result(self, paper) -> Dict:
        """Normalize Semantic Scholar response"""
        # Extract authors
        authors = []
        if paper.authors:
            authors = [a.name for a in paper.authors]

        # Extract external IDs
        external_ids = paper.externalIds if hasattr(paper, 'externalIds') else {}
        doi = external_ids.get('DOI') if external_ids else None
        arxiv_id = external_ids.get('ArXiv') if external_ids else None

        return {
            'title': paper.title,
            'authors': authors,
            'year': paper.year,
            'venue': paper.venue if hasattr(paper, 'venue') else '',
            'paperId': paper.paperId,
            'doi': doi,
            'arxiv_id': arxiv_id,
            'citationCount': paper.citationCount if hasattr(paper, 'citationCount') else 0,
            'abstract': paper.abstract if hasattr(paper, 'abstract') else '',
            'source': 'semantic_scholar'
        }


class CitationAPIManager:
    """Unified API manager

    Coordinates the three API clients and implements an intelligent API selection strategy
    """

    def __init__(self):
        """Initialize all API clients"""
        self.crossref = None
        self.arxiv = None
        self.semantic_scholar = None

        # Attempt to initialize each client
        try:
            self.crossref = CrossRefClient()
        except Exception as e:
            print(f"Warning: CrossRef client initialization failed: {e}")

        try:
            self.arxiv = ArXivClient()
        except Exception as e:
            print(f"Warning: arXiv client initialization failed: {e}")

        try:
            self.semantic_scholar = SemanticScholarClient()
        except Exception as e:
            print(f"Warning: Semantic Scholar client initialization failed: {e}")

    def verify_citation(self, citation_info: Dict) -> tuple[bool, Optional[str], Optional[Dict]]:
        """Verify a citation

        Implements API selection strategy:
        1. Prefer DOI -> CrossRef
        2. arXiv ID -> arXiv
        3. Title search -> Semantic Scholar

        Args:
            citation_info: citation information dictionary, may contain doi, arxiv_id, title, authors, etc.

        Returns:
            (exists, api_source, api_data)
            - exists: whether the paper exists
            - api_source: verification source ('crossref', 'arxiv', 'semantic_scholar')
            - api_data: normalized data returned by the API
        """
        # Strategy 1: prefer DOI
        if 'doi' in citation_info and self.crossref:
            data = self.crossref.search_by_doi(citation_info['doi'])
            if data:
                return True, 'crossref', data

        # Strategy 2: arXiv ID
        arxiv_id = citation_info.get('arxiv_id')
        if not arxiv_id and 'note' in citation_info:
            # Try to extract arXiv ID from note field
            arxiv_id = ArXivClient.extract_arxiv_id(citation_info['note'])

        if arxiv_id and self.arxiv:
            data = self.arxiv.search_by_id(arxiv_id)
            if data:
                return True, 'arxiv', data

        # Strategy 3: general search (Semantic Scholar)
        if 'title' in citation_info and self.semantic_scholar:
            data = self.semantic_scholar.search_by_title(citation_info['title'])
            if data:
                return True, 'semantic_scholar', data

        return False, None, None

    def get_bibtex(self, doi: str) -> Optional[str]:
        """Get BibTeX by DOI

        Args:
            doi: DOI identifier

        Returns:
            BibTeX string, or None if failed
        """
        if self.crossref:
            return self.crossref.get_bibtex(doi)
        return None


# ============================================================================
# Usage examples
# ============================================================================

if __name__ == '__main__':
    # Example 1: using CrossRef client
    print("Example 1: CrossRef client")
    print("-" * 60)
    crossref = CrossRefClient()
    result = crossref.search_by_doi("10.48550/arXiv.1706.03762")
    if result:
        print(f"Title: {result['title']}")
        print(f"Authors: {', '.join(result['authors'][:3])}")
        print(f"Year: {result['year']}")
    print()

    # Example 2: using arXiv client
    print("Example 2: arXiv client")
    print("-" * 60)
    try:
        arxiv_client = ArXivClient()
        result = arxiv_client.search_by_id("1706.03762")
        if result:
            print(f"Title: {result['title']}")
            print(f"Authors: {', '.join(result['authors'][:3])}")
            print(f"Year: {result['year']}")
    except ImportError as e:
        print(f"Skipped: {e}")
    print()

    # Example 3: using Semantic Scholar client
    print("Example 3: Semantic Scholar client")
    print("-" * 60)
    try:
        ss_client = SemanticScholarClient()
        result = ss_client.search_by_title("Attention is All You Need")
        if result:
            print(f"Title: {result['title']}")
            print(f"Authors: {', '.join(result['authors'][:3])}")
            print(f"Year: {result['year']}")
            print(f"Citations: {result['citationCount']}")
    except ImportError as e:
        print(f"Skipped: {e}")
    print()

    # Example 4: using the unified manager
    print("Example 4: Unified API manager")
    print("-" * 60)
    manager = CitationAPIManager()
    citation_info = {
        'title': 'Attention is All You Need',
        'authors': ['Vaswani', 'Shazeer'],
        'year': '2017'
    }
    exists, source, data = manager.verify_citation(citation_info)
    if exists:
        print(f"Verification succeeded!")
        print(f"Source: {source}")
        print(f"Title: {data['title']}")
        print(f"Year: {data['year']}")
