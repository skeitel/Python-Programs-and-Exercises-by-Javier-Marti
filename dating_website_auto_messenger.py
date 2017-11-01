from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time, random, re, pickle
#Python program by Javier Marti
'''THIS PROGRAM OPENS UP A NEW CHROME INSTANCE,
LOGS INTO PLENTY OF FISH AND THEN GOES TO HISTORY PAGE
RETRIEVES ALL CONTACTED USERNAMES AND LINKS,
THEN GOES TO LASTONLINE PAGE OBTAINS ALL USERNAMES AND LINKS,
THEN COMPARES TO MAKE SURE USERS HAVE NOT BEEN CONTACTED BEFORE,
THEN SENDS A PERSONALIZED MESSAGE TO EACH USER THAT HAS NOT BEEN PREVIOUSLY CONTACTED.
note: 1) SELECT NUMBER OF PAGES TO BE SCANNED FOR "LASTONLINE" IN LASTONLINE FUNCTION
2) MAKE SURE BUTTON CLICK TO SEND MESSAGE LINE IS UNCOMMENTED, IN ORDER TO PERFORM FINAL ACTION
Copyright JavierMarti.co.uk'''

chromedriver = 'D:\\Program files\\chromedriver_win32\\chromedriver.exe'
browser = webdriver.Chrome(chromedriver)
browser.get('http://www.pof.com')


##################################################################
#FUNCTION DEFINITION STARTS ######################################
##################################################################

def check_and_log_in():
    try:
        browser.find_element_by_id("logincontrol_username")
        username = browser.find_element_by_id("logincontrol_username")
        password = browser.find_element_by_id("logincontrol_password")
        username.send_keys("username_goes_here")
        #wait between key presses
        time.sleep(random.uniform(0.6,1))
        password.send_keys("password_goes_here")
        browser.find_element_by_name("login").click()
        print("Finished logging in...")
        time.sleep(1)
        browser.get(url1)
        # browser.execute_script("window.history.go(-1)")

    except:
        pass
        print("Something went wrong OR WE'RE ALREADY LOGGED IN, as I am the EXCEPTION being triggered")
def click_sent_mssgs():
    # CHECKING THAT WE'RE STILL LOGGED IN
    try:
        login_link = browser.find_element_by_partial_link_text("iciar Sesió")
        if login_link:
            login_link.click()
            check_and_log_in()
    except:
        pass

    # STARTING FUNCTION OPERATION
    time.sleep(2)
    browser.find_element_by_partial_link_text('Msjs').click()
    print('Finished clicking sent messages...')
def grab_user_link_data_from_sent_page():
    #Function grabs data from current page, clicks on next page and does the same

    #CHECKING THAT WE'RE STILL LOGGED IN
    try:
        login_link = browser.find_element_by_partial_link_text("iciar Sesió")
        if login_link:
            login_link.click()
            check_and_log_in()
    except:
        pass

    # STARTING FUNCTION OPERATION
    print('About to start grab_user_link_data_from_sent_page function')
    print('This is the initial content of contacted_dict, before applying the grabbing function \n', contacted_dict)
    print('Starting grab_user_link_data_from_sent_page function...')
    while True:
        try:
            #get source code ready to scan
            time.sleep(random.uniform(0.5,1))
            print("Doing the first sleep...")
            soup = BeautifulSoup(browser.page_source, 'lxml')

            print('This is the current content of people_to_contact\n', people_to_contact)
            print('Starting to grab username and link from this page')

            #grabbing username and link starts
            for link in soup.find_all("span", {'class': 'blue-title-sm'}):
                username = link.text
                print(username)
                profile_link = 'http://www.pof.es/' + link.a[
                    'href']  # THIS IS HOW YOU GET A LINK IN bs4!! Took me 30 tries to find this out
                print(profile_link)

                print('Starting function to verify name...')

                # verifying user not already in dict
                if username not in contacted_dict:
                    # add to dict
                    contacted_dict[username] = profile_link
                    print("Username FROM SENT added to contacted_dictionary ")

            print('At the end of scanning this page, there are ' + str(len(contacted_dict)) + ' users in contacted_dict\n')
            print("Finished selecting users, GOING TO THE NEXT PAGE...")

            #clicks on "next page" button if it exists
            time.sleep(random.uniform(0.5,1))
            next_button = browser.find_element_by_partial_link_text("nte Pág")
            if next_button:
                next_button.click()
        except:
            break

    #Adds data to notepad file
    # print('STARTING TO WRITE TO FILE...')
    # file_of_contacted = open('list_pof_contacted.txt', 'r+')
    # file_of_contacted.write(str(contacted_dict))
    # file_of_contacted.close()
    # print('DATA OF CONTACTED USERS HAS BEEN WRITTEN TO list_pof_contacted.txt')
