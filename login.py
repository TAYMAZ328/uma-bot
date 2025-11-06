from selenium.webdriver.common.by import By
from selenium import webdriver
import time, csv

def get_login():
    with open("files\\tokens.csv", "r") as f:
        c = csv.reader(f)
        c = list(c)[1]
        return c[0].strip(), c[1].strip()

def get_cap():
    # Open browser
    global driver
    driver = webdriver.Chrome()
    driver.get("https://taghzieh.uma.ac.ir")
    time.sleep(10)
    driver.find_element(By.ID, "captcha-image")
    path = dl_captcha()
    return path

def login(captcha):
    user, psw = get_login()

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

