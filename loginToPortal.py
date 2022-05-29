# setup selenium with firefox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
import time
import os
from datetime import datetime, timedelta


# clear console
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# load file if exists else create
def loadFile(fileName):
    if os.path.isfile(fileName):
        with open(fileName, 'r') as f:
            return f.read().split("\n")
    else:
        clear()
        email = input("Enter the email used on the LUMS Portal? \n>")
        clear()
        password = input("Enter the password used on the LUMS Portal? \n>")
        clear()
        print("Thanks. Your credentials have been saved for future logins.")

        with open(fileName, 'w') as f:
            f.write(f"{email}\n{password}")
            return f"{email}\n{password}".split("\n")


def elementFinder(value, by=By.CSS_SELECTOR, event="text", messages=["", ""], one=True):
    clear()
    print(messages[0])

    while True:
        try:
            # if multiple elements need to be returned
            if not one:
                ele = driver.find_elements(by=by, value=value)
                print(messages[1])
                return ele

            # if text of one element needs to be returned
            elif event == "text":
                text = driver.find_element(by=by, value=value).text
                print(messages[1])
                return text

            # if one element needs to be clicked
            elif event == "click":
                driver.find_element(by=by, value=value).click()
                print(messages[1])
                return True

        except ElementClickInterceptedException:
            continue
        except NoSuchElementException:
            continue


# get email and password from stored file if exists else get info from user
email = loadFile('unpw.txt')[0]
password = loadFile('unpw.txt')[1]
# show browser when checking portal
SHOW_BROWSER = True
# how often to refresh in minutes
REFRESH_RATE = 5

options = Options()
options.headless = not SHOW_BROWSER
driver = webdriver.Firefox(
    options=options, service=Service("./geckodriver.exe"))

driver.set_page_load_timeout(120)
driver.implicitly_wait(120)

# webdriver setup
driver.get("https://admissions.lums.edu.pk/application/")

# email field
xpath = "//input[@type='email']"
emailField = elementFinder(xpath, by=By.XPATH, one=False, messages=[
    "Searching for email input", "Entered email"])[0]
emailField.send_keys(email)

# password field
xpath = "//input[@type='password']"
pwField = elementFinder(xpath, by=By.XPATH, one=False, messages=[
                        "Searching for password input", "Entered Password"])[0]
pwField.send_keys(password)
pwField.send_keys(Keys.ENTER)

# find and go to application form link
# span tag which has text "Application Form"
cls = "span.label-pill.label-inline"
linkTag = elementFinder(
    cls, messages=["Waiting to get logged in", "Successful login"], one=False)[2]

# get href from the parent a tag of the span tag
link = linkTag.find_element(By.XPATH, "..").get_attribute("href")
# go to that main portal link
driver.get(link)
