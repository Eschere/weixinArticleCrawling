import json
from selenium.webdriver.chrome.webdriver import WebDriver

def saveCacheCookie(cookies):
    with open('./.cache/cookie.json', mode='w', encoding='utf-8') as f:
        json.dump(cookies, f)

def getCacheCookie() -> list[dict]:
    try:
        with open('./.cache/cookie.json', mode='r', encoding='utf-8') as f:
            cookies = json.load(f)
            return cookies
    except:
        return False

def addCookies(driver: WebDriver, cookies):
    if cookies:
        try:
            for cookie in cookies:
                driver.add_cookie(cookie)
            return True
        except:
            return False
    
    return False