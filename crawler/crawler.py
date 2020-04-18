from concurrent.futures import ThreadPoolExecutor
from typing import List, Generator

from bloom_filter import BloomFilter

from crawler.fetch import fetch
from crawler.utils import chunks_by_count, chunks_by_size
from db import bulk_insert
from logger import get_logger


class Crawler:
    def __init__(self, start_urls: List[str],
                 crawled_pages_count: int,
                 chunk_size: int,
                 fetch_workers: int,
                 database_workers: int):
        # При использоание set на больших объемах достигнем лимита
        # памяти.Поэтому используем фильтр блума, при этом проигрываем
        # по скорости.
        self._visited = BloomFilter(max_elements=crawled_pages_count)
        self._logger = get_logger(__name__)
        self._stop_crawling = False
        self._urls = start_urls
        self._data = []
        self._buffer = []
        self._total_crawled_pages = 0
        self._stop_crawling = False
        self._fetch_error_rate = 0.9
        self._crawled_pages_count = crawled_pages_count
        self._chunk_size = chunk_size
        self._fetch_workers = fetch_workers
        self._database_workers = database_workers
        self._max_buffer_len = self._chunk_size * self._fetch_error_rate

    def _get_urls(self) -> Generator:
        urls = self._urls
        self._urls = []
        for chunk in chunks_by_size(urls, self._chunk_size):
            yield chunk

    def _get_data(self, urls: List[str]):
        with ThreadPoolExecutor(self._fetch_workers) as executor:
            self._data = executor.map(fetch, urls)

    def _process_data(self):
        for status, url, clean_text, parsed_urls in self._data:
            if status != 0:
                continue
            self._visited.add(url)
            self._urls.extend(
                [u for u in parsed_urls if u not in self._visited])
            self._buffer.append((url, clean_text))

    def _save_data(self):
        self._total_crawled_pages += len(self._buffer)
        with ThreadPoolExecutor(self._database_workers) as executor:
            executor.map(
                bulk_insert,
                chunks_by_count(self._buffer, self._database_workers))
        self._buffer = []

    def run(self):
        while True:
            if not self._urls or self._stop_crawling:
                self._logger.info(
                    'Total pages parsed: ' + str(self._total_crawled_pages))
                break

            for urls in self._get_urls():
                self._get_data(urls)
                self._process_data()
                if len(self._buffer) >= self._max_buffer_len:
                    self._save_data()

                if self._total_crawled_pages >= self._crawled_pages_count:
                    self._stop_crawling = True
                    break


__all__ = [Crawler]
