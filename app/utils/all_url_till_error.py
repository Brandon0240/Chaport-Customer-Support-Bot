import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from app.config.paths import ALL_LINKS_PATH

def get_all_links(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(10)

    try:
        driver.get(url)
    except TimeoutException:
        print(f"Timeout while loading {url}")
        driver.quit()
        return []

    driver.implicitly_wait(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    base_domain = urlparse(url).netloc
    links = set()

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(url, href)
        if urlparse(full_url).netloc == base_domain:
            links.add(full_url)

    return list(links)


def load_existing_links(filename=ALL_LINKS_PATH):

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return set(line.strip() for line in file if line.strip())
    return set()


def append_link_to_file(link, filename=ALL_LINKS_PATH):

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "a", encoding="utf-8") as file:
        file.write(link + "\n")


def crawl_website_until_error(start_url, visited_links):
    to_visit = {start_url}

    while to_visit:
        url = to_visit.pop()
        if url in visited_links:
            continue

        print(f"Crawling: {url}")
        visited_links.add(url)
        append_link_to_file(url)

        try:
            new_links = get_all_links(url)
            for link in new_links:
                if link not in visited_links:
                    to_visit.add(link)
        except Exception as e:
            print(f"Error at {url}: {e}")
            break

        time.sleep(1)



if __name__ == "__main__":
    start_url = input("Enter the website URL to start: ").strip()

    if not start_url.startswith("http://") and not start_url.startswith("https://"):
        start_url = "https://" + start_url

    visited = load_existing_links()
    crawl_website_until_error(start_url, visited)

    print(f"\nCrawling complete. Links stored in: {ALL_LINKS_PATH}")
