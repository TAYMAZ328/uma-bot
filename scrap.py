from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


def update_week(driver, week):
    match week:
        case 'pre':
            pre = driver.find_element(By.XPATH, "//div[@class='btn-group']/button[1]")
            pre.click()
        case 'corrent':
            cnt = driver.find_element(By.XPATH, "//div[@class='btn-group']/button[2]")
            cnt.click()
        case 'next':
            next = driver.find_element(By.XPATH, "//div[@class='btn-group']/button[3]")
            next.click()

    time.sleep(5)

    return driver


def scrap(driver):
    src = driver.page_source
    bs = BeautifulSoup(src, 'html.parser')
    raw_table = bs.find('table')

    return raw_table
