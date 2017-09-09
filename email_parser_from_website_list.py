#--- EMAIL PARSER FROM WEBSITE LIST ---
# @copyright JavierMarti.co.uk
#THIS PARSES A LIST OF WEBSITES FOR EMAILS IN TWO DIFFERENT WAYS (BS4, MAILTOS)
#THEN DOUBLE CHECKS WITH SELENIUM BY OPENING CONTACT LINKS AND SCRAPING WITH REGEX
#THE LIST OF WEBSITES TO BE PARSES IS INSERTED INTO "dicti_pretty_links" in the "search for emails" function


import requests,re,bs4
from selenium import webdriver
from bs4 import BeautifulSoup
import time,random

global remove_list
remove_list = ['.gif', '.png', 'example.com', 'abuse@', 'yourdomain', 'jpg','jpeg','database@','fbl@','ftp@','noc@','post@','postbox@','postmaster@','privacy@','remove@','root@','spam@','subscribe@','uucp@','webmaster@','welcome@','www@','%20','user']

def search_for_emails():                #Googles and gets the first few links

    global scrapedEmails
    scrapedEmails = []
    global emails_not_found
    emails_not_found = []
    global dicti_pretty_links

    # INSERT WEBSITES TO PARSE FOR EMAILS HERE AS A LIST, NOT AS A DICTIONARY ~~~~~~~~~~~~~~~~~~~~~~~~~

    dicti_pretty_links = ['http://www.mckinsey.com', 'http://www.bcg.com/', 'http://www.bain.com/', 'http://strategyand.pwc.com', 'http://www.monitor.com', 'http://www.deloitte.com/view/en_US/us/Services/consulting', 'http://www.oliverwyman.com', 'http://www.rolandberger.com', 'http://www.lek.com', 'http://www.atkearney.com', 'http://www.zsassociates.com', 'http://www.accenture.com', 'http://www.capgemini.com', 'http://www.pwc.com/gx/en/consulting-services', 'http://parthenon.ey.com/PO/en/Home', 'http://www.ibm.com/consulting', 'http://www.ey.com/US/en/Services/Advisory', 'http://www.towerswatson.com', 'http://www.kpmg.com/Global/en/WhatWeDo/Advisory/management-consulting', 'http://www.mercer.com', 'http://www.aon.com/human-capital-consulting', 'http://www.huronconsultinggroup.com', 'http://www.alvarezandmarsal.com', 'http://www.haygroup.com', 'http://www.altran.com']

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    print('Number of sites to be parsed (in dicti_pretty_links): ', len(dicti_pretty_links))

    for el in dicti_pretty_links:
    #######START OF THE BS CHECK FOR EMAILS BY REGEX #################
        #This opens page in BS for parsing emails

        try:
            webpage = (el)
            headers = {'User-agent':'Mozilla/5.0'}
            res = requests.get(webpage, headers=headers)

        except:
            pass

        try:
            statusCode = res.status_code
            if statusCode == 200:
                soup = bs4.BeautifulSoup(res.text,'lxml')
                #if "</form>" in soup:
                try:

                    #This is the first way to search for an email in soup, "MO"
                    emailRegex = re.compile(r'([a-zA-Z0-9_.+]+@[a-zA-Z0-9_.+.+]+)', re.VERBOSE)
                    mo = emailRegex.findall(res.text)
                    print('THIS BELOW IS MO')
                    print(mo,'EMAILS COMING FROM: ',el)
                    for el in mo:
                        if el not in scrapedEmails:
                            scrapedEmails.append(el)
                except:
                    pass

                try:
                    #This is the second way to search for an email in soup, "MAILTOS":
                    mailtos = soup.select('a[href^=mailto]')
                    print('THIS BELOW IS MAILTOS')
                    print(mailtos, el, 'THIS IS THE WEBSITE IT IS COMING FROM')

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
            #browser = webdriver.Firefox()  #This converts page into Selenium object
            chromedriver = 'C:\\chromedriver\\chromedriver.exe'
            browser = webdriver.Chrome(chromedriver)

            page = browser.get(el)
            time.sleep(random.uniform(0.5,1.5))
            try:                                #Tries to open "contact" link
                contact_link = browser.find_element_by_partial_link_text('ontact')
                if contact_link:
                    contact_link.click()
            except:
                pass    #Silently ignores exception
            html = browser.page_source          #Loads up the page for Regex search
            soup = BeautifulSoup(html,'lxml')
            time.sleep(random.uniform(0.5,1.5))
            emailRegex = re.compile(r'([a-zA-Z0-9_.+]+@[a-zA-Z0-9_.+.+]+)', re.VERBOSE)
            mo = emailRegex.findall(html)
            print('THIS BELOW IS SEL_emails_MO for',el)
            print(mo,'EMAILS COMING FROM: ',el)
            if not mo:
                print('no emails found in ',el)
                emails_not_found.append(el)
            for el in mo:
                if el not in scrapedEmails:     #Checks if emails is/adds to ddbb
                    scrapedEmails.append(el)
            browser.close()
            #######END OF THE SELENIUM CHECK FOR "CONTACT" PAGES #################

            #print('EMAILS SCRAPED SO FAR: \n', scrapedEmails)

            #clean email addresses

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




        time.sleep(random.uniform(0.5,1.5))    #INSERTS HUMAN-LIKE RANDOM DELAY
    except:
        pass

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
    #print(dicti_pretty_links)
    print(len(dicti_pretty_links),' websites have been searched')
    print('A total of ',len(scrapedEmails),'emails have been found')
    print('A total of ',len(emails_not_found),'pages parsed did not contain an email')
    print('These are those pages: ', emails_not_found)
    print('These are the emails found:')
    print(str(scrapedEmails)[1:-1])
    print(100*'-')
    #testFile = open('test_google_tabs.txt', 'a')
    #testFile = open('test_google_tabs.txt', 'w')
    #filename = 'scrum_bri_lon'
    filename = ('website_parse_results')
    testFile = open(filename + '.txt', 'w')
    testFile.write('SEARCH: ')
    testFile.write(str(dicti_pretty_links).upper())
    testFile.write('\n')
    testFile.write(str(len(dicti_pretty_links)))
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

search_for_emails()

#google_nextpage_for_emails()

report()

open = input('Press any key to open the webpages that did not contain email addresses, or type "quit" to end program')

if open == 'quit':
    pass
else:
    open_emails_lost()

