# -*- coding:utf8 -*-

import time
from appium import webdriver
from selenium.webdriver.common.by import By

desired_caps = {'platformName': 'Android', 'platformVersion': '10.0', 'deviceName': 'emulator-5554',
                'appPackage': 'hd.camera', 'appActivity': '.MainActivity', 'newCommandTimeout': '1000', 'noReset': True}

driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)
time.sleep(10)

'''
requires the page in the main page
'''
el = driver.find_elements(By.CLASS_NAME, "android.widget.ImageButton")[9]
el.click()

driver.quit()

'''
{
  "platformName": "Android",
  "platformVersion": "10",
  "deviceName": "emulator-5554",
  "noReset": true,
  "appPackage": "hd.camera",
  "appActivity": ".MainActivity"
}
'''
