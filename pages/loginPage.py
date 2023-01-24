from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import components.settings as settings
from time import sleep

class LoginPage:
    def __init__(self, driver, id):
        self.driver = driver
        self.id = id
    
    def login(self):
        username_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
        password_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']")))

        username_input.send_keys(settings.login_data[self.id]["login"])
        password_input.send_keys(settings.login_data[self.id]["password"])

        login_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
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
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"a[href=\"/{settings.login_data[self.id]['username']}/\"]")))
        except Exception:
            print(f"[Драйвер - {self.id}] Вход НЕ выполнен\n")
        else:
            print(f"[Драйвер - {self.id}] Вход успешно выполнен\n")