"""Initialize base methods"""
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseClass:
    """Initialize base methods"""
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *locator):
        """Find element"""
        return self.driver.find_element(*locator)

    def click(self, locator):
        """Click element"""
        self.find_element(*locator).click()

    def hover(self, locator):
        """Hover on element"""
        element = self.find_element(*locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def wait_element_visibility(self, locator):
        """Wait for element to be visible"""
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print("Element not found")
            self.driver.quit()

    def wait_element_clickable(self, locator):
        """Wait for element to be clickable"""
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            print("Element not found")
            self.driver.quit()

    def switch_to_iframe(self, iframe_locator):
        """Switch to Iframe"""
        try:
            (WebDriverWait(self.driver, 5)
             .until(EC.frame_to_be_available_and_switch_to_it(iframe_locator)))
        except TimeoutException:
            print("Iframe not found")
            self.driver.quit()

    def switch_to_default_content(self):
        """Switch to default content"""
        self.driver.switch_to.default_content()
