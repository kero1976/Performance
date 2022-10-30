
import sys
import asyncio
import concurrent.futures
import time
from math import floor
from multiprocessing import cpu_count

import aiofiles
import aiohttp
from bs4 import BeautifulSoup
from logging import getLogger, basicConfig, INFO, DEBUG

"""
非同期IOとマルチプロセス
https://testdriven.io/blog/concurrency-parallelism-asyncio/#combining-asyncio-with-multiprocessing
"""
logger = getLogger(__name__)

formatter = '%(asctime)s %(levelname)s  %(processName)-20s: %(threadName)-20s: %(message)s'
basicConfig(level=DEBUG, format=formatter)

async def get_and_scrape_pages(num_pages: int, output_file: str):
    """
    Randamなページを取得
    Makes {{ num_pages }} requests to Wikipedia to receive {{ num_pages }} random
    articles, then scrapes each page for its title and appends it to {{ output_file }},
    separating each title with a tab: "\\t"
    #### Arguments
    ---
    num_pages: int -
        Number of random Wikipedia pages to request and scrape
    output_file: str -
        File to append titles to
    """
    logger.debug('get_and_scrape_pages num_pages:{}'.format(num_pages))
    async with \
    aiohttp.ClientSession() as client, \
    aiofiles.open(output_file, "a+", encoding="utf-8") as f:

        for _ in range(num_pages):
            logger.debug('for処理')
            async with client.get("https://en.wikipedia.org/wiki/Special:Random") as response:
                if response.status > 399:
                    # I was getting a 429 Too Many Requests at a higher volume of requests
                    response.raise_for_status()

                page = await response.text()
                soup = BeautifulSoup(page, features="html.parser")
                title = soup.find("h1").text
                # logger.debug(title)
                await f.write(title + "\n")

        await f.write("\n")


def start_scraping(num_pages: int, output_file: str, i: int):
    logger.debug('start_scraping num_pages:{}, i:{}'.format(num_pages, i))
    # On Windows, this finishes successfully, but throws 'RuntimeError: Event loop is closed'
    # The following lines fix this
    # Source: https://github.com/encode/httpx/issues/914#issuecomment-622586610
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    """ Starts an async process for requesting and scraping Wikipedia pages """
    print(f"Process {i} starting...")
    asyncio.run(get_and_scrape_pages(num_pages, output_file))
    print(f"Process {i} finished.")


def main():
    logger.debug('main')
    NUM_PAGES = 50 # Number of pages to scrape altogether
    NUM_CORES = 4 #cpu_count() # Our number of CPU cores (including logical cores)
    OUTPUT_FILE = "./wiki_titles.tsv" # File to append our scraped titles to

    PAGES_PER_CORE = floor(NUM_PAGES / NUM_CORES)
    PAGES_FOR_FINAL_CORE = PAGES_PER_CORE + NUM_PAGES % PAGES_PER_CORE # For our final core

    futures = []
    logger.info('PAGES_PER_CORE:{}'.format(PAGES_PER_CORE))
    logger.info('PAGES_FOR_FINAL_CORE:{}'.format(PAGES_FOR_FINAL_CORE))
    with concurrent.futures.ProcessPoolExecutor(NUM_CORES) as executor:
        for i in range(NUM_CORES - 1):
            logger.debug('main for i:{}'.format(i))
            new_future = executor.submit(
                start_scraping, # Function to perform
                # v Arguments v
                num_pages=PAGES_PER_CORE,
                output_file=OUTPUT_FILE,
                i=i
            )
            futures.append(new_future)

        futures.append(
            executor.submit(
                start_scraping,
                PAGES_FOR_FINAL_CORE, OUTPUT_FILE, NUM_CORES-1
            )
        )

    concurrent.futures.wait(futures)


if __name__ == "__main__":
    print("Starting: Please wait (This may take a while)....")
    start = time.time()
    main()
    print(f"Time to complete: {round(time.time() - start, 2)} seconds.")
