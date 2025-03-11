from selenium.webdriver.common.by import By
from BasePage import BasePage

class CheckoutPage(BasePage):
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    CONFIRMATION_MESSAGE = (By.XPATH, "//h2[contains(text(),'THANK YOU')]")

    def fill_checkout_info(self, first_name, last_name, postal_code):
        self.send_keys(*self.FIRST_NAME_FIELD, first_name)
        self.send_keys(*self.LAST_NAME_FIELD, last_name)
        self.send_keys(*self.POSTAL_CODE_FIELD, postal_code)
        self.click(*self.CONTINUE_BUTTON)

    def complete_purchase(self):
        self.click(*self.FINISH_BUTTON)

    def get_confirmation_message(self):
        return self.driver.find_element(*self.CONFIRMATION_MESSAGE).text
