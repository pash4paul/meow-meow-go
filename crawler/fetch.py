import re
from typing import List, Set
import urllib.parse

from bs4 import BeautifulSoup
import requests

from logger import get_logger

RE_CLEAN = re.compile(r'[^\w]+')
RE_CLEAN_SPACES = re.compile(r'\s+')
LOGGER = get_logger(__name__)


def parse_links(soup: BeautifulSoup) -> Set:
    links = set()
    for link in soup.find_all('a'):
        href = link.get('href')
        if not href or href.startswith('mailto:'):
            continue
        links.add(href)
    return links


def clean_html(html: str) -> str:
    clean_text = re.sub(RE_CLEAN, ' ', html)
    clean_text = re.sub(RE_CLEAN_SPACES, ' ', html)
    return clean_text.strip()


def fetch(url: str) -> (int, str, str, List[str]):
    try:
        html = requests.get(url).text
    except Exception as e:
        LOGGER.error('{} {}'.format(url, str(e)))
        return -1, '', '', []
    soup = BeautifulSoup(html, 'html.parser')
    links = parse_links(soup)
    urls = [urllib.parse.urljoin(url, l) for l in links]
    clean_text = clean_html(soup.get_text())
    LOGGER.info(url)
    return 0, url, clean_text, urls


__all__ = [fetch]
