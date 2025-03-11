class MainPage:
    def __init__(self, driver):
        self.driver = driver
    
    def click_menu_button(self):
        menu_button = self.driver.find_element(By.ID, "react-burger-menu-btn")
        menu_button.click()
    
    def click_logout_button(self):
        logout_button = self.driver.find_element(By.ID, "logout_sidebar_link")
        logout_button.click()
