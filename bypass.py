"""
    ByPass Google reCAPTCHA V2
    Shahzaib Chadhar
    YouTube Channel: NIKO TECH
"""

import urllib
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import sys
import time
from fake_useragent import UserAgent
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

audioToTextDelay = 10
delayTime = 6
audioFile = "\\payload.mp3"
recaptchaId = "recaptcha-demo"
URL = "https://www.google.com/recaptcha/api2/demo"
SpeechToTextURL = "https://speech-to-text-demo.ng.bluemix.net/"


def delay():
    """
        Delay between performing the task
    """
    time.sleep(delayTime)


def audioToText(audioFile):
    """ Converting audio mp3 to text """

    driver.execute_script('''window.open("","_blank")''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)

    delay()
    audioInput = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    # upload file mp3 to input
    audioInput.send_keys(audioFile)

    time.sleep(audioToTextDelay)
    # waiting for conversion to text

    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')

    result = text.text  # final text after conversion

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result


try:
    # setup chrome web driver
    ua = UserAgent()
    userAgent = ua.random
    option = webdriver.ChromeOptions()
    # option.add_argument("--headless") #uncomment this option to use chrome as headless
    option.add_argument("start-maximized")
    driver = webdriver.Chrome(options=option)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": userAgent})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
except Exception as e:
    print(e)
    sys.exit("[-] Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")


def isBlocked():
    try:
        errors = driver.find_element_by_class_name('rc-doscaptcha-header-text')
        print("TEXT: ", errors.text)
        if errors.text == "Try again later":
            return True
        return False
    except selenium.common.exceptions.NoSuchElementException:
        return False


driver.set_page_load_timeout(2000)
delay()
# go to website which have recaptcha protection
driver.get(URL)
print("Getting Captcha")
g_recaptcha = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, recaptchaId)))
outerIframe = g_recaptcha.find_element_by_tag_name('iframe')
print("Got captcha")
ActionChains(driver).move_to_element(outerIframe).pause(3).click(outerIframe).perform()
if isBlocked():
    sys.exit("Caught/Blocked by Google")
# click captcha to solve up
delay()
iframes = driver.find_elements_by_tag_name('iframe')
audioBtnFound = False
audioBtnIndex = -1
# go to audio solution
for index in range(len(iframes)):
    driver.switch_to.default_content()
    iframe = driver.find_elements_by_tag_name('iframe')[index]
    # delay()
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(delayTime)
    try:
        audioBtn = driver.find_element_by_id("recaptcha-audio-button")
        # delay()
        ActionChains(driver).move_to_element(audioBtn).pause(1).click(audioBtn).perform()
        # time.sleep(3)

        print("[INFO] Audio Button Clicked!")
        if isBlocked():
            sys.exit("Caught/Blocked by Google")
        audioBtnFound = True
        audioBtnIndex = index
        break
    except Exception as e:
        pass

if audioBtnFound:
    # if audio button found then procced
    delay()
    try:
        while True:
            # get the mp3 audio file

            src = driver.find_element_by_id("audio-source").get_attribute("src")
            print("[INFO] Audio src: %s" % src)

            # download the mp3 audio file from the source
            urllib.request.urlretrieve(src, os.getcwd() + audioFile)

            # Speech To Text Conversion
            key = audioToText(os.getcwd() + audioFile)
            print("[INFO] Recaptcha Key: %s" % key)
            delay()
            driver.switch_to.default_content()
            iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
            delay()
            driver.switch_to.frame(iframe)

            # key in results and submit
            # input field where we have to write the audio text
            # delay()
            inputField = driver.find_element_by_id("audio-response")
            inputField2 = driver.find_element_by_id("audio-response")
            ActionChains(driver).move_to_element(inputField).pause(1).click(inputField).perform()
            time.sleep(1)
            for k in key:
                inputField2.send_keys(k)
                time.sleep(0.5)
            delay()
            ActionChains(driver).move_to_element(inputField2).pause(1).send_keys(Keys.ENTER).perform()
            delay()
            if isBlocked():
                sys.exit("Caught/Blocked by Google")

            # check if verification failed or passed?
            err = driver.find_elements_by_class_name('rc-audiochallenge-error-message')[0]
            if err.text == "" or err.value_of_css_property('display') == 'none':
                print("[INFO] Success!")
                break
            # if failed while loop run again and again untill success!

    except Exception as e:
        print(e)
        sys.exit("[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests")
else:
    sys.exit("[INFO] Audio Play Button not found! In Very rare cases!")
