import json
import datetime
from selenium import webdriver
from selenium.common import TimeoutException
from inspect import signature
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from Logger import set_up_logger

logger = set_up_logger('test-suite')


class BasicSeleniumDriver(webdriver.Chrome):
    wait: WebDriverWait

    def __init__(self, data_dir=False, incognito=False, headless=False, proxy=False, **kwargs):
        options = Options()
        if data_dir is not False:
            options.add_argument(data_dir)
        if incognito:
            options.add_argument("--incognito")
        options.add_argument("--start-maximized")
        if headless is True:
            options.add_argument('--headless')
        if proxy is not False:
            options.add_argument('--proxy-server=%s' % proxy)
        super().__init__(options=options, **kwargs)
        self.wait = WebDriverWait(self, 10)

    def get_element(self, xpath, wait=True):
        logger.debug(f"Searching for element '{xpath}'")
        if wait:
            return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return super().find_element(By.XPATH, xpath)

    def get_elements(self, xpath, wait=True):
        logger.debug(f"Searching for elements '{xpath}'")
        if wait:
            _ = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return super().find_elements(By.XPATH, xpath)

    @staticmethod
    def click_enter(element):
        element.send_keys(Keys.ENTER)

    @staticmethod
    def click_arrow_down(element):
        element.send_keys(Keys.ARROW_DOWN)

    def save_cookies(self, cookie_path):
        cookie_json = [{cookie['name']: cookie['value']} for cookie in self.get_cookies()]
        with open(cookie_path, 'w') as f:
            json.dump(cookie_json, f, indent=4, sort_keys=True)


def selenium_test(func):
    def _call_with_driver(headless=False, capture_screenshot=False):
        params = signature(func).parameters
        if params.get('headless'):
            headless = params.get('headless').default
        if params.get('capture_screenshot'):
            capture_screenshot = params.get('capture_screenshot').default
        driver = BasicSeleniumDriver(headless=headless)
        try:
            passed = func(driver)
        except Exception as e:
             passed = False
        if capture_screenshot:
            driver.save_screenshot(func.__name__ + f"{datetime.datetime.now()}.png")
        driver.quit()
        if passed:
            logger.info(f'{func.__name__} [PASSED]')
        else:
            logger.error(f'{func.__name__} [FAILED]')
        assert passed
    return _call_with_driver
