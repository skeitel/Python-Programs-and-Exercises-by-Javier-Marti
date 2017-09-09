#Python program by Javier Marti
'''This program logs into Linkedin, scrolls down a few times, then parses the page, extracting profile links and opening them in new tabs.
Copyright JavierMarti.co.uk'''

import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time, random
import requests, webbrowser, bs4
import smtplib

def log_in():
    if browser.find_element_by_id('login-email'):
        try:
            email = browser.find_element_by_id('login-email')
            email.send_keys('niquel757@gmail.com')
            pssw = browser.find_element_by_id('login-password')
            time.sleep(random.uniform(0.2,0.8))
            pssw.send_keys("lalala1")
            pssw.submit()
            print('Logging in...')
        except:
            pass

def getPeopleLinks():
    page = BeautifulSoup(browser.page_source,'lxml')
    global links
    links = []
    count = 0
    for link in page.find_all('a'):
        url = link.get('href')
        #url = str(url)
        if url:
            if 'hp-feed-member-name' in url and link not in links:
                links.append(url)
                print('link',count,'has been appended to dict')
                count = count + 1
    #print(links)
    return links

def send_email():
    # content = 'Lkn program has run. Profiles visited:' + len(final_links)
    content = 'Lkn program has run. Profiles visited: ' + str(len(final_links))
    mail = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('ram_308@yahoo.com','ifeelhappy1')
    mail.sendmail('ram_308@yahoo.com','niquel757@gmail.com', content)


# browser = webbrowser.open('http://www.linkedin.com') #WORKS TO OPEN IN NEW TAB

browser = webdriver.Firefox()
page = browser.get('http://www.linkedin.com')

log_in()

time.sleep(random.uniform(1,2))
htmlElem = browser.find_element_by_tag_name('html')
for i in range(2):
    htmlElem.send_keys(Keys.PAGE_DOWN)
    time.sleep(random.uniform(1,2))

getPeopleLinks()
print('done')
# print('*****************************')

#numOpen = min(50, len(links))
# for i in range(numOpen):

print('Links dict contains ',len(links),'records')
final_links = []
for el in links:
    if el not in final_links:
        final_links.append(el)
print('Final links dict contains ',len(final_links),'records')
print('Opening links in browser now...')

for el in final_links[0:3]:
    browser.find_element_by_tag_name('html').send_keys(Keys.CONTROL + "t")
    browser.find_element_by_tag_name('html').send_keys(Keys.CONTROL + "l")
    browser.find_element_by_tag_name('html').send_keys(el)
    browser.find_element_by_tag_name('html').send_keys(Keys.ENTER)
    time.sleep(random.uniform(1,2))

# webbrowser.open('http://www.linkedin.com')
#
# email = browser.find_element_by_id('login-email')
# email.send_keys('niquel757@gmail.com')
# pssw = browser.find_element_by_id('login-password')
# time.sleep(random.uniform(0.2,0.8))
# pssw.send_keys("lalala1")
# pssw.submit()
# print('Logging in second time...')
#
# for i in range(len(final_links)):
#     #email = browser.find_element_by_id('login-email')
#     webbrowser.open(final_links[i])
#     print('Link number',i,'has been opened')
#     time.sleep(random.uniform(1.2,3.4))
#
# send_email()

#https://www.linkedin.com/in/ayeshakhanior?authType=name&authToken=1PnP&trk=hp-feed-member-name
#?authType=name&authToken=1PnP&trk=hp-feed-member-name
#https://www.linkedin.com/in/jamescaldwellinnov8?authType=name&authToken=dst7&trk=hp-feed-member-name

####################################################################################


