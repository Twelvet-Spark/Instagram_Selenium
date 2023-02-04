from pages.loginPage import LoginPage
from pages.postPage import PostPage
import undetected_chromedriver as uc

class Drivers():
    def __init__(self, headless=False):
        self.headless = headless
        self.options = uc.ChromeOptions()
        self.http = 'https://www.instagram.com/'
        self.driver = ""

    def create_driver(self):
        if self.headless == True:
            self.options.headless = True
        self.options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.driver = uc.Chrome(options=self.options)
        print(f"Created driver, mode headless = {self.options.headless}\n")

    def get_driver(self):
        return self.driver

    def start_driver(self):
        self.driver.get(self.http)
        print(f"[Driver] Successful link click {self.http}\n")

    def stop_driver(self):
        self.driver.close()
        print(f"[Driver] Closed\n")

    def login_driver(self):
        LoginPage(self.driver).login()

    def start_scraping(self):
        PostPage(self.driver).scrape_links()