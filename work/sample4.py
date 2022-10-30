
import sys
import asyncio
import concurrent.futures
import time
from math import floor
from multiprocessing import cpu_count
import io
import aiofiles
import aiohttp
from bs4 import BeautifulSoup
from logging import getLogger, basicConfig, INFO, DEBUG
import numpy as np

"""
非同期IOとマルチプロセス
https://testdriven.io/blog/concurrency-parallelism-asyncio/#combining-asyncio-with-multiprocessing
"""
logger = getLogger(__name__)

formatter = '%(asctime)s %(levelname)s  %(processName)-20s: %(threadName)-20s: %(message)s'
basicConfig(level=DEBUG, format=formatter)

class Sample4():
    async def get_and_scrape_pages(self, num_pages, output_file):
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

            for _ in num_pages:
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


    def start_scraping(self, num_pages, output_file, i):
        logger.debug('start_scraping num_pages:{}, i:{}'.format(num_pages, i))
        # On Windows, this finishes successfully, but throws 'RuntimeError: Event loop is closed'
        # The following lines fix this
        # Source: https://github.com/encode/httpx/issues/914#issuecomment-622586610
        if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        """ Starts an async process for requesting and scraping Wikipedia pages """
        print(f"Process {i} starting...")
        asyncio.run(self.get_and_scrape_pages(num_pages, output_file))
        print(f"Process {i} finished.")


    def main(self):
        logger.debug('main')
        NUM_PAGES = [i for i in range(50)]
        NUM_CORES = 4 #cpu_count() # Our number of CPU cores (including logical cores)
        data = list(np.array_split(NUM_PAGES, NUM_CORES))

        OUTPUT_FILE = "./wiki_titles.tsv" # File to append our scraped titles to

        futures = []

        with concurrent.futures.ProcessPoolExecutor(NUM_CORES) as executor:
            for i in range(NUM_CORES):
                logger.debug('main for i:{}'.format(i))
                new_future = executor.submit(
                    self.start_scraping, 
                    data[i],
                    OUTPUT_FILE,
                    i
                )
                futures.append(new_future)

        concurrent.futures.wait(futures)


if __name__ == "__main__":
    print("Starting: Please wait (This may take a while)....")
    start = time.time()
    sample = Sample4()
    sample.main()
    print(f"Time to complete: {round(time.time() - start, 2)} seconds.")
