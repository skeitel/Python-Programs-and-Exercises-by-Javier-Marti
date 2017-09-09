#Python program by Javier Marti
'''This program accesses a job searches website, extracts a list of jobs, selects a particular one and sends an application to that job offer
Copyright JavierMarti.co.uk'''

from selenium import webdriver
from bs4 import BeautifulSoup
import re

#driver = webdriver.Firefox()
chromedriver = 'D:\\Program files\\chromedriver_win32\\chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
driver.get("https://www.infojobs.net/jobsearch/search-results/list.xhtml#f1=1&item_showFilters=false&item_showExtraFilters=false&f2=20&f3=&f4=0&f5=&f6=9&f7=&f8=0&f9=0&f10=0&f11=0&f12=&f13=true&f14=true&f15=10&f16=true&f17=&f18=&f19=0&f20=4&f21=3002&f22=0&f23=26931879312&f24=0&f25=&f26=0&f27=false&f28=&f29=1&f30=&f31=-2147483648&f32=-2147483648&f34=&item_vieneUrlExecutive=false&item_id_push=&ajax=true&formId=form_relaunch")

# chromedriver = 'D:\\Program files\\chromedriver_win32\\chromedriver.exe'
# browser = webdriver.Chrome(chromedriver)
# browser.get('http://www.pof.com')

# offer_title = driver.find_elements_by_class_name('job-list-title')
# offer_description = driver.find_elements_by_class_name('job-list-description')
#print(driver.current_url) #This can be used as a unique ID

#THIS OPENS THE BROWSER ON JOB SEARCH LIST
#https://www.infojobs.net/jobsearch/search-results/list.xhtml#f1=1&item_showFilters=false&item_showExtraFilters=false&f2=20&f3=carpintero&f4=0&f5=&f6=9&f7=&f8=0&f9=0&f10=0&f11=1&f12=&f13=true&f14=true&f15=22,10&f16=true&f17=&f18=&f19=0&f20=0&f21=3012&f22=0&f23=-2147483648&f24=&f25=&f26=&f27=false&f28=&f29=1&f30=&f31=-2147483648&f32=-2147483648&f34=&item_vieneUrlExecutive=false&item_id_push=&ajax=true&formId=form_relaunch
#page = "https://www.infojobs.net/jobsearch/search-results/list.xhtml#f1=1&item_showFilters=false&item_showExtraFilters=false&f2=20&f3=&f4=0&f5=&f6=9&f7=&f8=0&f9=0&f10=0&f11=0&f12=&f13=true&f14=true&f15=10&f16=true&f17=&f18=&f19=0&f20=4&f21=3002&f22=0&f23=26931879312&f24=0&f25=&f26=0&f27=false&f28=&f29=1&f30=&f31=-2147483648&f32=-2147483648&f34=&item_vieneUrlExecutive=false&item_id_push"
page = "https://www.infojobs.net/jobsearch/search-results/list.xhtml#f1=1&item_showFilters=false&item_showExtraFilters=false&f2=20&f3=carpintero&f4=0&f5=&f6=9&f7=&f8=0&f9=0&f10=0&f11=0&f12=&f13=true&f14=true&f15=22,10&f16=true&f17=&f18=&f19=0&f20=0&f21=3002&f22=0&f23=-2147483648&f24=0&f25=&f26=0&f27=false&f28=&f29=1&f30=&f31=-2147483648&f32=-2147483648&f34=&item_vieneUrlExecutive=false&item_id_push"
soup = BeautifulSoup(page, 'html.parser')
print('Success logging in!')
#print(soup.prettify())

#THIS PRINTS EACH OFFER'S TITLE
# for el in offer_title:
#     print(el.text)
#driver.close()

#THIS SELECTS ELEMENTS FROM PAGE, CLICKS ON FIRST, LOGS IN AND SENDS APPLICATION
text_offer_title = driver.find_element_by_class_name('job-list-title')
text_job_offer = driver.find_element_by_class_name('job-list-description')
print(text_offer_title.text)
print(text_job_offer.text)
text_offer_title.click()
driver.implicitly_wait(3)
link = driver.find_element_by_partial_link_text('Inscribirme')
link.click()
email = driver.find_element_by_id('email')
email.send_keys('info@javiermarti.co.uk')
pssw = driver.find_element_by_id('id-password')
pssw.send_keys("artwater1")
pssw.submit()
sendButton = driver.find_element_by_id('botonEnviar')
sendButton.click()





