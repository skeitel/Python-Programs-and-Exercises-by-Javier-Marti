#Python program by Javier Marti
'''THIS PROGRAM EXTRACTS ITEMS FROM A WEBPAGE DIRECTORY, GOES TO NEXT PAGE AND DOES THE SAME, STORING IT ALL IN A TEXT FILE
Copyright JavierMarti.co.uk'''

import time
import random
from selenium import webdriver
from bs4 import BeautifulSoup

chromedriver = 'C:\\chromedriver\\chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
#driver.get("https://www.mobileworldcongress.com/exhibitors/")# all cies whole world
driver.get("https://www.therobotreport.com/directory/service-robots-for-governmental-and-corporate-use") #DE


def grab_items_from_webpage_directory():


    global counter
    counter = 1
    while True:

        # get source code ready to scan
        print("Doing the first sleep to wait for loading...")
        time.sleep(random.uniform(1,2))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        get_class = soup.find("div", {'class': 'three-column'}).find_all('h3')

        # get rid of cookie
        try:

            cookie_button = driver.find_element_by_id('continuebutton')
            cookie_button.click()
            time.sleep(2)
        except:
            pass

        print('This is the current content of dictionary\n', main_dictionary)
        print('Starting to grab username and link from this page')

        try:

            # grabbing elements starts
            for el in get_class:

                # find first element to be added to dictionary (usually title or main id of the item)
                company_name = el.text
                print(company_name.text)

                # find second element (in this case a link)to be added to dictionary
                company_link = el.a['href']
                print(company_link)
                print('--------------------')

                print('Verifying item not already in dictionary...')
                if company_name.text not in main_dictionary:
                    main_dictionary[company_name.text] = company_link
        except:
            pass

        #WRITING ITEMS TO NOTEPAD FILE / CHANGE DESTIONATION FILE
        try:
            #writing items to textfile dictionary
            print('About to write items of main dictionary to text file...')
            #textFile = open('main_dictionary.txt', 'w')
            textFile = open('robotic_companies.txt', 'w')
            textFile.write(str(main_dictionary))
            textFile.close()
            print('Contents of main dictionary have been written to text file...')
            print(str(counter) + ' pages have been scanned so far')

            print('At the end of scanning this page, there are ' + str(
                len(main_dictionary)) + ' items in the dictionary\n')
        except:
            pass


        print("GOING TO THE NEXT PAGE...")

        time.sleep(random.uniform(1,2))
        # clicks on "next page" button if it exists
        try:
            next_button = driver.find_element_by_link_text('>')
            if next_button:
                next_button.click()
        except:
            break

        counter += 1



def test_function():
    global counter
    counter = 1
    while True:

        # get source code ready to scan
        print("Doing the first sleep to wait for loading...")
        time.sleep(random.uniform(1, 2))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        get_class = soup.find("div", {'class': 'three-column'}).find_all('h3')
        #print(get_class)
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        print('This is the current content of dictionary\n', main_dictionary)
        print('Starting to grab username and link from this page')



        # grabbing elements starts
        for el in get_class:

            # find first element to be added to dictionary (usually title or main id of the item)
            company_name = el.text
            print(company_name)

            # find second element (in this case a link)to be added to dictionary
            company_link = el.a['href']
            print(company_link)
            print('--------------------')

            print('Verifying item not already in dictionary...')
            if company_name not in main_dictionary:
                main_dictionary[company_name] = company_link


        #WRITING ITEMS TO NOTEPAD FILE / CHANGE DESTINATION FILE
        try:
            # writing items to textfile dictionary
            print('About to write items of main dictionary to text file...')
            # textFile = open('main_dictionary.txt', 'w')
            textFile = open('robotic_companies.txt', 'w')
            textFile.write(str(main_dictionary))
            textFile.close()
            print('Contents of main dictionary have been written to text file...')
            print(str(counter) + ' pages have been scanned so far')

            print('At the end of scanning this page, there are ' + str(
                len(main_dictionary)) + ' items in the dictionary\n')
        except:
            pass

        print("GOING TO THE NEXT PAGE...")

        time.sleep(random.uniform(1, 2))
        # clicks on "next page" button if it exists
        try:
            next_button = driver.find_element_by_link_text('>')
            if next_button:
                next_button.click()
        except:
            pass

        counter += 1
        if counter == 5:
            print(main_dictionary)
        elif counter == 10:
            print(main_dictionary)



####################################################################################
#make global vars
global main_dictionary



# creating/loading dictionary that will store parsed items
main_dictionary = {}


#grab_items_from_webpage_directory()
test_function()

print('##########################################')
print('THIS IS THE DICTIONARY CONTENT \n')
print(main_dictionary)
print('There are ' + str(len(main_dictionary)) + ' items in the dictionary')

print('Closing browser...')
driver.close()

