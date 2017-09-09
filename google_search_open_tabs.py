#Python program  by Javier Marti
'''This program searches for any numvber of search terms (plus extra additional words)and scrapes for emails the
first X number of results or several result pages. Once this is done the program uses Selenium and Regex to extract the email. Then the program verifies that emails are not
already in the existing list, and if so appends them to the list.
'''
#Copyright JavierMarti.co.uk

import requests,re,bs4
from selenium import webdriver
from bs4 import BeautifulSoup
import time,random

# search_terms = ['Sevilla']
# added_terms = 'seleccion de personal executive search email contact? @'
# search_terms = ['Hawaii','Cuba']
# added_terms = 'jobs accommodation contact email @'
# added_terms = 'London UK -KY -Ontario -jobs -vacancy -vacancies -directory'
search_terms = ['cognizant Technology Solutions', 'Computer Sciences Corporation', 'Corporate Executive Board', 'Deloitte Consulting', 'Detica', 'Ernst & Young', 'Fulcrum Worldwide', 'FTI Consulting', 'Grant Thornton', 'Hay Group', 'HCL Axon', 'Hewitt Associates', 'Hitachi Consulting', 'Horváth & Partners', 'HP Enterprise Services', 'Huron Consulting Group', 'IBM Global Business Services', 'ICF International', 'Ikon Marketing Consultants', 'Imdad logistics', 'IPL Information Processing Limited', 'ITN Consulting', 'KPMG', 'Kurt Salmon', 'L.E.K. Consulting', 'Logica', 'Marsh & McLennan Companies', 'McGladrey', 'McKinsey & Company', 'Mercer', 'Mitchell Madison Group', 'Monitor Group', 'Mott MacDonald', 'Navigant Consulting', 'Oliver Wyman', 'PA Consulting Group', 'Perficient', 'PricewaterhouseCoopers', 'Protiviti', 'PRTM', 'QualPro', 'Rambøll Management', 'Roland Berger Strategy Consultants', 'The Saint Consulting Group', 'Sapient', 'Schlumberger Business Consulting', 'SDG Group', 'Simon-Kucher & Partners', 'Slalom Consulting', 'SM&A', 'Strategy& (formerly Booz & Company)', 'Tata Consultancy Services', 'Tefen', 'Towers Watson', 'West Monroe Partners', 'WS Atkins PLC']
added_terms = ' contact email @'
number_of_sites = 2  #NUMBER OF SITES (SEARCH RESULTS) TO PARSE FOR EMAILS
number_of_search_pages = 1   #NUMBER OF GOOGLE RESULT PAGES TO PARSE (SEARCH RESULTS) TO PARSE FOR EMAILS

dicti_pretty_links = str(search_terms) + str(added_terms)

global remove_list
remove_list = ['.gif', '.png', 'example.com', 'abuse@', 'yourdomain', 'jpg','jpeg','database@','fbl@','ftp@','noc@','post@','postbox@','postmaster@','privacy@','remove@','root@','spam@','subscribe@','uucp@','webmaster@','welcome@','www@','%20','glassdoor','fake','test','email.com']