# # from selenium import webdriver
# # from selenium.webdriver.common.keys import Keys
# # import random, os, time
# # from bs4 import BeautifulSoup
# # import urllib.request
#
# # from collections import deque
# # def log_in():
# # 	email = browser.find_element_by_id('login-email')
# # 	email.send_keys('niquel757@gmail.com')
# # 	pssw = browser.find_element_by_id('login-password')
# # 	time.sleep(random.uniform(0.5,1.5))
# # 	pssw.send_keys("lalala1")
# # 	pssw.submit()
# # 	print('Logging in...')
# #
# # browser = webdriver.Firefox()
# # page = browser.get('http://www.linkedin.com')
# # login_field = browser.find_elements_by_xpath('//*[@id="login-email"]')
# #
# # if login_field:
# # 	log_in()
# #
# # def getPeopleLinks():
# # 	page = BeautifulSoup(browser.page_source,'lxml')
# # 	links = []
# # 	for link in page.find_all('a'):
# # 		url = link.get('href')
# # 		if url:
# # 			if 'hp-feed-member-name' in url:
# # 				links.append(url)
# # 	return links
# #
# # getPeopleLinks()
# # print(getPeopleLinks())
# # for el in getPeopleLinks():
# # 	browser = webdriver.Firefox()
# # 	page = browser.get(el)
# # 	if reLogin:
# # 		reLogin()
# # 	else:
# # 		continue
#
#
# def reLogin():
# 	browser = webdriver.Firefox()
# 	page = browser.get('https://www.linkedin.com/start/join?trk=login_reg_redirect&session_redirect=https%3A%2F%2Fwww.linkedin.com%2Fprofile%2Fview%3FauthType%3Dname%26id%3DAAMAAAO03I8BW4VlckV4bkkK0z65R4vXXbIGcTI%26authToken%3DY4EN%26trk%3Dhp-feed-member-name')
# 	req = urllib.request.urlopen('https://www.linkedin.com/start/join?trk=login_reg_redirect&session_redirect=https%3A%2F%2Fwww.linkedin.com%2Fprofile%2Fview%3FauthType%3Dname%26id%3DAAMAAAO03I8BW4VlckV4bkkK0z65R4vXXbIGcTI%26authToken%3DY4EN%26trk%3Dhp-feed-member-name')
# 	soup = BeautifulSoup(req, 'html.parser')
# 	req.addheaders = [ ('User-agent', 'Mozilla/5.0') ]
# 	linki = soup.find('p', class_ = 'signin-link')
# 	#linki = soup.find('p', class_ = 'sign-in-link') #doesn't work
# 	# soup.find_all('p', class_ = 'signin-link') #doesn't work
# 	# soup.find_all('p', class_ = 'sign-in-link') #doesn't work
# 	#news = urllib.request.urlopen(linki).read() #doesn't work
# 	#news = urllib.request.urlopen(linki).read() #doesn't work
# 	print(news)
# 	browser.close()
#
# 	# time.sleep(2)
# 	# email = browser.find_element_by_xpath('//*[@id="uno-reg-join"]')
# 	# email.send_keys('niquel757@gmail.com')
# 	# pssw = browser.find_element_by_id('login-password')
# 	# time.sleep(random.uniform(0.5,1.5))
# 	# pssw.send_keys("lalala1")
# 	# pssw.submit()
# 	# print('Logging in...')
#
# reLogin()

#print(getPeopleLinks())
# for url in getPeopleLinks()[:3]:
# 	url = "'"+url+"'"
# 	print(url)
# 	#print(url,'\n') #for testing purposes
# 	browser = webdriver.Firefox
# 	browser.get(url)

#DIDN'T WORK
# total_links = getPeopleLinks()
# for el in getPeopleLinks()[:3]:
# 	print(el)
# 	el = ('"'+el+'"')
# 	browser.get(el)

# total_links = getPeopleLinks()
# for link in total_links:
# 	browser.get(link)
# 	#print(link)


# numOpen = min(5, len(links))
# for i in range(numOpen):
#     #webdriver.open('http://google.com' + linkElems[i].get('href'))
# 	#webdriver.open('http://google.com' + linkElems[i].get('href'))
# 	webdriver.open(links[i])
# 	time.sleep(random.uniform(1,2))

