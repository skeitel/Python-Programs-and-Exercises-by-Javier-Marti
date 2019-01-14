#Python program by Javier Marti
'''This program obtains a list of jobs in GuardianJobs, stores the info in notepad and sends an email
Copyright JavierMarti.co.uk'''

#THIS LOOKS FOR A LIST OF JOBS ON GUARDIANJOBS, STORES IN NOTEPAD AND SENDS AN EMAIL
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('https://jobs.theguardian.com/searchjobs/?LocationId=1500&keywords=managing+director&radialtown=London+(Central)%2c+London+(Greater)&countrycode=GB')

chromedriver = 'C:\\chromedriver\\chromedriver.exe'
browser = webdriver.Chrome(chromedriver)


elem = browser.find_elements_by_class_name('lister__header')

helloFile = open('C:\\Users\\SK\\Downloads\\test_emails.txt', "w")
helloFile.write('This is the updated list of jobs: \n') #will return a single line/string
helloFile.close()

with open('C:\\Users\\SK\\Downloads\\test_emails.txt', "a") as f: #this opens the file, process its contents, and closes it
    for el in elem:
       f.write(el.text+"\n")


# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
textfile = 'test_email.txt'

with open(textfile) as fp:
    # Create a text/plain message
    msg = MIMEText(fp.read())


# me == the sender's email address
# you == the recipient's email address
me = 'email1'
you = 'email2'


msg['Subject'] = 'The contents of the file %s' % textfile
msg['From'] = me
msg['To'] = you


# print('enter ymail password to send email ')
# pa = input()
mail = smtplib.SMTP('smtp.mail.yahoo.com', 587)
mail.ehlo()
mail.starttls()
#mail.login('email1',pa)
mail.login('email1', 'password_goes_here') #delete this line if you want it back to password-dependent
mail.send_message(msg)
mail.quit()

# # Send the message via our own SMTP server.
# s = smtplib.SMTP('localhost')
# s.send_message(msg)
# s.quit()

#------------------
#code that works to extract a list of Guardian jobs
# import selenium.webdriver as webdriver
#
# def listOfJobs():
#     browser = webdriver.Firefox()
#     browser.get('https://jobs.theguardian.com/searchjobs/?LocationId=1500&keywords=managing+director&radialtown=London+(Central)%2c+London+(Greater)&countrycode=GB')
#     #elem = browser.find_elements_by_class_name('lister__header')
#     elem = browser.find_elements_by_xpath('//h3/a/span')
#     for el in elem:
#         listOfJobs.printText = print(el.text)
#
#     browser.close()
#
# listOfJobs()
#############################################################################

#THIS LOOKS FOR EMPLOYERS IN INFOJOBS AND STORES THEM AS NOTEPAD LIST WITHOUT BRACKETS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0


def get_companies():
    chromedriver = 'C:\\chromedriver\\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver)
    #driver = webdriver.Firefox()
    driver.get("https://www.infojobs.net/jobsearch/search-results/list.xhtml#f1=1&item_showFilters=false&item_showExtraFilters=false&f2=20&f3=&f4=0&f5=&f6=9&f7=&f8=0&f9=0&f10=0&f11=0&f12=&f13=true&f14=true&f15=10&f16=true&f17=&f18=&f19=0&f20=4&f21=3012&f22=0&f23=-2147483648&f24=&f25=&f26=&f27=false&f28=&f29=1&f30=&f31=31&f32=-2147483648&f34=&item_vieneUrlExecutive=false&item_id_push=&ajax=true&formId=form_relaunch")

    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pageNext")))
        print('Element located!')


        #time.sleep(5)
        # only_BCN = driver.find_element_by_xpath('//*[@id="nav2_top"]/li[2]/label/a')
        # only_BCN.click()
        # time.sleep(2)
        global dict_companies
        dict_companies = []
        for i in range(2):
            text_offer_subtitle = driver.find_elements_by_class_name('job-list-subtitle')
            for el in text_offer_subtitle:
                if el.text not in dict_companies:
                    dict_companies.append(el.text)
                    print('Adding record to databse')
                else:
                    print('Duplicate record already in database')
            print('There are now '+(str(len(dict_companies)))+' records in the dictionary')
            next_button = driver.find_element_by_xpath('//*[@id="pageNext"]')
            if next_button:
                next_button.click()
            else:
                driver.close()
            time.sleep(random.uniform(3.5,5))

    finally:
        driver.quit()

get_companies()
print(dict_companies)

testFile = open('test_infojobs.txt', 'a')
testFile.write(str(dict_companies)[1:-1])  #last part deletes the square brakets
testFile.close()
#########################################################################
