# -*- coding:utf8 -*-

import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '10.0'
desired_caps['deviceName'] = 'emulator-5554'
desired_caps['appPackage'] = 'com.google.earth'
desired_caps['appActivity'] = 'com.google.android.apps.earth.EarthActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True


driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)
time.sleep(10)


'''
requires the page in the main page
'''
el = driver.find_elements_by_class_name("android.widget.ImageView")[4]
el.click()

driver.quit()


'''
{
  "platformName": "Android",
  "platformVersion": "10",
  "deviceName": "emulator-5554",
  "noReset": true,
  "appPackage": "com.google.earth",
  "appActivity": "com.google.android.apps.earth.EarthActivity"
}
'''