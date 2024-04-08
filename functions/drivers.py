"""Initialize drivers"""
from selenium import webdriver
from utils.document_and_names import DocumentsAndPaths


class Drivers:
    """Initialize drivers"""
    def __init__(self, browser, logger):
        self.browser = browser
        self.driver = None
        self.logger = logger

    def start_browser(self):
        """Set browser"""
        if self.browser == "chrome":
            self.driver = webdriver.Chrome()
        elif self.browser == "firefox":
            self.driver = webdriver.Firefox()
        elif self.browser == "edge":
            self.driver = webdriver.Edge()

        self.logger.info(f"Started script on {self.browser} browser")
        self.driver.maximize_window()
        self.driver.get(DocumentsAndPaths.url)
        self.logger.info(f"Page opened {DocumentsAndPaths.url}")

    def close_browser(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed TEST PASSED")
        else:
            self.logger.warning("The browser was not closed.")
