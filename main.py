import asyncio
import logging
import json
from crawl4ai import (
    BrowserConfig,
    CrawlerRunConfig,
    CacheMode,
    JsonCssExtractionStrategy,
    AsyncWebCrawler
)
from dotenv import load_dotenv
import os
import re
from file_utils import write_to_file, load_json, add_to_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.example.com")
START_FROM_PAGE = os.getenv("START_FROM_PAGE", "1")
END_AT_PAGE = os.getenv("END_AT_PAGE", "10")
SAVE_FILE_NAME = os.getenv("SAVE_FILE_NAME", "crawled_data")

async def crawl_content_using_schema(url: str, schema: dict) -> dict:
    browser_config = BrowserConfig()
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=JsonCssExtractionStrategy(schema, verbose=True),
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        crawled_result = await crawler.arun(url=url, config=run_config)

        if not crawled_result.success:
            logger.error(
                f"Failed to extract structured data from {url}, error: {crawled_result.error_message}"
            )
            return None
        valid_content = {}
        for item in json.loads(crawled_result.extracted_content):
            if item and any(value for value in item.values()):
                valid_content = item
                break
        return valid_content
    
def reformat_text(text: str) -> str:
    # Match ., !, or ? only when followed immediately by a non-space character
    return re.sub(r'([.!?:])(?=\S)', r'\1\n', text)

def update_content(crawled_content: dict, page: int, final_result: str) -> str:
    contents = crawled_content.get("contents", [])
    if contents:
        final_result += f"\n== Page {page} ==\n"
        for content in contents:
            content_text = content.get("content", "")
            content_text = reformat_text(content_text)
            if content_text:
                final_result += content_text + "\n"
    return final_result


def process_crawl_article():
    schema = load_json(f"schema/ts.py")
    final_result = """"""
    base_url = BASE_URL.rstrip("/")
    save_file = f"output/{SAVE_FILE_NAME}.txt"

    for page in range(int(START_FROM_PAGE), int(END_AT_PAGE) + 1):
        url = f"{base_url}/{page}"
        page_content = asyncio.run(crawl_content_using_schema(url, schema))
        # final_result = update_content(page_content, page, final_result)
        page_content = update_content(page_content, page, final_result)
        add_to_file(save_file, page_content)

    # write_to_file(save_file, final_result)
    logger.info(f"Saved crawled content to {save_file}")

    

def main():
    process_crawl_article()


if __name__ == "__main__":
    main()
