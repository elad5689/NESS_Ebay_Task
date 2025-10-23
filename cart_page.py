import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_page import BasePage
import re
from typing import Optional
import allure


class CartPage(BasePage):
    # Locators
    # Using a robust CSS selector for the cart icon link
    CART_ICON = (By.CSS_SELECTOR, "a.gh-flyout__target[href='https://cart.ebay.com']")
    # Using the stable ID for the internal content body of the mini-cart flyout.
    MINI_CART = (By.ID, "gh-minicart-hover-body")
    # Fallback locator for the cart total
    CART_TOTAL = (By.CSS_SELECTOR, "span.total-val")

    def __init__(self, driver):
        super().__init__(driver)
        # Navigate to the eBay homepage upon initialization
        self.driver.get("https://www.ebay.com/")
        self.cart_total = None

    def get_cart_total(self, take_screenshot: bool = False) -> Optional[float]:
        """
        Hovers over the cart icon to view the mini-cart and retrieves the cart total.

        Args:
            take_screenshot: If True, takes a screenshot after hovering

        Returns:
            float: The cart total as a float, or None if an error occurs
        """
        try:
            print("Attempting to get cart total...")
            wait = WebDriverWait(self.driver, 10)

            # 1. Wait for the cart icon to be present and hover over it
            print("Waiting for cart icon...")
            cart_icon = wait.until(
                EC.presence_of_element_located(self.CART_ICON),
                message="Cart icon not found"
            )
            print("Cart icon found. Performing hover...")
            ActionChains(self.driver).move_to_element(cart_icon).perform()
            
            # Brief pause for animation
            time.sleep(0.5)

            # 2. Wait for the mini-cart to become visible
            print("Waiting for mini-cart to be visible...")
            wait.until(
                EC.visibility_of_element_located(self.MINI_CART),
                message="Mini-cart did not become visible after hover"
            )
            print("Mini-cart is visible")

            # Take screenshot if requested
            if take_screenshot:
                print("Taking screenshot of mini-cart...")
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="mini_cart_hover.png",
                    attachment_type=allure.attachment_type.PNG
                )

            # 3. Find the price element using multiple selectors for robustness
            print("Searching for price element...")
            selectors_to_try = [
                (By.CSS_SELECTOR, "div.gh-subtotal"),
                self.CART_TOTAL, # Using the class property
                (By.CSS_SELECTOR, "span[class*='total']"),
                (By.CSS_SELECTOR, "span[data-test-id='cart-total']"),
                (By.CSS_SELECTOR, "span.gh-ebayui-cart-total")
            ]
            
            price_element = None
            for selector in selectors_to_try:
                try:
                    # Use a shorter wait here as the element should already be visible
                    price_element = WebDriverWait(self.driver, 2).until(
                        EC.visibility_of_element_located(selector)
                    )
                    print(f"Found price element with selector: {selector}")
                    break
                except:
                    continue
            
            if not price_element:
                raise Exception("Could not find price element with any selector")

            price_text = price_element.text.strip()
            print(f"Raw price text: '{price_text}'")

            # 4. Clean up the price text and convert to float
            numeric_value = float(re.sub(r"[^\d.]", "", price_text))
            self.cart_total = numeric_value
            print(f"Parsed cart total: {self.cart_total}")
            return self.cart_total

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            # Take a screenshot on failure for debugging
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="cart_total_error.png",
                attachment_type=allure.attachment_type.PNG
            )
            # Re-raise the exception to ensure the test fails
            raise Exception(f"Failed to get cart total. URL: {self.driver.current_url}, Error: {str(e)}")
            
    def assert_cart_total_not_exceeds(self, max_budget: float) -> None:
        """
        Asserts that the cart total does not exceed the specified maximum budget.
        
        Args:
            max_budget: The maximum allowed cart total
            
        Raises:
            AssertionError: If the cart total exceeds the max budget
        """
        # Get cart total with screenshot
        cart_total = self.get_cart_total(take_screenshot=True)
        
        # Additional info for the report
        print(f"Cart Total: ${cart_total:.2f}")
        print(f"Max Budget: ${max_budget:.2f}")
        
        # Assertions
        assert cart_total is not None, "Cart total could not be determined."
        assert cart_total <= max_budget, f"Cart total {cart_total} exceeds max allowed budget {max_budget}"