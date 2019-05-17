from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver: RemoteWebDriver):
        self.driver = driver


class MainPage(BasePage):
    """Home page action methods come here. I.e. Python.org"""

    # Declares a variable that will contain the retrieved text
    # search_text_element = SearchTextElement()

    def is_title_matches(self):
        """我的 BK 体验 - 欢迎"""
        return "BK" in self.driver.title

    """locators=(By.ID, 'submit')"""
    def click_button_jump(self, locators):

        element = self.driver.find_element(locators)
        element.click()




class SearchResultsPage(BasePage):
    """Search results page action methods come here"""

    def is_results_found(self):
        # Probably should search for this text in the specific page
        # element, but as for now it works fine
        return "No results found." not in self.driver.page_source