def google_this_for_emails():                #Googles and gets the first few links

    global scrapedEmails
    scrapedEmails = []
    global emails_not_found
    emails_not_found = []
    global dicti_pretty_links

    # This searches for certain keywords in Google and parses results with BS
    for el in search_terms:
        webpage = 'http://google.com/search?q=' + '%20'.join(el.split()) + '%20' + '%20'.join(added_terms.split())
        print('\n Searching for the terms...', el, added_terms)
        headers = {'User-agent': 'Mozilla/5.0'}
        res = requests.get(webpage, headers=headers)
        # res.raise_for_status()

        statusCode = res.status_code
        if statusCode == 200:
            soup = bs4.BeautifulSoup(res.text, 'lxml')
            serp_res_rawlink = soup.select('.r a')

            dicti = []  # This gets the href links
            for link in serp_res_rawlink:
                url = link.get('href')
                if 'pdf' not in url:
                    dicti.append(url)

            dicti_url = []  # This cleans the "url?q=" from link
            for el in dicti:
                if '/url?q=' in el:
                    result = (el.strip('/url?q='))
                    dicti_url.append(result)
            # print(dicti_url)

            global dicti_pretty_links
            dicti_pretty_links = []  # This cleans the gibberish at end of url
            for el in dicti_url[0:(number_of_sites)]:
                pretty_url = el.partition('&')[0]
                dicti_pretty_links.append(pretty_url)
            print(dicti_pretty_links)
            time.sleep(random.uniform(3,7))

        else:
            print('StatusCode was not 200, but ' + str(statusCode))

    print('Number of emails in pretty links', len(dicti_pretty_links))

    for el in dicti_pretty_links:
        #######START OF THE BS CHECK FOR EMAILS BY REGEX #################
        # This opens page in BS for parsing emails

        try:
            webpage = (el)
            headers = {'User-agent': 'Mozilla/5.0'}
            res = requests.get(webpage, headers=headers)

        except:
            pass

        try:
            statusCode = res.status_code
            if statusCode == 200:
                soup = bs4.BeautifulSoup(res.text, 'lxml')
                # if "</form>" in soup:
                try:

                    # This is the first way to search for an email in soup, "MO"
                    emailRegex = re.compile(r'([a-zA-Z0-9_.+]+@[a-zA-Z0-9_.+.+]+)', re.VERBOSE)
                    mo = emailRegex.findall(res.text)
                    print('THIS BELOW IS MO')
                    print(mo, 'EMAILS COMING FROM: ', el)
                    for el in mo:
                        if el not in scrapedEmails:
                            scrapedEmails.append(el)
                except:
                    pass

                try:
                    # This is the second way to search for an email in soup, "MAILTOS":
                    mailtos = soup.select('a[href^=mailto]')
                    print('THIS BELOW IS MAILTOS')
                    print(mailtos, el, '<-- THIS IS THE WEBSITE IT IS COMING FROM')

                    dicti_cleaner = []
                    target = re.compile(r'mailto')
                    for el in mailtos:
                        mo = target.search(str(el))
                        dicti_cleaner.append(el)

                    temp = []
                    for el in dicti_cleaner:
                        pretty_url = str(el).partition(':')[2]
                        second_url = str(pretty_url).partition('"')[0]
                        temp.append(second_url)

                    for el in temp:
                        if el not in scrapedEmails:
                            scrapedEmails.append(el)
                except:
                    pass

            # clean email addresses

            scrapedEmails = [item for item in scrapedEmails if '.' in (item)]
            scrapedEmails = [item for item in scrapedEmails if not any(word in item for word in remove_list)]
            scrapedEmails = [item for item in scrapedEmails if "'" not in (item)]
            scrapedEmails = [item for item in scrapedEmails if '"' not in (item)]

            # verify email has a domain name at the end
            for el in scrapedEmails:
                if '.' not in el[-6:]:
                    print('This email did not have a domain so it will be erased: ', el)
                    scrapedEmails.remove(el)
            print(str(len(scrapedEmails)) + ' EMAILS SCRAPED AFTER CLEANING \n', scrapedEmails)




            #######END OF THE BS CHECK FOR EMAILS BY REGEX #################
        except:
            pass


    try:
        for el in dicti_pretty_links:
            #######START OF THE SELENIUM CHECK FOR "CONTACT" PAGES #################
            # browser = webdriver.Firefox()  #This converts page into Selenium object
            chromedriver = 'C:\\chromedriver\\chromedriver.exe'
            browser = webdriver.Chrome(chromedriver)

            page = browser.get(el)
            time.sleep(random.uniform(0.5, 1.5))
            try:  # Tries to open "contact" link
                contact_link = browser.find_element_by_partial_link_text('ontact')
                if contact_link:
                    contact_link.click()
            except:
                pass  # Silently ignores exception
            html = browser.page_source  # Loads up the page for Regex search
            soup = BeautifulSoup(html, 'lxml')
            time.sleep(random.uniform(0.5, 1.5))
            emailRegex = re.compile(r'([a-zA-Z0-9_.+]+@[a-zA-Z0-9_.+.+]+)', re.VERBOSE)
            mo = emailRegex.findall(html)
            print('THIS BELOW IS SEL_emails_MO for', el)
            print(mo, 'EMAILS COMING FROM: ', el)
            if not mo:
                print('no emails found in ', el)
                emails_not_found.append(el)
            for el in mo:
                if el not in scrapedEmails:  # Checks if emails is/adds to ddbb
                    scrapedEmails.append(el)
            browser.close()
            #######END OF THE SELENIUM CHECK FOR "CONTACT" PAGES #################

            # print('EMAILS SCRAPED SO FAR: \n', scrapedEmails)

            # clean email addresses

            scrapedEmails = [item for item in scrapedEmails if '.' in (item)]
            scrapedEmails = [item for item in scrapedEmails if not any(word in item for word in remove_list)]
            scrapedEmails = [item for item in scrapedEmails if "'" not in (item)]
            scrapedEmails = [item for item in scrapedEmails if '"' not in (item)]

            # verify email has a domain name at the end
            for el in scrapedEmails:
                if '.' not in el[-6:]:
                    print('This email did not have a domain so it will be erased: ', el)
                    scrapedEmails.remove(el)
            print(str(len(scrapedEmails)) + ' EMAILS SCRAPED AFTER CLEANING \n', scrapedEmails)

        time.sleep(random.uniform(0.5, 1.5))  # INSERTS HUMAN-LIKE RANDOM DELAY
    except:
        print(scrapedEmails)
        pass