########################################################################
# THIS WORKS TO GET A LIST OF LINKS FROM A DICTIONARY AND VISIT THEM IN NEW WINDOWS#####
# from selenium import webdriver
# from bs4 import BeautifulSoup
# import time, random
# import urllib.request
#
# article = "http://www.vox.com/2016/2/5/10919082/solar-storage-economics"
# headers = {'User-agent':'Mozilla/5.0'}
# req = urllib.request.Request(article, headers={'User-agent': 'Mozilla/5.0'})
# html = urllib.request.urlopen(req).read()
#
# soup = BeautifulSoup(html,'lxml')
#
# def getPeopleLinks():
#     global links
#     links = []
#     for link in soup.find_all('a')[1:6]:
#         url = link.get('href')
#         if url:
#             if 'http://' in url:
#                 links.append(url)
#     return links
#
# print(getPeopleLinks())
#
#
# count = 0
# for el in getPeopleLinks():
#     #print(el)
#     #here try list.pop, enumerate, or open links in range
#     person = links.pop()
#     browser = webdriver.Firefox()
#     browser.get(person)
#     count += 1
#     time.sleep(random.uniform(0.5,1))



#################################################################################
#LINKEDIN BOT FOR 2.7 THAT DOES NOT WORK, POSSIBLY DUE TO URLPARSE NOT AVAILABLE
# import argparse, os, time
# import urlparse, random
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup
#
# def getPeopleLinks(page):
# 	links = []
# 	for link in page.find_all('a'):
# 		url = link.get('href')
# 		if url:
# 			if 'profile/view?id=' in url:
# 				links.append(url)
# 	return links
#
# def getJobLinks(page):
# 	links = []
# 	for link in page.find_all('a'):
# 		url = link.get('href')
# 		if url:
# 			if '/jobs' in url:
# 				links.append(url)
# 	return links
#
# def getID(url):
# 	pUrl = urlparse.urlparse(url)
# 	return urlparse.parse_qs(pUrl.query)['id'][0]
#
# def ViewBot(browser):
# 	visited = {}
# 	pList = []
# 	count = 0
# 	while True:
# 		#sleep to make sure everything loads, add random to make us look human.
# 		time.sleep(random.uniform(3.5,6.9))
# 		page = BeautifulSoup(browser.page_source)
# 		people = getPeopleLinks(page)
# 		if people:
# 			for person in people:
# 				ID = getID(person)
# 				if ID not in visited:
# 					pList.append(person)
# 					visited[ID] = 1
# 		if pList: #if there is people to look at look at them
# 			person = pList.pop()
# 			browser.get(person)
# 			count += 1
# 		else	: #otherwise find people via the job pages
# 			jobs = getJobLinks(page)
# 			if jobs:
# 				job = random.choice(jobs)
# 				root = 'http://www.linkedin.com'
# 				roots = 'https://www.linkedin.com'
# 				if root not in job or roots not in job:
# 					job = 'https://www.linkedin.com'+job
# 				browser.get(job)
# 			else:
# 				print "I'm Lost Exiting"
# 				break
#
# 		#Output (Make option for this)
# 		print "[+] "+browser.title+" Visited! \n("\
# 			+str(count)+"/"+str(len(pList))+") Visited/Queue)"
#
#
# def Main():
# 	parser = argparse.ArgumentParser()
# 	parser.add_argument("email", help="linkedin email")
# 	parser.add_argument("password", help="linkedin password")
# 	args = parser.parse_args()
#
# 	browser = webdriver.Firefox()
#
# 	browser.get("https://linkedin.com/uas/login")
#
#
# 	emailElement = browser.find_element_by_id("session_key-login")
# 	emailElement.send_keys(args.email)
# 	passElement = browser.find_element_by_id("session_password-login")
# 	passElement.send_keys(args.password)
# 	passElement.submit()
#
# 	os.system('clear')
# 	print "[+] Success! Logged In, Bot Starting!"
# 	ViewBot(browser)
# 	browser.close()
#
# if __name__ == '__main__':
# 	Main()

