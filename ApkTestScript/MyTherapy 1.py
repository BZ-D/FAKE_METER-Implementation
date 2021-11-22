# -*- coding:utf8 -*-

import time
from appium import webdriver
from selenium.webdriver.common.by import By

desired_caps = {'platformName': 'Android', 'platformVersion': '10.0', 'deviceName': 'emulator-5554',
                'appPackage': 'eu.smartpatient.mytherapy', 'appActivity': '.onboarding.WelcomeActivity',
                'newCommandTimeout': '1000', 'noReset': True}

driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)
time.sleep(20)

# 
# reminder time
el = driver.find_elements(By.CLASS_NAME, "android.widget.Button")[4]
el.click()

driver.quit()


'''
{
  "platformName": "Android",
  "platformVersion": "10",
  "deviceName": "emulator-5554",
  "noReset": true,
  "appPackage": "eu.smartpatient.mytherapy",
  "appActivity": ".onboarding.WelcomeActivity"
}
'''