def google_nextpage_for_emails():                #Googles and gets the first few links
    global scrapedEmails
    global emails_not_found

    print(60*'-')
    print('STARTING FUNCTION NEXTPAGE FOR EMAILS')
    print('ScrapedEmails looks liks this right now: ', scrapedEmails)
    counter = 10
    for i in range(0,(number_of_search_pages)):
        #This searches for certain keywords in Google and parses results with BS
        for el in search_terms:
            webpage = 'https://www.google.com/search?q='+str(el)+str(added_terms)+'&start='+str(counter)
            print('\n Searching for the terms...', el,added_terms, 'on', webpage)
            headers = {'User-agent':'Mozilla/5.0'}
            res = requests.get(webpage, headers=headers)
            #res.raise_for_status()

            statusCode = res.status_code
            if statusCode == 200:
                soup = bs4.BeautifulSoup(res.text,'lxml')
                serp_res_rawlink = soup.select('.r a')

                dicti = []                  #This gets the href links
                for link in serp_res_rawlink:
                    url = link.get('href')
                    if 'pdf' not in url:
                        dicti.append(url)

                dicti_url = []              #This cleans the "url?q=" from link
                for el in dicti:
                    if '/url?q=' in el:
                        result = (el.strip('/url?q='))
                        dicti_url.append(result)
                #print(dicti_url)

                global dicti_pretty_links
                dicti_pretty_links = []     #This cleans the gibberish at end of url
                for el in dicti_url[0:(number_of_sites)]:
                    pretty_url = el.partition('&')[0]
                    dicti_pretty_links.append(pretty_url)
                print(dicti_pretty_links)


                for el in dicti_pretty_links:
                #######START OF THE BS CHECK FOR EMAILS BY REGEX #################
                    #This opens page in BS for parsing emails
                    webpage = (el)
                    headers = {'User-agent':'Mozilla/5.0'}
                    res = requests.get(webpage, headers=headers)

                    statusCode = res.status_code
                    if statusCode == 200:
                        soup = bs4.BeautifulSoup(res.text,'lxml')
                        #if "</form>" in soup:

                        #This is the first way to search for an email in soup, "MO"
                        emailRegex = re.compile(r'([a-zA-Z0-9_.+]+@[a-zA-Z0-9_.+.+]+)', re.VERBOSE)
                        mo = emailRegex.findall(res.text)
                        print('THIS BELOW IS MO')
                        print(mo, el, 'THIS IS THE WEBSITE IT IS COMING FROM')
                        for el in mo:
                            if el not in scrapedEmails:
                                scrapedEmails.append(el)

                        #This is the second way to search for an email in soup, "MAILTOS":
                        # mailtos = soup.select('a[href^=mailto]')
                        # print('THIS BELOW IS MAILTOS')
                        # print(mailtos, el, 'THIS IS THE WEBSITE IT IS COMING FROM')
                        #
                        # dicti_cleaner = []
                        # target = re.compile(r'mailto')
                        # for el in mailtos:
                        #     mo = target.search(str(el))
                        #     dicti_cleaner.append(el)
                        #
                        # temp = []
                        # for el in dicti_cleaner:
                        #     pretty_url = str(el).partition(':')[2]
                        #     second_url = str(pretty_url).partition('"')[0]
                        #     temp.append(second_url)
                        #
                        # for el in temp:
                        #     if el not in scrapedEmails:
                        #         scrapedEmails.append(el)
                #     #######END OF THE BS CHECK FOR EMAILS BY REGEX #################

                try:
                    for el in dicti_pretty_links:
                    #######START OF THE SELENIUM CHECK FOR "CONTACT" PAGES #################
                        #browser = webdriver.Firefox()  #This converts page into Selenium object
                        chromedriver = 'C:\\chromedriver\\chromedriver.exe'
                        browser = webdriver.Chrome(chromedriver)

                        page = browser.get(el)
                        time.sleep(random.uniform(1,2))
                        try:                                #Tries to open "contact" link
                            contact_link = browser.find_element_by_partial_link_text('ontact')
                            if contact_link:
                                contact_link.click()
                        except Exception as e:
                            print (e)
                            #continue
                            pass    #Silently ignores exception


                        html = browser.page_source          #Loads up the page for Regex search
                        soup = BeautifulSoup(html,'lxml')
                        time.sleep(random.uniform(1,2))
                        emailRegex = re.compile(r'([a-zA-Z0-9_.+]+@[a-zA-Z0-9_.+.+]+)', re.VERBOSE)
                        mo = emailRegex.findall(html)
                        print('THIS BELOW IS SEL_emails_MO for',el)
                        print(mo, el, 'THIS IS THE WEBSITE IT IS COMING FROM')
                        if not mo:
                            print('no emails found in ',el)
                            emails_not_found.append(el)
                        for el in mo:
                            if el not in scrapedEmails:     #Checks if emails is/adds to ddbb
                                scrapedEmails.append(el)
                        browser.close()
                        #######END OF THE SELENIUM CHECK FOR "CONTACT" PAGES #################
                except Exception as e:
                    print(e)
                    continue

        counter += 10
        time.sleep(random.uniform(1,2.5))    #INSERTS HUMAN-LIKE RANDOM DELAY
        print('EMAILS SCRAPED SO FAR \n', scrapedEmails)

        # clean email addresses
        remove_list = ['.gif', '.png', 'example.com']
        scrapedEmails = [item for item in scrapedEmails if '.' in (item)]
        scrapedEmails = [item for item in scrapedEmails if not any(word in item for word in remove_list)]

        #verify email has a domain name at the end
        for el in scrapedEmails:
            if '.' not in el[-6:]:
                print('This email did not have a domain so it will be erased: ', el)
                scrapedEmails.remove(el)
        print(str(len(scrapedEmails)) + ' EMAILS SCRAPED AFTER CLEANING \n', scrapedEmails)



        report()

