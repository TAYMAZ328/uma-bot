from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


def update_week(driver, week):
    if week == "pre":
        pre = driver.find_element(By.XPATH, "//div[@class='btn-group']/button[1]")
        pre.click()
    elif week == "current":
        cnt = driver.find_element(By.XPATH, "//div[@class='btn-group']/button[2]")
        cnt.click()
    elif week == "next":
        nxt = driver.find_element(By.XPATH, "//div[@class='btn-group']/button[3]")
        nxt.click()
    time.sleep(5)

    return driver


def scrap(driver):
    src = driver.page_source
    bs = BeautifulSoup(src, "html.parser")
    raw_table = bs.find("table")
    return raw_table
