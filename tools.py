from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException
from urllib3.exceptions import ProtocolError

import time

class ScrapeTools():
    @staticmethod
    def safeClick(webElement, webDriver, timeout=10):
        now = time.time()
        while time.time() < now + timeout:
            try:
                webElement.click()
                return
            except ElementNotInteractableException:
                time.sleep(1)
            except ElementClickInterceptedException:
                webDriver.execute_script("arguments[0].scrollIntoView();", webElement)
        try:
            webElement.click()
        except Exception as clickError:
            raise Exception('Could not click element {} within {} seconds due to {}.'.format(webElement.get_attribute('outerHTML'), timeout, clickError))

    @staticmethod
    def safeFind(selector, element, timeout=30):
        now = time.time()
        while time.time() < now + timeout:
            try:
                result = selector(element)
                return result
            except NoSuchElementException:
                time.sleep(1)
            except ProtocolError:
                time.sleep(5)
        try:
            result = selector(element)
            return result
        except Exception as selectionError:
            raise Exception('Could not find element {} within {} seconds due to {}.'.format(element, timeout, selectionError))

    @staticmethod
    def goBack(webDriver):
        webDriver.execute_script("window.history.go(-1)")
