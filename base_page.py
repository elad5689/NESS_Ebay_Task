
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """
    Base class for all page objects.
    """
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def do_click(self, by_locator):
        """
        Performs a click on a web element.
        """
        self.wait.until(EC.element_to_be_clickable(by_locator)).click()

    def do_send_keys(self, by_locator, text):
        """
        Sends keys to a web element.
        """
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        element.clear()
        element.send_keys(text)

    def get_element(self, by_locator):
        """
        Finds and returns a web element.
        """
        return self.wait.until(EC.visibility_of_element_located(by_locator))

    def get_elements(self, by_locator):
        """
        Finds and returns a list of web elements.
        """
        return self.wait.until(EC.presence_of_all_elements_located(by_locator))

    def get_attribute(self, by_locator, attribute_name):
        """
        Gets an attribute of a web element.
        """
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        return element.get_attribute(attribute_name)

    def execute_script(self, script, element):
        """
        Executes JavaScript on an element.
        """
        self.driver.execute_script(script, element)