def open_emails_lost():
   for el in emails_not_found:
        print(el)
        #browser = webdriver.Firefox()  #This converts page into Selenium object
        chromedriver = 'C:\\chromedriver\\chromedriver.exe'
        browser = webdriver.Chrome(chromedriver)

        try:
            browser.get(el)
            time.sleep(random.uniform(1,2))
        except:
            pass

def report():
    global emails_not_found
    print(100*'-')
    print('The following search terms have been searched: ')
    print(search_terms)
    print(len(search_terms),'terms have been searched, for a total of',number_of_sites,'from each Google website result page')
    print(len(search_terms)*number_of_sites,'pages have been scraped for emails.')
    print('A total of ',len(scrapedEmails),'emails have been found')
    print('A total of ',len(emails_not_found),'pages parsed did not contain an email')
    print('These are those pages: ', emails_not_found)
    print('These are the emails found:')
    print(str(scrapedEmails)[1:-1])
    print(100*'-')
    #testFile = open('test_google_tabs.txt', 'a')
    #testFile = open('test_google_tabs.txt', 'w')
    #filename = 'scrum_bri_lon'
    filename = (str(search_terms[0])+str('_')+str(added_terms))
    testFile = open(filename + '.txt', 'w')
    testFile.write('SEARCH: ')
    testFile.write(str(search_terms).upper())
    testFile.write(str(added_terms).upper())
    testFile.write('\n')
    testFile.write(str(len(search_terms)))
    testFile.write(' Google result parsed')
    testFile.write('\n')
    testFile.write(str(len(scrapedEmails)))
    testFile.write(' emails found')
    testFile.write('\n')
    testFile.write(60*'*')
    testFile.write('\n')
    testFile.write(str(scrapedEmails)[1:-1])  #last part deletes the square brakets
    testFile.write('\n')
    testFile.write('\n')
    testFile.write(str('And these below are the pages were emails were not found_____________'))
    testFile.write('\n')
    testFile.write(str(emails_not_found)[1:-1])
    testFile.close()
    #print('The information has been successfully written to "test_google_tabs.txt"')
    print('The information has been successfully written to', filename)
    print(60*'-')
    print('This is a list of the websites where email count not be found')
    for el in emails_not_found:
        print(el)
    print(60 * '-')




#program instructions #######################

google_this_for_emails()

google_nextpage_for_emails()

report()


open = input('Press any key to open the webpages that did not contain email addresses, or type "quit" to end program')

if open == 'quit':
    pass
else:
    open_emails_lost()


#####################################################################################
#TRYING TO OPEN SEARCH RESULTS WITH SELENIUM
# import requests, webbrowser, bs4, re
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import pyperclip,time,random

# search_terms = 'Alexander Hughes'
# # added_words = 'email contact contacto contactar'
# url = 'http://google.com/search?q=email+contactar+contacto+' + str(search_terms)#+ str(added_words)


# # res = requests.get(url)
# # res.raise_for_status()
# # soup = bs4.BeautifulSoup(res.text,'lxml')
# linkElems = soup.find_all('.r a')

# driver = webdriver.Firefox()
# page = driver.get(url)
# driver.implicitly_wait(1)
# time.sleep(random.uniform(0.5,1))
# global linkElems1
# linkElems1 = driver.find_elements_by_class_name('r')
# print('linkElelems1', linkElems1)
# # (linkElems1)[0].click()
# # (linkElems1)[1].click()


# numOpen = min(3, len(get_results()))
# for i in range(numOpen):
#     webbrowser.open('http://google.com' + str(i))
    # driver = webdriver.Firefox()
    # driver.get(i)



##################################################################
#THIS WORKED TO GO TO A PAGE AND GET EMAILS
#temperase
# url = 'http://www.alexanderhughes.es/contacto.html'
# driver = webdriver.Firefox()
# page = driver.get(url)
#
# global elem
# elem = driver.page_source
#
# global emailsList
# emailsList = []
#
# def get_emails_from_page():
#     assert elem
      #if 'contactar' or 'contacto' in elem select link and click