def extract_user_link_from_lastOnline_page():
    # Function grabs data from current page, clicks on next page and does the same

    # CHECKING THAT WE'RE STILL LOGGED IN
    try:
        login_link = browser.find_element_by_partial_link_text("iciar Sesió")
        if login_link:
            login_link.click()
            check_and_log_in()
    except:
        pass

    #STARTING FUNCTION OPERATION
    browser.get('http://www.pof.es/es_lastonlinemycity.aspx')
    print('Starting grab email function')

    global page_num
    ###############################################################################
    page_num = 1  # SET IN WHICH PAGE TO START TO GO TO NEXT PAGE
    ##################################################################################
    while page_num < 5:  # SET HOW MANY PAGES TO SCAN ################################
        ##################################################################################
        try:
            time.sleep(random.uniform(0.5,1))
            print("Doing the first sleep...")
            soup = BeautifulSoup(browser.page_source, 'lxml')

            # get all usernames and links
            # print(contacted_dict, 'first time printing the dict')
            for link in soup.find_all("div", {'class': 'about'}):
                print('extract_user_link_from_lastOnline_page FUNCTION IS STARTING ................')
                username = link.text.split()[0]  # this will get only the first word from the div
                # This works too:
                # for anchor in soup.select('div.about a'):
                #     print(anchor.text)
                print(username)
                profile_link = 'http://www.pof.es/' + link.a[
                    'href']  # THIS IS HOW YOU GET A LINK IN bs4!! :o Took me 30 tries to find this out
                print(profile_link)

                if 'TRANS' in username:
                    print('\n******** Transexual person identified*******\n')
                    print(username)
                    print('\n******** Transexual person identified*******\n')

                elif 'trans' in username:
                    print('\n******** Transexual person identified*******\n')
                    print(username)
                    print('\n******** Transexual person identified*******\n')

                elif 'Trans' in username:
                    print('\n******** Transexual person identified*******\n')
                    print(username)
                    print('\n******** Transexual person identified*******\n')

                else:

                    print('Starting function to verify name')

                    # verifying user not already in dict
                    if username not in contacted_dict and 'TRANS' not in username and 'trans' not in username and 'Trans' not in username:

                        # add to temporary dict to email users not in main dict
                        people_to_contact[username] = profile_link
                        print('Added this user to people to contact in this run')

                    time.sleep(1)

        except:
            print('No more pages to scan for users')
            break

        # PREVIOUS LOOP TO SCAN THE PAGE WILL BE REPEATED FROM HERE DOWN

        page_num = page_num + 1
        print('page_num is now', page_num)
        url_next_page = 'http://www.pof.es/es_lastonlinemycity.aspx?SID=ljqe0vgjzgu2k34k0qffpfls&guid=26843346&page=' + str(
            page_num) + '&count=700'
        browser.get(url_next_page)

        time.sleep(random.uniform(0.5,1))
        print("Doing the first sleep...")
        soup = BeautifulSoup(browser.page_source, 'lxml')

        # get all usernames and links
        # print(contacted_dict, 'first time printing the dict')
        for link in soup.find_all("div", {'class': 'about'}):
            print('MAIN FUNCTION IS STARTING ................')
            username = link.text.split()[0]  # this will get only the first word from the div
            # This works too:
            # for anchor in soup.select('div.about a'):
            #     print(anchor.text)
            print(username)
            profile_link = 'http://www.pof.es/' + link.a[
                'href']  # THIS IS HOW YOU GET A LINK IN bs4!! :o Took me 30 tries to find this out
            print(profile_link)

            if 'TRANS' in username:
                print('\n******** Transexual person identified*******\n')
                print(username)
                print('\n******** Transexual person identified*******\n')

            elif 'trans' in username:
                print('\n******** Transexual person identified*******\n')
                print(username)
                print('\n******** Transexual person identified*******\n')

            elif 'Trans' in username:
                print('\n******** Transexual person identified*******\n')
                print(username)
                print('\n******** Transexual person identified*******\n')

            else:

                print('Starting function to verify name')

                # verifying user not already in dict
                if username not in contacted_dict and 'TRANS' not in username and 'trans' not in username and 'Trans' not in username:
                    # add to temporary dict to email users not in main dict
                    people_to_contact[username] = profile_link
                    print('Added this user to people to contact in this run')

                time.sleep(1)

    print('\nTHIS IS THE PEOPLE TO CONTACT IN THIS CURRENT RUN: \n', people_to_contact)

    ##########################################



