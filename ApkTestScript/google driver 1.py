# -*- coding:utf8 -*-

import time
from appium import webdriver

desired_caps = {'platformName': 'Android', 'platformVersion': '7.0', 'deviceName': 'emulator-5554',
                'appPackage': 'com.google.android.apps.docs',
                'appActivity': 'com.google.android.apps.docs.app.NewMainProxyActivity', 'noReset': True}

'''
make sure the screen is under the screen "file"
'''

# test action 1 click on more options
driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)
time.sleep(10)

el = driver.find_element_by_accessibility_id("More actions for paperRecord")
el.click()

driver.quit()
