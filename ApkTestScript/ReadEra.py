# -*- coding:utf8 -*-

import time
from appium import webdriver
from selenium.webdriver.common.by import By

desired_caps = {'platformName': 'Android', 'platformVersion': '10.0', 'deviceName': 'emulator-5554',
                'appPackage': 'org.readera', 'appActivity': 'com.readera.MainActivity', 'newCommandTimeout': '1000',
                'noReset': True}

driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)
time.sleep(10)

# 安装后跳过引导界面到字体下拉页面
el = driver.find_elements(By.ID, "org.readera:id/arg")[3]
el.click()


driver.quit()

'''
{
  "platformName": "Android",
  "platformVersion": "10",
  "deviceName": "emulator-5554",
  "noReset": true,
  "appPackage": "org.readera",
  "appActivity": "com.readera.MainActivity"
}
'''