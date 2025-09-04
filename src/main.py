from browser import Browser
from scrapers.lupa_scraper import LupaScraper


def main():
    browser = Browser()
    lupa_scraper = LupaScraper(browser)
    lupa_scraper.scrape()
    browser.quit()


if __name__ == "__main__":
    main()