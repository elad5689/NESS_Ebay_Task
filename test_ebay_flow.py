
import json
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

# Import all the page objects
from home_page import HomePage
from search_results_page import SearchResultsPage
from product_page import ProductPage
from cart_page import CartPage
from login_page import LoginPage


def load_test_data(file_path):
    """Loads test data from the specified JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def validate_test_data(data):
    """Validates the structure and values of the test data."""
    if not isinstance(data.get('search_term'), str) or not data['search_term']:
        pytest.fail("Test data error: 'search_term' must be a non-empty string.")

    try:
        max_price = float(data.get('max_price'))
        if max_price < 0:
            pytest.fail("Test data error: 'max_price' cannot be negative.")
    except (ValueError, TypeError):
        pytest.fail("Test data error: 'max_price' must be a valid number.")

    try:
        item_limit = int(data.get('item_limit'))
        if item_limit < 0:
            pytest.fail("Test data error: 'item_limit' cannot be negative.")
    except (ValueError, TypeError):
        pytest.fail("Test data error: 'item_limit' must be a valid integer.")

    if 'username' not in data or 'password' not in data:
        pytest.fail("Test data error: 'username' and 'password' are required for login.")


@allure.title("Ebay Shopping Flow Test")
@allure.description("This test simulates a full user journey: logging in, searching for an item, filtering by price, adding multiple items to the cart, and verifying the total.")
def test_ebay_shopping_journey():
    """Main function to run the automation flow."""
    driver: WebDriver = None
    try:
        # --- Load and Validate Test Data ---
        with allure.step("Load and validate test data from data.json"):
            try:
                test_data = load_test_data('data.json')
                validate_test_data(test_data)
                search_term = test_data['search_term']
                max_price = test_data['max_price']
                item_limit = test_data['item_limit'] + 2
                username = test_data['username']
                password = test_data['password']
                allure.attach(json.dumps(test_data, indent=4), name="Test Data", attachment_type=allure.attachment_type.JSON)
            except (FileNotFoundError, KeyError) as e:
                pytest.fail(f"Failed to load or parse test data: {e}")

        # --- Initialize WebDriver ---
        with allure.step("Initialize Chrome WebDriver"):
            driver = webdriver.Chrome()
            driver.maximize_window()
            driver.implicitly_wait(10)

        # --- Login Step ---
        with allure.step(f"Log in with user: {username}"):
            login_page = LoginPage(driver)
            login_page.login(username, password)
            # You might want to add an assertion here to verify login was successful

        # --- Start of the automation flow ---
        home_page = HomePage(driver)

        # --- Search for Items and Filter by Price ---
        with allure.step(f"Search for '{search_term}' with max price {max_price}"):
            search_results_page = SearchResultsPage(driver)
            item_urls = search_results_page.search_item_by_name_under_price(
                item_name=search_term,
                max_price=max_price,
                limit=item_limit
            )
            if not item_urls:
                pytest.fail("No item URLs were found after filtering.")
            allure.attach(f"Found {len(item_urls)} items to process.", name="Item URLs Count")


        # --- Add Items to Cart ---
        with allure.step(f"Visit each product page and add items to cart"):
            for index, url in enumerate(item_urls, start=1):
                with allure.step(f"Processing item {index}/{len(item_urls)}"):
                    try:
                        product_page = ProductPage(driver, url)
                        product_page.add_item_to_cart(index)
                        allure.attach(driver.get_screenshot_as_png(), name=f"item{index}.png", attachment_type=allure.attachment_type.PNG)
                    except Exception as e:
                        allure.attach(driver.get_screenshot_as_png(), name=f"item{index}_error.png", attachment_type=allure.attachment_type.PNG)
                        print(f"Error adding item {index}: {e}")
                        continue

        # --- View Cart and Assert Total ---
        with allure.step("Verify cart total does not exceed budget"):
            cart_page = CartPage(driver)
            max_budget = float(max_price) * len(item_urls)
            
            # This will take a screenshot and assert the total
            cart_page.assert_cart_total_not_exceeds(max_budget)
            
            # Attach the budget info to the report
            allure.attach(f"Cart Total: {cart_page.cart_total}\nMax Budget: {max_budget}", 
                         name="Budget Verification")


    except Exception as e:
        # Attach a screenshot on any failure in the main flow
        if driver:
            allure.attach(driver.get_screenshot_as_png(), name="test_failure_screenshot.png", attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"An unexpected error occurred during the main flow: {e}")

    finally:
        # --- Clean up ---
        if driver:
            driver.quit()
