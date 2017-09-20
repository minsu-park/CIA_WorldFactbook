import urllib
from bs4 import BeautifulSoup
import time
import locale
import json


html_doc =  urllib.urlopen('https://www.cia.gov/library/publications/the-world-factbook/fields/2010.html')
text = html_doc.read().decode("utf8")
soup = BeautifulSoup(text, 'html.parser')
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

d = {}
for item in soup.find_all('tr'):
    content = item.text
    country_id = item.get('id')

    if country_id != None:
        counter = 0
        for line in content.splitlines():
            if country_id not in d:
                d[country_id] = {}
            if counter == 0:
                country_name = line.strip()
                d[country_id]['country_name'] = country_name
                counter += 1
            else:
                age_g = line.strip().split()[0]
                d[country_id][age_g] = {}
                age_p = float(line.strip().split(': ')[1].split('%')[0])
                d[country_id][age_g]['proportion'] = age_p
                male_f = locale.atoi(line.strip().split('male ')[1].split('/')[0])
                d[country_id][age_g]['male'] = male_f
                female_f = locale.atoi(line.strip().split('female ')[1].split(')')[0])
                d[country_id][age_g]['female'] = female_f

with open('./cia_factbook.json', 'w') as f:
    json.dump(d, f)