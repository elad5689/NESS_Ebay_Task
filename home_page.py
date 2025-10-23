from selenium.webdriver.common.by import By
from base_page import BasePage

class HomePage(BasePage):
    # Locators
    SEARCH_BOX = (By.ID, "gh-ac")
    SEARCH_BUTTON = (By.ID, "gh-search-btn")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://www.ebay.com/")

    def search_for_item(self, item_name):
        """
        Searches for an item on the home page and proceeds to the search results page.
        """
        self.do_send_keys(self.SEARCH_BOX, item_name)
        self.do_click(self.SEARCH_BUTTON)
        # This action navigates to the search results page, so we can return an instance of it.
        # We will import SearchResultsPage in the main script to avoid circular dependencies here.