##################################################################
#PROGRAM CODE STARTS #############################################
##################################################################

#make global vars
global people_to_contact
global contacted_dict

# creating/loading dictionary of "sent to" usernames and links
contacted_dict = {}

#call functions that will be used
check_and_log_in()
click_sent_mssgs()

#make soup
soup = BeautifulSoup(browser.page_source, 'lxml')


#LOAD THE BACKUP TEXT FILE OF CONTACTED PEOPLE
textFile = open('C:\\Users\\nique\\PycharmProjects\\untitled\\backup_contacted_pof.txt', 'r+')
#textFile = open('backup_contacted_pof.txt', 'r+')
print(textFile.read(), 'lalala')
textFile = dict(textFile)
print('This is the content of textFile: \n')

print('..'*40)
print('Number of users in contacted_dict before loading it into the pickle: ', str(len(contacted_dict)))

#loading contacted_dict in the text file and pickling it
with open('C:\\Users\\nique\\PycharmProjects\\untitled\\list_pof_contacted.txt', 'wb') as myFile:
    pickle.dump(contacted_dict, myFile)

#loading dict FROM pickle
with open('C:\\Users\\nique\\PycharmProjects\\untitled\\list_pof_contacted.txt', 'rb') as myFile:
    contacted_dict_pickle = pickle.load(myFile)

print('This is the initial dictionary from loading the pickle: \n', contacted_dict_pickle)
print('Number of users in contacted_dict_pickle after loading pickle: ' + str(len(contacted_dict_pickle)))

#PENDING: HERE WE COULD ADD UP THE TEXT FILE WITH THE PICKLED, INTO CONTACTED_DICT
pickled_plus_textFile = {**contacted_dict_pickle, **textFile}
print('This is pickled_plus_textfile', pickled_plus_textFile)

#temporary dict that will be used to contact users in this run, identified as not previously contacted
people_to_contact = {}
print('BEFORE STARTING "EXTRACT FROM LAST ONLINE FUNCTION" - The content of "people_to_contact" dict is now: \n', people_to_contact)


#grab info from sent page
print('About to start grabbing user link data from sent page')
grab_user_link_data_from_sent_page()


###GO TO TARGET PAGE####
print('About to start grabbing user link from lastOnline_page')
extract_user_link_from_lastOnline_page()


#MERING ALL CONTACTED DATA TOGETHER: TEXT FILE, PICKLED AND CONTACTED_DICT
pickled_textFile_contacteddict = {**pickled_plus_textFile, **contacted_dict}


#remove duplicates from people_to_contact, compared to contacted ones
people_to_contact_duplicates_removed = dict(people_to_contact.items() - pickled_textFile_contacteddict.items())
print('REMOVAL OF DUPLICATES HAS TAKEN PLACE')
print('Number of users in people_to_contact: ' + str(len(people_to_contact)))
print('Number of users in people_to_contact_duplicates_removed: ' + str(len(people_to_contact_duplicates_removed)))

