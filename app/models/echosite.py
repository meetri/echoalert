'''navigate echo site'''
import sys
import logging
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

class Echosite(object):

    KEYLOOKUP = {
            "Kn": "kn",
            "Co": "co",
            "Ag": "ag",
            "Progress (all activities)": "progress_all",
            "Course": "course",
            "Score": "score",
            "Progress (gradable)": "progress_gradable",
            "Or": "oral",
            "Wr": "wr"
            }


    def __init__(self):
        #self.browser = webdriver.Firefox(executable_path='../drivers/geckodriver',log_path='../logs/geckodriver.log')
        self.browser = webdriver.PhantomJS()
        self.browser.set_window_size(1024,768)
        self.waiter = WebDriverWait(self.browser,30)


    def shutdown(self):
        self.browser.quit()

    def login ( self, url, uname , upass ):

        logging.info("logging in to {}".format(url))

        self.browser.get(url)
        username = self.waiter.until ( EC.presence_of_element_located( (By.XPATH, "//input[@ng-model='ctrl.username']")) )
        pw = self.browser.find_element_by_xpath("//input[@ng-model='ctrl.password']")
        submit = self.browser.find_element_by_xpath("//button[@type='submit']")

        username.send_keys(uname)
        pw.send_keys(upass)
        submit.click()
        self.waiter.until ( EC.presence_of_element_located( (By.XPATH, "//button[@title='GRADEBOOK']")) )


    def click_gradebook( self ):
        gradebook = self.browser.find_element_by_xpath("//button[@title='GRADEBOOK']")
        gradebook.click()
        self.waiter.until ( EC.presence_of_element_located( (By.CLASS_NAME, "buzz-student-objective-summary")) )


    def click_activities( self ):
        activities = self.browser.find_element_by_xpath("//button[@title='COURSE ACTIVITIES']")
        activities.click()
        self.waiter.until ( EC.presence_of_element_located( (By.CLASS_NAME, "buzz-course-selector")) )

    def get_courses( self ):
        self.click_activities()
        dom_courselist = self.browser.find_elements_by_class_name("buzz-course-selector-column")

        courselist = []
        for dom_item in dom_courselist:
            dom_courses = dom_item.find_elements_by_xpath(".//li")
            todolist = []
            for dom_course in dom_courses:
                course_name = dom_course.find_element_by_class_name("buzz-course-title").text
                course_term = dom_course.find_element_by_class_name("buzz-course-term").text
                courselist += [{
                    "course": course_name,
                    "term": course_term,
                }]

        return courselist

    @staticmethod
    def filter_course_grades( name , esum ):
        for course in esum:
            if name in course['course']:
                return course

        return None

    def get_course_assignments( self, course_name ):

        self.click_activities()
        course = self.browser.find_element_by_xpath("//div[@title='{}']".format(course_name))
        course.click()
        self.waiter.until ( EC.presence_of_element_located( (By.CLASS_NAME, "buzz-course-summary")) )

        items = self.browser.find_elements_by_xpath("//ul//li[@class='buzz-to-do-item ng-scope']")
        todoitems = []
        for p in items:
            title = p.find_element_by_class_name("buzz-to-do-title").text
            duedate = p.find_element_by_class_name("buzz-to-do-date").text
            todoitems += [{
                'title': title,
                'due': duedate
            }]

        self.browser.back()
        self.waiter.until ( EC.presence_of_element_located( (By.CLASS_NAME, "buzz-course-selector")) )

        return todoitems


    def get_assignments( self ):
        self.click_activities()
        courselist = self.browser.find_elements_by_class_name("buzz-course-selector-column")

        assignments = []
        for item in courselist:
            courses = item.find_elements_by_xpath(".//li")
            todolist = []
            for course in courses:
                course_name = course.find_element_by_class_name("buzz-course-title").text
                course_term = course.find_element_by_class_name("buzz-course-term").text
                course.click()
                self.waiter.until ( EC.presence_of_element_located( (By.CLASS_NAME, "buzz-course-summary")) )
                res = item.find_elements_by_xpath("//ul//li[@class='buzz-to-do-item ng-scope']")
                todoitems = []
                for p in res:
                    title = p.find_element_by_class_name("buzz-to-do-title").text
                    duedate = p.find_element_by_class_name("buzz-to-do-date").text
                    todoitems += [{
                        'title': title,
                        'due': duedate
                    }]
                if len(todoitems) > 0:
                    assignments += [{
                        "course": course_name,
                        "term": course_term,
                        "todo": todoitems,
                    }]
                self.browser.back()
                self.waiter.until ( EC.presence_of_element_located( (By.CLASS_NAME, "buzz-course-selector")) )

        return assignments


    def get_grade_summary( self ):

        #self.login( account['echo_site'], account['echo_username'],account['echo_password'] )
        self.click_gradebook()

        header = self.browser.find_elements_by_xpath("//table//thead//th")
        courses = self.browser.find_elements_by_xpath("//table//tbody//tr")

        course_map = []
        for course in courses:
            info = course.find_elements_by_xpath(".//td")
            m = {}
            cnt = 0
            for head in header:
                h = str(head.text)
                if len(h) > 0:
                    k = Echosite.KEYLOOKUP[h]
                    v = str(info[cnt].text)
                    if '%' in v:
                        m[k] = float(v.replace('%',''))
                    else:
                        m[k] = str(info[cnt].text)

                    if m[k] == '':
                        m[k] = None
                cnt +=1

            course_map += [m]

        return course_map

