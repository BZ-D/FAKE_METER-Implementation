# -*- coding:utf8 -*-

import time
from appium import webdriver
from selenium.webdriver.common.by import By

desired_caps = {'platformName': 'Android', 'platformVersion': '7.0', 'deviceName': 'emulator-5554',
                'appPackage': 'com.google.android.apps.docs',
                'appActivity': 'com.google.android.apps.docs.app.NewMainProxyActivity', 'noReset': True}
'''
make sure the screen is under the screen "share"
'''

# test action 3 edit on message
driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)
time.sleep(10)

# after updated: com.google.android.apps.docs:id/add_collaborator_chips_textbox
el = driver.find_element(By.ID, "com.google.android.apps.docs:id/collaborator_recipient_text_view")
el.send_keys("people 1")

# after updated: com.google.android.apps.docs:id/add_collaborator_message
el = driver.find_element(By.ID, "com.google.android.apps.docs:id/message")
el.send_keys("message 1")

# ......

driver.quit()
