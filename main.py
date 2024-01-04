import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from mock import WebFetch, injectScript
from handler import onArticleList
from config import accountName, startPage
from cookie import addCookies, saveCacheCookie, getCacheCookie

if not os.path.exists('./.cache'):
    os.mkdir('./.cache')

driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.get('https://mp.weixin.qq.com')

if addCookies(driver, getCacheCookie()):
    driver.refresh()

wait = WebDriverWait(driver, 30)
wait.until(EC.url_matches('/cgi-bin/home'))

print('sign in success')
signedCookies = []

for cookie in driver.get_cookies():
    if not (cookie["name"] == 'uuid'
             or cookie["name"] == 'ua_id'
             or cookie["name"] == 'b-user-id'
             or cookie["name"] == '_clck'
             ):
        signedCookies.append(cookie)

saveCacheCookie(signedCookies)

newTextEntry = driver.find_element(By.CSS_SELECTOR, '.weui-desktop-panel .new-creation__menu-item')
newTextEntry.click()

original_window = driver.current_window_handle
wait.until(EC.number_of_windows_to_be(2))
for window_handle in driver.window_handles:
    if window_handle != original_window:
        driver.switch_to.window(window_handle)
        injectScript(driver)
        break

newAnchor = driver.find_element(By.CSS_SELECTOR, '#js_plugins_list .tpl_item')
newAnchor.click()

dialog = driver.find_element(By.CSS_SELECTOR, '.weui-desktop-link-dialog .weui-desktop-dialog')

dialog.find_element(By.CSS_SELECTOR, '.inner_link_account_msg button').click()
inputWrap = dialog.find_elements(By.CSS_SELECTOR, '.weui-desktop-form__control-group')[3]
inputEl = inputWrap.find_element(By.TAG_NAME, 'input')
inputEl.send_keys(accountName)
inputEl.send_keys(Keys.ENTER)

account = dialog.find_element(By.CSS_SELECTOR, '.weui-desktop-search__panel .inner_link_account_list .inner_link_account_item')
account.click()

def waitRes():
    fetch = WebFetch(driver, '/cgi-bin/appmsgpublish')
    fetch.waitRes(onArticleList)

if startPage == 0:
    waitRes()

else:
    pageInput = dialog.find_element(By.CSS_SELECTOR, '.weui-desktop-form__controls .weui-desktop-pagination .weui-desktop-pagination__form .weui-desktop-pagination__input')
    pageInput.clear()
    pageInput.send_keys(Keys.BACKSPACE)
    pageInput.send_keys(startPage)
    pageInput.send_keys(Keys.ENTER)
    waitRes()
    
    # while True:
    #     try:
    #         code = input('>>>')
    #         print(eval(code))
    #     except Exception as e:
    #         print(e)


while True:
    time.sleep(5)

    try:
        nextBtn = dialog.find_element(By.CSS_SELECTOR, '.weui-desktop-form__controls .weui-desktop-pagination .weui-desktop-pagination__nav .weui-desktop-pagination__num__wrp+a')
        nextBtn.click()
    except:
        break
    waitRes()

   
