import os
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SearchResult:
    title: str
    url: str


@dataclass
class FetchedPage:
    url: str
    title: str
    text: str


def _fetch(url: str, timeout: int = 15) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "MuseumEngine/1.0 (research)"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def search_duckduckgo(query: str, max_results: int = 5) -> List[SearchResult]:
    encoded = urllib.parse.quote_plus(query)
    url = f"https://duckduckgo.com/html/?q={encoded}"
    html = _fetch(url)
    results = []
    for match in re.finditer(r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>(.*?)</a>', html):
        href = match.group(1)
        title = re.sub(r"<.*?>", "", match.group(2))
        results.append(SearchResult(title=title.strip(), url=href))
        if len(results) >= max_results:
            break
    return results


def search(query: str, max_results: int = 5) -> List[SearchResult]:
    provider = os.getenv("MUSEUM_ENGINE_SEARCH", "duckduckgo")
    if provider == "duckduckgo":
        return search_duckduckgo(query, max_results=max_results)
    raise RuntimeError(f"Unsupported search provider: {provider}")


def fetch_page(url: str) -> FetchedPage:
    html = _fetch(url)
    title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else url
    text = re.sub(r"<script.*?>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style.*?>.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return FetchedPage(url=url, title=title, text=text)


def maybe_search(query: str, max_results: int = 5, offline: bool = False) -> List[SearchResult]:
    if offline:
        return []
    return search(query, max_results=max_results)


def maybe_fetch(url: str, offline: bool = False) -> Optional[FetchedPage]:
    if offline:
        return None
    return fetch_page(url)
