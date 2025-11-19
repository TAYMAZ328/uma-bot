from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time, os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("USER")
psw = os.getenv("PSW")


def get_cap():
    # Open browser
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    global driver
    driver = webdriver.Chrome(options=options)
    driver.get("https://taghzieh.uma.ac.ir")
    time.sleep(10)
    driver.find_element(By.ID, "captcha-image")
    path = dl_captcha()
    return path

def login(captcha):
    driver.find_element(By.NAME, 'username').send_keys(user)
    driver.find_element(By.NAME, 'password').send_keys(psw)
    driver.find_element(By.NAME, 'Captcha').send_keys(captcha)
    # driver.find_element(By.NAME, 'Captcha').send_keys(input("Enter: "))
    

    time.sleep(2)
    submit = driver.find_element(By.CLASS_NAME, 'btn-primary')
    submit.click()

    # wait for the command
    time.sleep(90)
    driver.get("https://taghzieh.uma.ac.ir/#!/Reservation")
    time.sleep(10)

    return driver


def dl_captcha():
    img_element = driver.find_element(By.ID, "captcha-image")
    img_url = img_element.get_attribute("src")
    print(f"Image URL: {img_url}")

    path = "captcha.png"
    img_element.screenshot(path)


    print(f"Captcha downloaded as {path}")
    return path

