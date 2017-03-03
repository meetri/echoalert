'''navigate echo site'''
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.keys import Keys


class Echosite(object):


    def __init__(self, url):
        self.browser = webdriver.Firefox(executable_path='../drivers/geckodriver',log_path='../logs/geckodriver.log')
        self.waiter = WebDriverWait(self.browser,10)
        self.url = url


    def login ( self, user, pass ):
        self.browser.get("https://amcanhs.echo-ntn.org/")
        username = waiter.until ( EC.presence_of_element_located( (By.XPATH, "//input[@ng-model='ctrl.username']")) )

        print "sending login credentials..."
        username.send_keys(uname)
        pw = browser.find_element_by_xpath("//input[@ng-model='ctrl.password']")
        pw.send_keys(pword)
        submit = browser.find_element_by_xpath("//button[@type='submit']")
        submit.click()


    def navigate_to_summary(self ):





