from selenium.webdriver.common.by import By
from base_page import BasePage
import time

class LoginPage(BasePage):
    # Locators
    SIGN_IN_LINK = (By.LINK_TEXT, "Sign in")
    USERNAME_FIELD = (By.ID, "userid")
    CONTINUE_BUTTON = (By.ID, "signin-continue-btn")
    PASSWORD_FIELD = (By.ID, "pass")
    SIGN_IN_BUTTON = (By.ID, "sgnBt")
    USER_MENU = (By.ID, "gh-ug")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://www.ebay.com/")
        
    def login(self, username, password):
        """
        Attempt to log in with the provided credentials.
        Returns True if login was successful, False otherwise.
        """
        try:
            # Click sign in link
            self.do_click(self.SIGN_IN_LINK)
            
            # Enter username and continue
            self.do_send_keys(self.USERNAME_FIELD, username)
            self.do_click(self.CONTINUE_BUTTON)
            
            # Wait for password field and enter password
            time.sleep(2)  # Wait for page transition
            self.do_send_keys(self.PASSWORD_FIELD, password)
            self.do_click(self.SIGN_IN_BUTTON)
            
            # Verify login was successful
            time.sleep(2)  # Wait for page to load
            return self.is_logged_in()
            
        except Exception as e:
            print(f"Login error: {str(e)}")
            self.driver.get("https://www.ebay.com/")
            return False
            
    def is_logged_in(self):
        """Check if user is logged in by looking for user menu."""
        try:
            return self.get_element(self.USER_MENU).is_displayed()
        except:
            return False
