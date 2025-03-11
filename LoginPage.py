from selenium.webdriver.common.by import By
from BasePage import BasePage

class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    
    USERS = {
        "standard_user": {"username": "standard_user", "password": "secret_sauce"},
        "locked_out_user": {"username": "locked_out_user", "password": "secret_sauce"},
        "problem_user": {"username": "problem_user", "password": "secret_sauce"},
        "performance_glitch_user": {"username": "performance_glitch_user", "password": "secret_sauce"}
    }

    def login(self, username, password):
        self.send_keys(*self.USERNAME_FIELD, username)
        self.send_keys(*self.PASSWORD_FIELD, password)
        self.click(*self.LOGIN_BUTTON)

    def get_error_message(self):
        try:
            return self.driver.find_element(*self.ERROR_MESSAGE).text
        except:
            return None