#     if '@' in elem:
#         print('Email found on this page')
#         emailRegex = re.compile(r'[a-zA-Z0-9_.+]+@[a-zA-Z0-9_.+]+', re.VERBOSE)
#         global mo
#         mo = emailRegex.findall(elem)
#         print(mo)
#         outfile = open("wiki_test.txt","wb")
#         for el in mo:
#             if el not in emailsList:
#                 addEmail = emailsList.append(el)
#                 outfile.write(bytes(el,'UTF-8'))
#         print('Success writing to Notepad file')
#         print(emailsList)
#
# get_emails_from_page()

# THIS WORKS
# driver = webdriver.Firefox()
# page = driver.get(url)
# linkElems1 = driver.find_element_by_class_name('r')
# (linkElems1).click()


#     #open search results in tabs
# numOpen = min(1, len(linkElems))
# for i in range(numOpen):
#     webbrowser.open('http://google.com' + linkElems[i].get('href'))
#     webbrowser.
#     emailRegex = re.compile(r'([a-zA-Z0-9_.+]+@[a-zA-Z0-9_.+])', re.VERBOSE)
#     emailRegex.findall(page.page_source)
#     print(mo.group)
    #go to tab 1, parse for emails, close

    #go to tab 2, parse for emails

    #for each open tab, parse for emails, then close tabs

#sstart search again with new term


# counter = soup.find(id="resultStats").text
# print(counter)
# print('I am %s closer to my goal' % (counter))


#################################################################################
#THIS MAKES A SEARCH AND OPENS THE FIRST X RESULTS IN NEW TABS ##################
# import requests, webbrowser, bs4
#
# keywords = input('What words to search Google for?: \n')
# print('Googling...')
#
# res = requests.get('http://google.com/search?q=' + keywords)
# res.raise_for_status()
#
# soup = bs4.BeautifulSoup(res.text,'lxml')
# linkElems = soup.select('.r a')
# counter = soup.find(id="resultStats").text
#
# numOpen = min(5, len(linkElems))
# for i in range(numOpen):
#     webbrowser.open('http://google.com' + linkElems[i].get('href'))
#
# print(counter)
# print('I am %s closer to my goal' % (counter))

#####################################################################
# SIMPLE WEB SEARCH SCRIPT
# import webbrowser, sys, pyperclip
# textToSearch = 'Titanic'
# webbrowser.open('https://www.google.co.uk/?gfe_rd=cr&ei=GuENVvq5Is2q8wed_L0g&gws_rd=ssl#q='+textToSearch)

#####################################################################
#GET ALL LINKS IN A GOOGLE SEARCH RESULTS PAGE
# import requests, re
# from bs4 import BeautifulSoup
# headers = {'User-agent':'Mozilla/5.0'}
# page = requests.get('https://www.google.com/search?q=Tesla',headers=headers)
# soup = BeautifulSoup(page.content,'lxml')
# links = soup.findAll('a')
# for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
#     print(re.split(":(?=http)",link["href"].replace("/url?q=","")))


####################################################################################
#THIS WILL GOOGLE AND CHECK SEVERAL PAGES OF RESULTS, LOOKING FOR A LINK ###########
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# q = input("Enter the search query")
# q = q.replace(' ', '')
# browser = webdriver.Firefox()
# body = browser.find_element_by_tag_name("body")
# body.send_keys(Keys.CONTROL + 't')
# counter = 0
# for i in range(0,20):
#     browser.get("https://www.google.com/search?q=" + q + "&start=" + str(counter))
#     body = browser.find_element_by_tag_name("body")
#     if "thetaranights" in body.text:
#         browser.find_element_by_xpath('//a[starts-with(@href,"http://www.thetaranights.com")]').click()
#         break
#     counter += 10

