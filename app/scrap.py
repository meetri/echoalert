#!/usr/bin/python
import psycopg2
import os
import sys
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.keys import Keys

script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_path + "/models")

import accounts, echosite

echo = new Echosite()
# GO HEADLESS - LOG INTO ECHO AND EXTRACT GRADE DETAILS
browser = webdriver.Firefox(executable_path='../drivers/geckodriver',log_path='../logs/geckodriver.log')

# GET ACCOUNT DETAILS FROM POSTGRES DATABASE
try:
    # TODO: Externalize config properties...
    conn = psycopg2.connect("dbname='echoalert' user='postgres' host='192.168.59.104' port='32768' password='abignewworld'")
except:
    print "I am unable to connect to the database"
    sys.exit()


echo = new echosite("",browser)
ac = new accounts(conn)
results = ac.get_user_paginate(0,1))

for result in results:
    summary = echosite.get_grade_summary(browser,result)



cur = conn.cursor()
cur.execute("""SELECT id,echo_username,echo_password, notification_email,notification_sms FROM echoalert.accounts""")
rows = cur.fetchall()

if len(rows) == 0:
    print "can't find any accounts to scrape"
    sys.exit()

uname = rows[0][1]
pword = rows[0][2]

# GO HEADLESS - LOG INTO ECHO AND EXTRACT GRADE DETAILS
browser = webdriver.Firefox(executable_path='../drivers/geckodriver',log_path='../logs/geckodriver.log')
waiter = WebDriverWait(browser,10)

print "accessing https://amcanhs.echo-ntn.org/ ..."
browser.get("https://amcanhs.echo-ntn.org/")

username = waiter.until ( EC.presence_of_element_located( (By.XPATH, "//input[@ng-model='ctrl.username']")) )

print "sending login credentials..."
username.send_keys(uname)
pw = browser.find_element_by_xpath("//input[@ng-model='ctrl.password']")
pw.send_keys(pword)
submit = browser.find_element_by_xpath("//button[@type='submit']")
submit.click()

gradebook = waiter.until ( EC.presence_of_element_located( (By.XPATH, "//button[@title='GRADEBOOK']")) )
gradebook.click()

summary = waiter.until ( EC.presence_of_element_located( (By.CLASS_NAME, "buzz-student-objective-summary")) )

header = browser.find_elements_by_xpath("//table//thead//th")
courses = browser.find_elements_by_xpath("//table//tbody//tr")

course_map = {}
course_cnt = 0
for course in courses:
    info = course.find_elements_by_xpath(".//td")
    m = {}
    cnt = 0
    for head in header:
        h = str(head.text)
        if len(h) > 0:
            m[h] = str(info[cnt].text)
        cnt +=1
    course_map[course_cnt] = m
    course_cnt +=1
    #print "Course: %s, Score: %s, Progress: %s" %(info[1].text,info[3].text, info[4].text )


for idx,course in course_map.iteritems():
    print "{1} - {0}".format( course["Course"], course["Score"])

for k,v in course_map[0].iteritems():
    print "{}:={}".format(k,v)

browser.quit()

#gradebook = browser.find_element(by='title',value='GRADEBOOK')
#gradebook.click()
