import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from base_page import BasePage
from home_page import HomePage

class SearchResultsPage(BasePage):
    # Locators
    MAX_PRICE_INPUT = (By.XPATH, "//label[contains(text(), 'Max')]/following::input[1]")
    PRICE_FILTER_BUTTON = (By.CLASS_NAME, "x-textrange__button")
    ITEM_CARDS = (By.CLASS_NAME, "s-card")
    ITEM_LINK_SELECTOR = (By.CLASS_NAME, "su-link")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.home_page = HomePage(driver)

    def search_item_by_name_under_price(self, item_name: str, max_price: float, limit: int = 5) -> list:
        """
        Searches for an item by name and filters results by maximum price.
        
        Args:
            item_name: The name of the item to search for
            max_price: The maximum price to filter by
            limit: Maximum number of items to return (default: 5)
            
        Returns:
            list: URLs of the filtered items
        """
        # Perform the initial search
        self.home_page.search_for_item(item_name)
        
        # Apply price filter
        time.sleep(3)  # Wait for search results to load
        self.do_send_keys(self.MAX_PRICE_INPUT, str(max_price))
        self.do_click(self.PRICE_FILTER_BUTTON)
        time.sleep(3)  # Wait for the filter to apply
        
        # Get the filtered item URLs
        return self.get_item_urls(limit)
        
    def set_max_price(self, max_price):
        """
        Sets the maximum price filter on the search results page.
        
        Note: This method is kept for backward compatibility.
        Consider using search_item_by_name_under_price instead.
        """
        time.sleep(3)  # Allowing time for elements to be fully ready
        self.do_send_keys(self.MAX_PRICE_INPUT, str(max_price))
        self.do_click(self.PRICE_FILTER_BUTTON)
        time.sleep(3)  # Wait for the filter to apply

    def get_item_urls(self, limit):
        """
        Gets the URLs of the items on the page up to a given limit.
        Skips the first 2 results as they are often ads.
        """
        urls = []
        try:
            items = self.get_elements(self.ITEM_CARDS)
            # Process only up to the limit or the number of items found
            num_to_process = min(limit, len(items))
            
            for i in range(num_to_process):
                try:
                    card = items[i]
                    # Find the link element within each item card
                    url_element = card.find_element(self.ITEM_LINK_SELECTOR[0], self.ITEM_LINK_SELECTOR[1])
                    url = url_element.get_attribute("href")
                    urls.append(url)
                except Exception as e:
                    print(f"Could not get URL for item {i + 1}: {e}")
        except Exception as e:
            print(f"Could not find item cards: {e}")

        # Remove the first 2 URLs as they are likely ads, per original logic
        return urls[2:] if len(urls) > 2 else []
