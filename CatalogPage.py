from selenium.webdriver.common.by import By

class CatalogPage:
    def __init__(self, driver):
        self.driver = driver
    
    # Localizadores dos elementos na págin
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[text()='Add to cart']")
    REMOVE_BUTTON = (By.XPATH, "//button[text()='Remove']")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    
    # Para adicionar um produto ao carrinho
    def add_product_to_cart(self, product_index=0):
        add_buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTON)
        add_buttons[product_index].click()

    # Para remover um produto do catálogo
    def remove_product_from_catalog(self, product_index=0):
        remove_buttons = self.driver.find_elements(*self.REMOVE_BUTTON)
        remove_buttons[product_index].click()
    
    # Verificar se o ícone do carrinho está presente
    def is_cart_icon_visible(self):
        return self.driver.find_element(*self.CART_ICON).is_displayed()
    
    # Verificar se a página foi carregada corretamente
    def is_catalog_page_loaded(self):
        return "Products" in self.driver.title
