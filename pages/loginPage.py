from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome
import components.settings as settings

class LoginPage:
    def __init__(self, driver: Chrome):
        self.driver = driver
    
    def login(self):
        username_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
        password_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']")))

        username_input.send_keys(settings.login_data["login"])
        password_input.send_keys(settings.login_data["password"])

        login_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        login_button.click()
        
        try:
            WebDriverWait(self.driver, 10).until(EC.url_contains("https://www.instagram.com/accounts/onetap/"))
            buttons = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button")))[1].click()
            for button in buttons:
                if button.text == "Not Now":
                    button.click()
        except Exception as e:
            pass

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"a[href=\"/{settings.login_data['username']}/\"]")))
        except Exception:
            print(f"[Driver] Login failed\n")
        else:
            print(f"[Driver] Login completed successfully\n")