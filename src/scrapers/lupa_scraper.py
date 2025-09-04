import logging

from browser import Browser


class LupaScraper:
    def __init__(self, browser: Browser) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__browser = browser
        self.__base_url = 'https://lupa.uol.com.br'
        self.__search_url = f'{self.__base_url}/busca'
        self.__news_url = f'{self.__base_url}/jornalismo'
        self.__all_fact_checks_url = f'{self.__news_url}/categoria/verificação'

    def scrape(self):
        self.__browser.go_to_page(self.__all_fact_checks_url)
        div_init = self.__browser.find_element_by_id('init')
        buttons = [
            button for button in self.__browser.find_elements_by_tag('button') 
                if button.text == 'Carregar mais'
        ]
        self.__browser.move_to_element_and_click(buttons[0])
        content = [
            line.strip() for line in div_init.text.split('\n')
            if line != ''
        ]
        urls = [
            a.get_property('href') for a in self.__browser.find_elements_by_tag('a')
                if a.get_property('href').startswith(self.__news_url)
        ]
        urls = urls[1:]
        total = int(content[0].split()[3])
        extracted_fact = []
        while len(extracted_fact) < total:
            start_position = len(extracted_fact) * 4
            fact = {
                'url': urls[len(extracted_fact)],
                'datetime': content[start_position + 1],
                'title': content[start_position + 2],
                'description': content[start_position + 3],
                'author': content[start_position + 4]
            }
            extracted_fact.append(fact)
            print(len(extracted_fact))
            if len(extracted_fact) % 30 == 0:
                self.__browser.scroll_to_bottom()
                div_init = self.__browser.find_element_by_id('init')
                content = [
                    line.strip() for line in div_init.text.split('\n')
                    if line != ''
                ]
                urls = [
                    a.get_property('href') for a in self.__browser.find_elements_by_tag('a')
                    if a.get_property('href').startswith(self.__news_url)
                ]
                urls = urls[1:]

    def scrape_by_search(self, query: str) -> None:
        urls = self.extract_urls(query)
        for url in urls:
            content = self.extract_content(url)
            if content:
                print(content)

    def extract_urls(self, query: str) -> list[str]:
        search_url = f'{self.__search_url}/{query}'
        self.__browser.go_to_page(search_url)
        urls = [
            tag_a.get_property("href") for tag_a in self.__browser.find_elements_by_tag('a')
                if tag_a.get_property('href').startswith(f'{self.__base_url}{self.__news_url}')
        ]
        return urls

    def extract_content(self, url: str):
        content = None
        try:
            self.__browser.go_to_page(url)
            spans = [span.text.strip() for span in self.__browser.find_elements_by_tag('span')]
            content = {
                'url': url,
                'category': spans[3],
                'title': spans[4],
                'date': spans[5],
            }
        except Exception:
            self.__logger.error(f"Failed to extract content from {url}")
        finally:
            return content


