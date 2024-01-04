import time
from selenium.webdriver.chrome.webdriver import WebDriver

def injectScript(driver: WebDriver):
    with open('./xhr.js', encoding='utf-8') as f:
        driver.execute_script(f.read())

class WebFetch:
    _driver: WebDriver
    _pathname: str
    _timeout: int = 60
    def __init__(self, driver, pathname, *timeout):
        self._driver = driver
        self._pathname = pathname
        if timeout:
            self._timeout = timeout

    def waitRes(self, callback):
        self._driver.execute_script(f'window.__resStore["{self._pathname}"] = null')
        # endTime = time.monotonic() + self._timeout
        while True:
            res = self.getRes()
            if res:
                callback(res)
                return
            
            # if time.monotonic() > endTime:
            #     break
            time.sleep(0.5)
        # raise Exception(f'{self._pathname} res timeout')
        
        
    def getRes(self) -> str:
        res = self._driver.execute_script(f'return window.__resStore["{self._pathname}"]')
        return res


# def saveRes():
    

# def mock(driver, url):
#     wait = WebDriverWait(driver, 10)
#     wait.until(EC.)