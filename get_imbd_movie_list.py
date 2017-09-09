#Python program by Javier Marti
'''This program uses beautifulsoup  and phantomJS to extract a list of movies from IMDB.com
Copyright JavierMarti.co.uk'''

from selenium import webdriver
from bs4 import BeautifulSoup

# create driver
#driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs_win32\phantomjs.exe')
driver = webdriver.PhantomJS(executable_path = r'D:\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe')

url = 'http://www.imdb.com/chart/top'
driver.get(url)
print("starting to get website...")
soup = BeautifulSoup(driver.page_source, 'lxml')

table = soup.find('table', class_ = 'chart')

for td in table.find_all('td', class_ = 'titleColumn'):
    full_title = td.text.strip().replace('\n', '').replace('      ', '')
    print(full_title)


# print("finished getting website...")
# #print (html_doc)
#
# print(soup.prettify())
# driver.close()