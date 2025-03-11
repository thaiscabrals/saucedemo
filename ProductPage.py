from selenium.webdriver.common.by import By
from BasePage import BasePage

class ProductPage(BasePage):
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[text()='ADD TO CART']")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")

    def add_product_to_cart(self):
        self.click(*self.ADD_TO_CART_BUTTON)

    def go_to_cart(self):
        self.click(*self.CART_ICON)

    def sort_products(self, sort_option):
        self.click(*self.SORT_SELECT)
        self.driver.find_element(By.XPATH, f"//option[text()='{sort_option}']").click()
