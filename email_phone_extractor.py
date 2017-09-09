#Python program by Javier Marti
'''This program uses Regex to extract emails from a webpage, and copy them to clipboard. It can also be fed a list of webpages and opening webpages in new tabs to proceed with the information extraction.
Copyright JavierMarti.co.uk'''

import re, pyperclip

#create regex object for phone numbers
phoneRegex = re.compile(r"""
    #515-345-3453, 233-4444, (234) 234-34983, 555-9999 ext 12345, ext. 12345, x12345
(
((\d\d\d)|(\(\d\d\d\)))?     #area code (optional)
(\s|-)                       # first separator
\d\d\d                       # first 3 digits
-                            # another separator
\d\d\d\d                     #last four digits
(((ext(\.)?\s)|x)            # extension word part (optional)
 (\d{2,5}))?                 # extension num part (optional)
)
""", re.VERBOSE)


#create a regex for emails
emailRegex = re.compile(r"""
                    # something.+_@something.com we create our own character class with []
[a-zA-Z0-9_.+]+     #name part (the "+" indicated that we'll be searching for one or more of htem
@                   #@ symbol
[a-zA-Z0-9_.+]+     #domain name part
""", re.VERBOSE)

#Get the text off the clipboard
text = pyperclip.paste()

#extract the email /phone from this list
extractedPhone = phoneRegex.findall(text)
extractedEmail = emailRegex.findall(text)

#problem is that the first item in the tuple is the phone number. Solution:
allPhoneNumbers = [] # this will go through all tuples and extract first value
for phoneNumber in extractedPhone:
    allPhoneNumbers.append(phoneNumber[0]) #this will append it to the list we created (allPhoneNumbers)

print(allPhoneNumbers)
print(extractedEmail)

#copy the extracted email/phone to the clipboard
results = '\n'.join(allPhoneNumbers ) + '\n' + '\n'.join(extractedEmail)   #this will add a new line for each result, so the output looks nicer
pyperclip.copy(results)




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