#go to each page of each user not contacted, check if we're still logged in and if so send mssg, record in dict and move to next
for k, v in people_to_contact_duplicates_removed.items():
    #go to v url
    #making this var global to use it in the login function
    global url1
    url1 = v
    print(url1)
    page = browser.get(url1)
    time.sleep(random.uniform(1,2))

    #check if we are still logged in by looking for login link
    try:
        login_link = browser.find_element_by_partial_link_text("iciar Sesió")
        if login_link:
            login_link.click()
            check_and_log_in()
    except:
        pass

    # tailor message with elements from user and SEND MESSAGE
    username = browser.find_element_by_id('username').text
    haircolor = browser.find_element_by_id('haircolor').text
    text_box = browser.find_element_by_id("send-message-textarea")
    #Assign random message between the three following var1, var2, var3
    var1 = '...que tal por POF, Srta. "' + str(
        username) + '"? Siempre es un poco raro hablar por aqui...pero bueno. "' + str(
        haircolor) + '" dijiste que tenias el pelo cuando escribiste esto. ¿Todavía lo tienes de ese color, o te lo has cambiado? Avísame cuando quieras quedar a tomar algo, y en cuanto podamos lo hacemos. Yo estoy por el centro de BCN, ¿y tú?'

    var2 = 'Hey. Siempre es un poco raro hablar por aqui...pero bueno. que tal por POF, Srta. "' + str(
        username) + '"? Dicen que este sitio web es bueno, pero no se... "' + str(
        haircolor) + '" dijiste que tenias el pelo cuando escribiste esto. ¿Todavía lo tienes de ese color, o te lo has cambiado? Avísame cuando quieras quedar a tomar algo, y en cuanto podamos lo hacemos. Yo estoy por el centro de BCN, ¿y tú?'

    var3 = 'Hello...que tal por POF, Srta. "' + str(
        username) + '"? Siempre es un poco raro hablar por aqui...pero bueno. Avísame cuando quieras quedar a tomar algo, y en cuanto podamos lo hacemos. Yo estoy por el centro de BCN, ¿y tú? "' + str(
        haircolor) + '" dijiste que tenias el pelo cuando escribiste esto. ¿Todavía lo tienes de ese color, o te lo has cambiado? Pásalo bien!'

    message = random.choice([var1, var2, var3])
    #message = 'Hello Lena'
    #Fill textbox with message and wait
    text_box.send_keys(message)
    time.sleep(random.uniform(1,1.3))
    #CLICK BUTTON TO SEND MESSAGE
    browser.find_element_by_css_selector("#send-quick-message-submit").click()
    time.sleep(random.uniform(1,1.3))
    #write k,v in "contacted" dictionary
    pickled_textFile_contacteddict[k] = v
    print(k + ' has been added to pickled_textFile_contacteddict')
    print('.....................................')

print('Number of users in pickled_textFile_contacteddict: ' + str(len(pickled_textFile_contacteddict)))
print('The content of "pickled_textFile_contacteddict" is now: \n', pickled_textFile_contacteddict)


textFile = open('C:\\Users\\nique\\PycharmProjects\\untitled\\backup_contacted_pof.txt', 'w')
textFile.write(str(pickled_textFile_contacteddict))
textFile.close()

print('\nI AM ABOUT TO PICKLE CONTACTED DICT...\n')

#pickle new contacted_dict in Notepad file, replacing the old one
with open('C:\\Users\\nique\\PycharmProjects\\untitled\\list_pof_contacted.txt', 'wb') as myFile:
    pickle.dump(pickled_textFile_contacteddict, myFile)

print('CONTACTED DICT HAS BEEN PICKLED BACK INTO THE list_pof_contacted.txt FILE')
print('Number of users that have been contacted in this run: ' + str(len(people_to_contact_duplicates_removed)))



browser.close()

#end of program

###################################################################################
#TO WIPE OUT CONTENTS OF CONTACTED_DICT SIMPLY UNCOMMENT THIS SECTION ONCE#########
###################################################################################
# contacted_dict = {}
# #loading dict in the text file and pickling it
# with open('list_pof_contacted.txt', 'wb') as myFile:
#     pickle.dump(contacted_dict, myFile)
#
# #loading dict FROM pickle
# with open('list_pof_contacted.txt', 'rb') as myFile:
#     contacted_dict = pickle.load(myFile)
#
# print('This is the content of contacted_dict', contacted_dict)
###################################################################################