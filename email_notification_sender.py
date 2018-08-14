'''This program is based on a real case. It facilitates the onboarding of a new person to a company by streamlining the communication process between departments. In this case, the program checks that someone has been added to an excel sheet and notifies via email another person of this addition to the excel sheet. For example, the CTO approves the recruitment of a new person, adds it to the excel database and this is automatically sent to the personnel department in order to prepare the onboarding process in an orderly and timely fashion'''

import openpyxl #to read excel
import json #to convert dict into string to save in notepad
import smtplib #to send email
import time #used for cron job


#Cron job to make the program run at regular intervals
#if __name__ == '__main__':
while True:


    #MAIN PROGRAM STARTS
    def send_email():
        print('Please enter your email password to send this email')
        pa = input()
        print('connecting...')
        mail = smtplib.SMTP('smtp.mail.yahoo.com', 587, timeout=120)
        mail.ehlo()
        mail.starttls()
        mail.ehlo()
        mail.login('ram_308@yahoo.com', pa)
        mail.sendmail('ram_308@yahoo.com', 'niquel757@gmail.com', content)
        mail.quit()

    def filling_excel():
        for row in range(2, sheet.max_row + 1):
            name = sheet['A' + str(row)].value
            position = sheet['B' + str(row)].value
            start_date = sheet['C' + str(row)].value
            start_date = str(start_date).split(' ')[0]
            upcoming_recruits[name] = [position, start_date]

    #OPEN notepad DICT with "already sent" info
    with open('already_sent.txt') as txtfile:
        already_sent = txtfile.read()

    #INPUT INFO FOR UPCOMING RECRUITS IN NEW DICT
    upcoming_recruits = {}

    #opening excel doc
    wb = openpyxl.load_workbook('new_recruits.xlsx')
    sheet = wb['Sheet1']

    #populating the dictionary with the information
    filling_excel()

    print('already sent:', already_sent)
    print('......')
    print('upcoming recruits:', upcoming_recruits)
    print('......')

    content_email = [] #temporary list to add to content email mssg later

    #comparing if records already exists in recruits_dict
    for k in upcoming_recruits:
        if k not in already_sent:
            #print('UPCOMING RECRUITS TO SEND EMAIL ABOUT: \n')
            to_send = (k, upcoming_recruits[k])
            #print(to_send)
            if to_send:
                content_email.append(to_send)

                # prepare info to send email
                content = '\nHi!\nJust to let you know that soon a new collaborator(s) will be starting with us. \nPlease make sure that you have the onboarding material ready! \nHere is the name, position and start date: \n\n' + str(content_email) + '\n\n Many thanks \n Personnel Department'

                #Sending the email
                send_email()

    #Security check printing
    #print('content email:', content_email)
    try:
        if to_send:
            print('\nEmail successfully sent. The email sent will look like this: \n')
            print(content)
    except:
        print('Program has no new recruits to notify about')
        pass

    #replace already_sent dict by upcoming_recruits info
    with open('already_sent.txt', 'w') as txtfile:
        txtfile.write(json.dumps(upcoming_recruits))

    #close Notepad file
    txtfile.close()

    #cpioqsrhlndfizsg

    #MAKE PROGRAM SLEEP FOR X SECONDS
    time.sleep(20)