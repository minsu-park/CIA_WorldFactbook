import urllib
from bs4 import BeautifulSoup
import time

html_doc =  urllib.urlopen('https://www.cia.gov/library/publications/the-world-factbook/fields/2010.html')
text = html_doc.read().decode("utf8")
soup = BeautifulSoup(text, 'html.parser')

for item in soup.find_all('tr'):
    content = item.text
    country_id = item.get('id')
    
    if country_id != None:
        for line in content.splitlines():
            print(line)
            print('xxx')
        print(content)
        print(country_id.upper())

    print('\n\n\n\n\n')
    