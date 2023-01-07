from typing import List, Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup
from loguru import logger

BASE_URL = "http://www.nuforc.org/webreports/ndxevent.html"
TABLE_PAGE_BASE_URL = "http://www.nuforc.org/webreports"


def get_raw_html(url: str) -> bytes:
    """Request a GET method from the URL and return the content.

    ```python
    content = get_raw_html("http://www.nuforc.org/webreports/ndxevent.html")
    ```

    :param url: The URL of the web page to be downloaded.
    """
    logger.debug(f"Downloading {url}...")

    req = requests.get(url)

    if not req.status_code == 200:
        raise Exception(f"GET {url} returned status code {req.status_code}")
    else:
        logger.debug(f"Downloaded {url}...")
        return req.content


def extract_links(content: bytes, top: Optional[int] = None) -> List[str]:
    """Extract all the links to the monthly reports
    from the html page content.

    The links are extracted by
    1. find all the rows in the table of montly reports,
    2. filter and sort the http links in the table.

    :param content: The bytes representation of the html content
    :param top: only extract the most recent months if specified.
    """

    soup_base = BeautifulSoup(content, "html.parser")
    table_base = soup_base.find(lambda tag: tag.name == "table")
    rows_base = table_base.findAll(lambda tag: tag.name == "tr")
    cell_contents = sum([i.findAll("td") for i in rows_base], [])

    page_links = sum([j.findAll("a") for j in cell_contents], [])
    page_links = list(set([f"{TABLE_PAGE_BASE_URL}/{i['href']}" for i in page_links]))
    page_links.sort(reverse=True)

    if top is not None:
        page_links = page_links[:top]

    return page_links


def extract_table(content) -> List[pd.DataFrame]:
    """Find the tables in the page and build pandas dataframes.

    :param url: URL of the page that contains tables.
    """

    link_soup = BeautifulSoup(content, "html.parser")
    link_table = link_soup.find(lambda tag: tag.name == "table")

    dfs = pd.read_html(str(link_table))
    logger.debug(f"retrieved {len(dfs)} table(s)")

    return dfs


def unified_dataframe_from_links(url: str, top: Optional[int] = None) -> pd.DataFrame:
    """Combine all the tables from the given list of URLs

    :param table_urls: urls that contains all the tables
    """
    table_page_urls = extract_links(get_raw_html(url), top=top)

    dfs = []
    for url in table_page_urls:
        try:
            content = get_raw_html(url)
            dfs_from_link = extract_table(content)
        except Exception as e:
            logger.error(f"Could not get table from {url}")
            dfs_from_link = []
        dfs += dfs_from_link

    df_full = pd.concat(dfs)
    df_full.drop_duplicates(inplace=True)

    return df_full
