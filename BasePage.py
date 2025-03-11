from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, by, value, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def click(self, by, value):
        self.wait_for_element(by, value)
        self.driver.find_element(by, value).click()

    def send_keys(self, by, value, text):
        self.wait_for_element(by, value)
        self.driver.find_element(by, value).send_keys(text)
