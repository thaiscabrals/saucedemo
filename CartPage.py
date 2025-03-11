from selenium.webdriver.common.by import By
from BasePage import BasePage

class CartPage(BasePage):
    REMOVE_BUTTON = (By.XPATH, "//button[@class='cart_button']")
    ITEM_COUNT = (By.CLASS_NAME, "cart_quantity")

    def remove_item_from_cart(self):
        self.click(*self.REMOVE_BUTTON)

    def get_item_count(self):
        return len(self.driver.find_elements(*self.ITEM_COUNT))
