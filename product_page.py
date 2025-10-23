
import time
import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from base_page import BasePage

class ProductPage(BasePage):
    # Locators
    DROPDOWN_BUTTONS = (By.CSS_SELECTOR, "div.x-msku-evo button.listbox-button__control")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "a[href*='https://cart.payments.ebay.com/sc/add']")

    def __init__(self, driver, url):
        super().__init__(driver)
        self.driver.get(url)
        print(f"\n--- Navigated to Product Page ---")
        print(f"URL: {url}")

    def _select_variants(self):
        """
        Private method to find and select options from all variant dropdowns.
        """
        try:
            dropdown_buttons = self.get_elements(self.DROPDOWN_BUTTONS)
            if not dropdown_buttons:
                print("No variant dropdowns found.")
                return

            print(f"Found {len(dropdown_buttons)} variant dropdowns.")

            for i in range(len(dropdown_buttons)):
                all_buttons = self.get_elements(self.DROPDOWN_BUTTONS)
                button_to_click = all_buttons[i]
                
                options_container_id = button_to_click.get_attribute("aria-controls")
                self.execute_script("arguments[0].click();", button_to_click)
                
                options_container_locator = (By.ID, options_container_id)
                options_container = self.get_element(options_container_locator)
                options_selector = (By.CSS_SELECTOR, "div.listbox__option:not([aria-disabled='true'])")
                options = options_container.find_elements(options_selector[0], options_selector[1])

                if len(options) > 1:
                    second_option = options[1]
                    print(f"Selecting option: '{second_option.text.strip()}'")
                    self.execute_script("arguments[0].click();", second_option)
                else:
                    print("No selectable options were found in this dropdown.")
                
                time.sleep(2)

        except TimeoutException:
            print("Timeout while looking for variant dropdowns. Assuming no variants.")

    def _click_add_to_cart_button(self):
        """
        Private method to click the 'Add to Cart' button.
        """
        print("Attempting to add item to cart...")
        self.do_click(self.ADD_TO_CART_BUTTON)
        time.sleep(2)

    def add_item_to_cart(self, index_for_pic):
        """
        Public method to select product variants (if any) and add the item to the cart.
        """
        try:
            self._select_variants()
            self._click_add_to_cart_button()
            time.sleep(2)
            print("Successfully processed 'add to cart'.")
        except Exception as e:
            print(f"An error occurred while trying to add item to cart: {e}")
            # Re-raise the exception to be handled by the test, which will take a failure screenshot
            raise
