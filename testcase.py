import pytest
from selenium import webdriver
from LoginPage import LoginPage
from ProductPage import ProductPage
from CartPage import CartPage
from CheckoutPage import CheckoutPage
from CatalogPage import CatalogPage
from MainPage import MainPage

@pytest.fixture
def setup():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

def test_successful_login(setup):
    driver = setup
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")
    assert "Products" in driver.page_source


# Verifique se é possível fazer o login com todos os usuários
@pytest.mark.parametrize("user_key", ["standard_user", "visual_user", "error_user", "locked_out_user", "problem_user", "performance_glitch_user"])
def test_login_for_all_users(setup, user_key):
    driver = setup
    login_page = LoginPage(driver)
    
    user_data = login_page.USERS[user_key]
    username = user_data["username"]
    password = user_data["password"]
    
    login_page.login(username, password)
    
    if user_key in ["standard_user", "visual_user", "error_user", "problem_user"]:
        assert "Products" in driver.page_source
    
    elif user_key == "locked_out_user":
        error_message = login_page.get_error_message()
        assert "Epic sadface: Sorry, this user has been locked out." in error_message
    
    elif user_key == "performance_glitch_user":
        # Aguarda até que o catálogo de produtos seja exibido
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))
        assert "Products" in driver.page_source

    driver.save_screenshot("screenshotLogin.png")
    
# Verifique se é possível remover itens do carrinho
def test_remove_item_from_cart(setup):
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")

    product_page = ProductPage(driver)
    product_page.add_product_to_cart()
    product_page.go_to_cart()

    cart_page = CartPage(driver)
    cart_page.remove_item_from_cart()

    assert cart_page.get_item_count() == 0

    driver.save_screenshot("screenshotRemoveItens.png")

# Verifique se é possível remover itens diretamente do catálogo
def test_remove_product_from_catalog_error_user(driver, login_page, catalog_page):
    login_page.login("error_user", "secret_sauce")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

    catalog_page.add_product_to_cart(0)
    assert catalog_page.is_cart_icon_visible()

    catalog_page.remove_product_from_catalog(0)
    WebDriverWait(driver, 2).until(EC.staleness_of(driver.find_element(By.XPATH, "//div[@class='inventory_item'][1]")))

    assert catalog_page.is_cart_icon_visible() 
    assert "Remove" not in driver.page_source

    assert catalog_page.is_catalog_page_loaded()
    assert "error" not in driver.page_source.lower()

    driver.save_screenshot("screenshotRemoverCatalogo.png")

# Verifique se é possível finalizar uma compra
def test_checkout_process(setup):
    driver = setup
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")

    product_page = ProductPage(driver)
    product_page.add_product_to_cart()

    product_page.go_to_cart()

    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    checkout_page.fill_checkout_info("Thais", "Cabral", "12345")
    checkout_page.complete_purchase()

    confirmation_message = checkout_page.get_confirmation_message()
    assert "THANK YOU FOR YOUR ORDER" in confirmation_message

    driver.save_screenshot("screenshotFinalizarCompra.png")

#Verifique se é uma mensagem de erro é exibida ao tentar odenar o catálogo com o usuário 'error_user'
def test_sort_catalog_for_error_user(setup):
    driver = setup
    login_page = LoginPage(driver)
    catalog_page = CatalogPage(driver)

    login_page.login("error_user", "secret_sauce")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
    
    # Tenta ordenar os produtos por "Price (low to high)"
    catalog_page.sort_products("Price (low to high)")
    error_message = catalog_page.get_error_message()    
    assert "Epic sadface" in error_message

    # Tenta ordenar os produtos por "Price (high to low)"
    catalog_page.sort_products("Price (high to low)")
    error_message = catalog_page.get_error_message()
    assert "Epic sadface" in error_message

    # Tenta ordenar os produtos por "Name (A to Z)"
    catalog_page.sort_products("Name (A to Z)")
    error_message = catalog_page.get_error_message()
    assert "Epic sadface" in error_message

    # Tenta ordenar os produtos por "Name (Z to A)"
    catalog_page.sort_products("Name (Z to A)")
    error_message = catalog_page.get_error_message()
    assert "Epic sadface" in error_message

    driver.save_screenshot("screenshotErroSort.png")


#Verifique se é possível finalizar a compra com o campo last name desabilitado para o 'error_user'
def test_checkout_last_name_field_for_error_user(setup):
    driver = setup
    login_page = LoginPage(driver)
    checkout_page = CheckoutPage(driver)    

    login_page.login("error_user", "secret_sauce")

    catalog_page = CatalogPage(driver)
    catalog_page.add_product_to_cart(0)
    
    catalog_page.click_checkout_button()

    checkout_page.enter_last_name("Teste")    
    last_name_value = checkout_page.get_last_name_field_value()
    assert last_name_value == ""
    
    checkout_page.click_continue()
    assert checkout_page.get_last_name_field_value() == ""

    error_message = checkout_page.get_error_message()
    assert error_message is not None

    driver.save_screenshot("screenshotLastName.png")

# Verifique se é possível realizar o logout 
def test_logout_for_all_users(setup):
    driver = setup
    login_page = LoginPage(driver)
    inventory_page = MainPage(driver)
    
    users = [
        {"username": "standard_user", "password": "secret_sauce"},
        {"username": "locked_out_user", "password": "secret_sauce"},
        {"username": "problem_user", "password": "secret_sauce"},
        {"username": "performance_glitch_user", "password": "secret_sauce"},
        {"username": "error_user", "password": "secret_sauce"}
    ]
    
    for user in users:
        login_page.login(user["username"], user["password"])
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

        inventory_page.click_menu_button()
        inventory_page.click_logout_button()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-button")))
        login_button = driver.find_element(By.ID, "login-button")
        assert login_button.is_displayed()

        driver.save_screenshot("screenshotLogout.png")

