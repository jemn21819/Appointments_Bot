from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH =  "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://passportappointment.travel.state.gov/")

try:
    new_appmnt = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "rb-home-list-new"))
    )
    new_appmnt.click()

    nextButtonHome = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "btnHomeNext"))
    )
    nextButtonHome.click()

    yesInter = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "InternationalTravel-yes"))
    )
    yesInter.click()

    dateTravel = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "DateTravel"))
    )
    dateTravel.send_keys("03/25/2021")

    noVisa = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"VisaNeeded-no"))
    )
    noVisa.click()

    household = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@data-val='2']" ))
    )
    household.click()


    notRobot = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@id='recaptcha-anchor']"))
    )
    notRobot.click()

    submitButton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='submit']"))
    )
    submitButton.click()

except:
    driver.quit()
