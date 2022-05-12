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
SHOW_BROWSER = False
# how often to refresh in minutes
REFRESH_RATE = 5


while True:
    t1 = time.perf_counter()

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

    # getting application status
    status = elementFinder("div span.label", messages=[
                           "Searching for status", "Found status"], event="text")

    # getting other user-specific information
    cls = "span.text-dark-50.text-hover-primary.font-weight-bold.mr-lg-8.mr-5.mb-lg-0.mb-2"
    info = elementFinder(
        cls, messages=["Searching for user information", "Found information"], one=False)

    # parsing user information
    userInfo = ""
    for inf in info:
        text = inf.text
        userInfo += (f"{text}\n")

    # close browser in background
    driver.close()

    # write log to file to keep track of status
    with open("log.txt", "a") as f:
        f.write(f"{datetime.now()}: {status}\n")

    # calculate time taken
    timeTaken = time.perf_counter() - t1
    # calculate when to refresh next using REFRESH_RATE variable
    nextRefresh = REFRESH_RATE * 60 - timeTaken

    clear()
    print(f"""
Status: {status}


{userInfo}

Latest Refresh at: {datetime.now()}
Time Taken to get status: {timeTaken :.0f}s
Next refresh at: {datetime.now() + timedelta(seconds=nextRefresh)}
""")

    if timeTaken < 60 * REFRESH_RATE:
        time.sleep((60 * REFRESH_RATE) - timeTaken)
