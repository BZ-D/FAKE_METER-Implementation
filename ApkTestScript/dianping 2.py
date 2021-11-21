# -*- coding:utf8 -*-

import time
from appium import webdriver

desired_caps = {'platformName': 'Android', 'platformVersion': '10.0', 'deviceName': 'emulator-5554',
                'appPackage': 'com.dianping.v1', 'appActivity': 'com.dianping.main.guide.SplashScreenActivity',
                'newCommandTimeout': '1000', 'noReset': True}

driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)
time.sleep(10)


# home page
el = driver.find_element_by_android_uiautomator("new UiSelector().text(\"酒店/民宿\")")
el.click()

driver.quit()


'''
{
  "platformName": "Android",
  "platformVersion": "10",
  "deviceName": "emulator-5554",
  "noReset": true,
  "appPackage": "com.dianping.v1",
  "appActivity": "com.dianping.main.guide.SplashScreenActivity"
}
'''