from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Browser:
    def __init__(self):
        self.__webdriver = webdriver.Chrome(
            service = Service(ChromeDriverManager().install()),
            options = self.__webdriver_options()
        )
        self.__webdriver.implicitly_wait(30)

    def go_to_page(self, url: str):
        self.__webdriver.get(url)

    def find_elements_by_tag(self, tag: str):
        WebDriverWait(self.__webdriver, 30).until(EC.presence_of_all_elements_located((By.TAG_NAME, tag)))
        return self.__webdriver.find_elements(By.TAG_NAME, tag)
    
    def find_element_by_id(self, id: str):
        WebDriverWait(self.__webdriver, 30).until(EC.presence_of_all_elements_located((By.ID, id)))
        return self.__webdriver.find_element(By.ID, id)

    def scroll_to_bottom(self):
        self.__webdriver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def move_to(self, element):
        self.__webdriver.execute_script("arguments[0].scrollIntoView();", element)

    def move_to_element_and_click(self, element):
        self.move_to(element)
        element.click()

    def wait_for_element_to_be_clickable(self, element: str):
        WebDriverWait(self.__webdriver, 30).until(EC.element_to_be_clickable(element))

    def quit(self):
        self.__webdriver.quit()

    def __webdriver_options(self):
        options = Options()
        #options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('window-size=1920,1080')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        prefs = {
            'profile.managed_default_content_settings.images': 2,
            'profile.managed_default_content_settings.stylesheets': 2,
            'profile.managed_default_content_settings.fonts': 2,
        }
        options.add_experimental_option('prefs', prefs)
        return options