##############################################################################
#GOOGLE SEARCH SEPARATED BY FUNCTIONS. ADDS EMAILS RESULTS TO EXCEL SHEET
#@copyright JavierMarti.co.uk
#THIS SEARCHES FOR ANY NUMBER OF SEARCH TERMS PLUS OTHER WORDS
#AND SCRAPES FOR EMAILS THE FIRST X NUMBERS OF RESULTS SEVERAL RESULT PAGES
#THEN DOUBLE CHECKS WITH SELENIUM BY OPENING CONTACT LINKS AND SCRAPING WITH REGEX
# import os
# import openpyxl
# import requests, re, bs4
# from selenium import webdriver
# from bs4 import BeautifulSoup
# import time,random
#
# def google_this_for_emails():                #Googles and gets the first few links
#
#     global scrapedEmails
#     scrapedEmails = []
#     global emails_not_found
#     emails_not_found = []
#
#     #This searches for certain keywords in Google and parses results with BS
#     #for el in search_terms:
#     webpage = 'http://google.com/search?q=' + str(search_terms + str(added_terms))
#     print('\nSearching for the terms...', search_terms, added_terms)
#
#     list_headers = ['Mozilla/5.0','Opera/9.80','Mozilla/4.0']
#     #list_complete_headers = ['Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)','Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16','Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36']
#     #proxies = {'http': 'http://107.151.136.195:80','https': 'http://189.218.255.151:16973',}
#     #res = requests.get(webpage, headers=random.choice(list_headers))
#
#     #headers = {'User-agent':'Mozilla/5.0'}#THIS LINE SHOULD BE ENABLED IF NOT WORKING WITH PROXIES
#     headers = {'User-agent':random.choice(list_headers)}
#     res = requests.get(webpage, headers=headers) #THIS LINE SHOULD BE ENABLED IF NOT WORKING WITH PROXIES
#     ##res.raise_for_status()
#
#     global emails_found_list
#     emails_found_list = []      #This adds emails to be inserted in cell
#
#     statusCode = res.status_code
#     if not statusCode == 200:
#         print('Problem connection to server, statusCode is: ',statusCode)
#     if statusCode == 200:
#         soup = bs4.BeautifulSoup(res.text,'lxml')
#         serp_res_rawlink = soup.select('.r a')
#         #print('END of Status code check )))))))))))))))))))))')
#         dicti = []                  #This gets the href links
#         for link in serp_res_rawlink:
#             url = link.get('href')
#             if 'pdf' not in url:
#                 dicti.append(url)
#
#         dicti_url = []              #This cleans the "url?q=" from link
#         for el in dicti:
#             if '/url?q=' in el:
#                 result = (el.strip('/url?q='))
#                 dicti_url.append(result)
#         #print(dicti_url)
#
#         global dicti_pretty_links
#         dicti_pretty_links = []     #This cleans the gibberish at end of url
#         for el in dicti_url[0:(number_of_sites)]:
#             pretty_url = el.partition('&')[0]
#             dicti_pretty_links.append(pretty_url)
#         print(dicti_pretty_links)
#
#
#         # for el in dicti_pretty_links:
#         # #######START OF THE BS CHECK FOR EMAILS BY REGEX #################
#         #     #This opens page in BS for parsing emails
#         #     webpage = (el)
#         #     headers = {'User-agent':'Mozilla/5.0'}
#         #     res = requests.get(webpage, headers=headers)
#         #
#         #     statusCode = res.status_code
#         #     if statusCode == 200:
#         #         soup = bs4.BeautifulSoup(res.text,'lxml')
#         #         #if "</form>" in soup:
#         #
#         #         #print('Start of Regex function )))))))))))))))))))))')
#         #
#         #         #This is the first way to search for an email in soup, "MO"
#         #         emailRegex = re.compile(r'([a-zA-Z0-9_.+]+@[a-zA-Z0-9_.+.+]+)', re.VERBOSE)
#         #         mo = emailRegex.findall(res.text)
#         #         print('THIS BELOW IS MO')
#         #         print(mo,'EMAILS COMING FROM: ',el)
#         #         for el in mo:
#         #             if el not in emails_found_list:
#         #                 emails_found_list.append(el)
#         #
#         #         print('END of Regex function ')
#
#                 #This is the second way to search for an email in soup, "MAILTOS":
#                 # mailtos = soup.select('a[href^=mailto]')
#                 # print('THIS BELOW IS MAILTOS')
#                 # print(mailtos, el, 'THIS IS THE WEBSITE IT IS COMING FROM')
#                 #
#                 # dicti_cleaner = []
#                 # target = re.compile(r'mailto')
#                 # for el in mailtos:
#                 #     mo = target.search(str(el))
#                 #     dicti_cleaner.append(el)
#                 #
#                 # temp = []
#                 # for el in dicti_cleaner:
#                 #     pretty_url = str(el).partition(':')[2]
#                 #     second_url = str(pretty_url).partition('"')[0]
#                 #     temp.append(second_url)
#                 #
#                 # for el in temp:
#                 #     if el not in emails_found_list:
#                 #         emails_found_list.append(el)
#
#         #     #######END OF THE BS CHECK FOR EMAILS BY REGEX #################
#
#         for el in dicti_pretty_links:
#         #######START OF THE SELENIUM CHECK FOR "CONTACT" PAGES #################
#             browser = webdriver.Firefox()  #This converts page into Selenium object
#             page = browser.get(el)
#             time.sleep(random.uniform(0.5,1.5))
#             try:                                #Tries to open "contact" link
#                 contact_link = browser.find_element_by_partial_link_text('ontact')
#                 if contact_link:
#                     contact_link.click()
#             except:
#                 pass    #Silently ignores exception
#             html = browser.page_source          #Loads up the page for Regex search
#             soup = BeautifulSoup(html,'lxml')
#             time.sleep(random.uniform(0.5,1.5))
#             emailRegex = re.compile(r'([a-zA-Z0-9_.+]+@[a-zA-Z0-9_.+.+]+)', re.VERBOSE)
#             mo = emailRegex.findall(html)
#             print('THIS BELOW IS SEL_emails_MO for',el)
#             print(mo,'EMAILS COMING FROM: ',el)
#             if not mo:
#                 print('no emails found in ',el)
#                 emails_not_found.append(el)
#             for el in mo:
#                 if el not in emails_found_list:     #Checks if emails is/adds to ddbb
#                     emails_found_list.append(el)
#             browser.close()
#             #######END OF THE SELENIUM CHECK FOR "CONTACT" PAGES #################
#
#
#         #HERE YOU MUST WRITE emails_found_list TO THE XLS CELL
#         first_row = "A" + str(i)
#         ws[first_row] = str(search_terms)
#         second_row = "B" + str(i)
#         ws[second_row] = str(emails_found_list)
#         wb.save('psychotherapists_central_LN.xlsx')
#         print(str(i)+'/3866 successfully saved')
#         time.sleep(random.uniform(2,4))    #INSERTS HUMAN-LIKE RANDOM DELAY
#         #IF NEXT PAGE WILL BE USED, SCRAPED_EMAILS MUST BE REPLACED WITH emails_found_list
#
#
# def google_nextpage_for_emails():                #Googles and gets the first few links
#     print(60*'-')
#     print('STARTING FUNCTION NEXTPAGE FOR EMAILS')
#     counter = 10
#     for i in range(0,(number_of_search_pages)):
#         #This searches for certain keywords in Google and parses results with BS
#         for el in search_terms:
#             webpage = 'https://www.google.com/search?q='+str(el)+str(added_terms)+'&start='+str(counter)
#             print('\n Searching for the terms...', el,added_terms, 'on', webpage)
#             headers = {'User-agent':'Mozilla/5.0'}
#             res = requests.get(webpage, headers=headers)
#             #res.raise_for_status()
#
#             statusCode = res.status_code
#             if statusCode == 200:
#                 soup = bs4.BeautifulSoup(res.text,'lxml')
#                 serp_res_rawlink = soup.select('.r a')
#
#                 dicti = []                  #This gets the href links
#                 for link in serp_res_rawlink:
#                     url = link.get('href')
#                     if 'pdf' not in url:
#                         dicti.append(url)
#
#                 dicti_url = []              #This cleans the "url?q=" from link
#                 for el in dicti:
#                     if '/url?q=' in el:
#                         result = (el.strip('/url?q='))
#                         dicti_url.append(result)
#                 #print(dicti_url)
#
#                 global dicti_pretty_links
#                 dicti_pretty_links = []     #This cleans the gibberish at end of url
#                 for el in dicti_url[0:(number_of_sites)]:
#                     pretty_url = el.partition('&')[0]
#                     dicti_pretty_links.append(pretty_url)
#                 print(dicti_pretty_links)
#
#
#                 for el in dicti_pretty_links:
#                 #######START OF THE BS CHECK FOR EMAILS BY REGEX #################
#                     #This opens page in BS for parsing emails
#                     webpage = (el)
#                     headers = {'User-agent':'Mozilla/5.0'}
#                     res = requests.get(webpage, headers=headers)
#
#                     statusCode = res.status_code
#                     if statusCode == 200:
#                         soup = bs4.BeautifulSoup(res.text,'lxml')
#                         #if "</form>" in soup:
#
#                         #This is the first way to search for an email in soup, "MO"
#                         emailRegex = re.compile(r'([a-zA-Z0-9_.+]+@[a-zA-Z0-9_.+.+]+)', re.VERBOSE)
#                         mo = emailRegex.findall(res.text)
#                         print('THIS BELOW IS MO')
#                         print(mo, el, 'THIS IS THE WEBSITE IT IS COMING FROM')
#                         for el in mo:
#                             if el not in scrapedEmails:
#                                 scrapedEmails.append(el)
#
#                         #This is the second way to search for an email in soup, "MAILTOS":
#                         # mailtos = soup.select('a[href^=mailto]')
#                         # print('THIS BELOW IS MAILTOS')
#                         # print(mailtos, el, 'THIS IS THE WEBSITE IT IS COMING FROM')
#                         #
#                         # dicti_cleaner = []
#                         # target = re.compile(r'mailto')
#                         # for el in mailtos:
#                         #     mo = target.search(str(el))
#                         #     dicti_cleaner.append(el)
#                         #
#                         # temp = []
#                         # for el in dicti_cleaner:
#                         #     pretty_url = str(el).partition(':')[2]
#                         #     second_url = str(pretty_url).partition('"')[0]
#                         #     temp.append(second_url)
#                         #
#                         # for el in temp:
#                         #     if el not in scrapedEmails:
#                         #         scrapedEmails.append(el)
#                 #     #######END OF THE BS CHECK FOR EMAILS BY REGEX #################
#
#                 try:
#                     for el in dicti_pretty_links:
#                     #######START OF THE SELENIUM CHECK FOR "CONTACT" PAGES #################
#                         browser = webdriver.Firefox()  #This converts page into Selenium object
#                         page = browser.get(el)
#                         time.sleep(random.uniform(2,4))
#                         try:                                #Tries to open "contact" link
#                             contact_link = browser.find_element_by_partial_link_text('ontact')
#                             if contact_link:
#                                 contact_link.click()
#                         except Exception as e:
#                             print (e)
#                             continue
#                             #pass    #Silently ignores exception
#                         html = browser.page_source          #Loads up the page for Regex search
#                         soup = BeautifulSoup(html,'lxml')
#                         time.sleep(random.uniform(5,10))
#                         emailRegex = re.compile(r'([a-zA-Z0-9_.+]+@[a-zA-Z0-9_.+.+]+)', re.VERBOSE)
#                         mo = emailRegex.findall(html)
#                         print('THIS BELOW IS SEL_emails_MO for',el)
#                         print(mo, el, 'THIS IS THE WEBSITE IT IS COMING FROM')
#                         if not mo:
#                             print('no emails found in ',el)
#                             emails_not_found.append(el)
#                         for el in mo:
#                             if el not in scrapedEmails:     #Checks if emails is/adds to ddbb
#                                 scrapedEmails.append(el)
#                         browser.close()
#                         #######END OF THE SELENIUM CHECK FOR "CONTACT" PAGES #################
#                 except Exception as e:
#                     print(e)
#                     continue
#
#         counter += 10
#         time.sleep(random.uniform(2,4))    #INSERTS HUMAN-LIKE RANDOM DELAY
#         print('EMAILS SCRAPED SO FAR \n', scrapedEmails)
#         report()
#
# def open_emails_lost():
#    for el in emails_not_found:
#         print(el)
#         browser = webdriver.Firefox()  #This converts page into Selenium object
#         try:
#             browser.get(el)
#             time.sleep(random.uniform(1,2))
#         except:
#             pass
#
# # def report():
# #     print(100*'-')
# #     print(len(search_terms),'terms have been searched, for a total of',number_of_sites,'from each Google website result page')
# #     print(len(search_terms)*number_of_sites,'pages have been scraped for emails.')
# #     print('A total of ',len(scrapedEmails),'emails have been found')
# #     print('A total of ',len(emails_not_found),'pages parsed did not contain an email')
# #     print('These are those pages: ', emails_not_found)
# #     print('These are the emails found:')
# #     print(str(scrapedEmails)[1:-1])
# #     print(100*'-')
# #     #testFile = open('test_google_tabs.txt', 'a')
# #     filename = (str(search_terms)+str('_')+str(added_terms))
# #     testFile = open(filename + '.txt', 'w')
# #     #testFile = open('test_google_tabs.txt', 'w')
# #     testFile.write('SEARCH: ')
# #     testFile.write(str(search_terms).upper())
# #     testFile.write(str(added_terms).upper())
# #     testFile.write('\n')
# #     testFile.write(str(len(search_terms)))
# #     testFile.write(' Google result parsed')
# #     testFile.write('\n')
# #     testFile.write(str(len(scrapedEmails)))
# #     testFile.write(' emails found')
# #     testFile.write('\n')
# #     testFile.write(60*'*')
# #     testFile.write('\n')
# #     testFile.write(str(scrapedEmails)[1:-1])  #last part deletes the square brakets
# #     testFile.write('\n')
# #     testFile.write('\n')
# #     testFile.write(str('And these below are the pages were emails were not found_____________'))
# #     testFile.write('\n')
# #     testFile.write(str(emails_not_found)[1:-1])
# #     testFile.close()
# #     #print('The information has been successfully written to "test_google_tabs.txt"')
# #     print('The information has been successfully written to', filename)
# #     print(60*'-')
#
#
# os.chdir('C:\\Users\\SK\\PycharmProjects\\untitled')
# workbook = openpyxl.load_workbook('psychotherapists_central_TEST.xlsx')
# wb = openpyxl.Workbook()
# ws = wb.active
#
# type(workbook)
# sheet = workbook.get_sheet_by_name('Sheet')
#
# for i in range(129,3866):
#     #print(sheet.cell(row=i, column=3).value)
#     number_of_sites = 1   #NUMBER OF SITES (SEARCH RESULTS) TO PARSE FOR EMAILS
#     number_of_search_pages = 1
#     global search_terms
#     if not (sheet.cell(row=i, column=3).value) == None:
#         search_terms = (sheet.cell(row=i, column=3).value)
#         global added_terms
#         added_terms = ' contact email @'
#         #print('(((((((((((((((((')
#         print(str(search_terms) + 'SEARCH TERM BEFORE FUNCTION')
#         google_this_for_emails()
#         time.sleep(random.uniform(30,40))
#     else:
#         continue
#     #google_nextpage_for_emails()
#     #report()###########################################################################
#