import config
from crawler.crawler import Crawler


if __name__ == '__main__':
    crawler = Crawler(
        start_urls=config.START_URLS,
        crawled_pages_count=config.CRAWLED_PAGES_COUNT,
        chunk_size=config.CHUNK_SIZE,
        fetch_workers=config.FETCH_WORKERS,
        database_workers=config.DATABASE_WORKERS
    )
    crawler.run()
