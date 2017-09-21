# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup
import time
import locale
import json
import pycountry


## Country code ##
countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_2


## Setup a set of replacements for unmatched country names ##
REPLACEMENTS = {
    'Bahamas, The': 'Bahamas',
    'Bolivia': 'Bolivia, Plurinational State of',
    'British Virgin Islands': 'Virgin Islands, British',
    'Brunei': 'Brunei Darussalam',
    'Congo, Democratic Republic of the': 'Congo, The Democratic Republic of the',
    'Congo, Republic of the': 'Congo',
    'Gambia, The': 'Gambia',
    'Iran': 'Iran, Islamic Republic of',
    'Korea, North': "Korea, Democratic People's Republic of",
    'Korea, South': 'Korea, Republic of',
    'Laos': "Lao People's Democratic Republic",
    'Macau': 'Macao',
    'Macedonia': 'Macedonia, Republic of',
    'Moldova': 'Moldova, Republic of',
    'Russia': 'Russian Federation',
    'Saint Helena, Ascension, and Tristan da Cunha': 'Saint Helena, Ascension and Tristan da Cunha',
    'Saint Martin': 'Saint Martin (French part)',
    'Sint Maarten': 'Sint Maarten (Dutch part)',
    'Syria': 'Syrian Arab Republic',
    'Taiwan': 'Taiwan, Province of China',
    'Tanzania': 'Tanzania, United Republic of',
    'Venezuela': 'Venezuela, Bolivarian Republic of',
    'Vietnam': 'Viet Nam'
}

EXCEPTIONS = ('Burma', "Cote d'Ivoire", 'Curacao', 'European Union', 'Gaza Strip', 'Kosovo', 'Saint Barthelemy', 'Virgin Islands', 'West Bank', 'World')


## Read CIA's factbook page ##
## Source: https://www.cia.gov/library/publications/the-world-factbook/fields/2010.html ##
html_doc =  urllib.urlopen('https://www.cia.gov/library/publications/the-world-factbook/fields/2010.html')
text = html_doc.read().decode("utf8")
soup = BeautifulSoup(text, 'html.parser')
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


## Parse the html page ##
d = {}
for item in soup.find_all('tr'):
    content = item.text
    country_id = item.get('id')

    if country_id != None:
        counter = 0
        for line in content.splitlines():
            if country_id not in d:
                d[country_id] = {}
                d[country_id]['country_name'] = ''
                d[country_id]['age_group'] = {}

            if counter == 0:
                country_name = line.strip()
                d[country_id]['country_name'] = country_name
                
                if country_name in REPLACEMENTS:
                    d[countries[REPLACEMENTS[country_name]]] = d.pop(country_id)
                    country_id = countries[REPLACEMENTS[country_name]]
                elif country_name in EXCEPTIONS:
                    del d[country_id]
                    counter += 1
                    continue
                else:
                    d[countries[country_name]] = d.pop(country_id)
                    country_id = countries[country_name]

                counter += 1

            else:
                age_g = line.strip().split()[0]
                d[country_id]['age_group'][age_g] = {}
                age_p = float(line.strip().split(': ')[1].split('%')[0])
                d[country_id]['age_group'][age_g]['proportion'] = age_p
                male_f = locale.atoi(line.strip().split('male ')[1].split('/')[0])
                d[country_id]['age_group'][age_g]['male'] = male_f
                female_f = locale.atoi(line.strip().split('female ')[1].split(')')[0])
                d[country_id]['age_group'][age_g]['female'] = female_f


## Save the outcome ##
with open('./cia_factbook.json', 'w') as f:
    json.dump(d, f)

