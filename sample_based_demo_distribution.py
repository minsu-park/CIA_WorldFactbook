import glob
import json
import gzip


## Factbook ##
with open('./cia_factbook.json') as infile:
    fb = json.load(infile)

## Proportion across globe ##
d = {}
total_p = 0
for country_code in fb:
    d[country_code] = {}
    d[country_code]['male'] = {}
    d[country_code]['female'] = {}
    for age_group in fb[country_code]['age_group']:
        d[country_code]['male'][str(age_group)] = fb[country_code]['age_group'][age_group]['male']
        d[country_code]['female'][str(age_group)] = fb[country_code]['age_group'][age_group]['female']
        total_p += fb[country_code]['age_group'][age_group]['male'] + fb[country_code]['age_group'][age_group]['female']

d_proportion = {}
for country_code in d:
    d_proportion[country_code] = {}
    d_proportion[country_code]['male'] = {}
    d_proportion[country_code]['female'] = {}
    for gender_group in d[country_code]:
        for age_group in d[country_code][gender_group]:
            d_proportion[country_code][gender_group][str(age_group)] = float(d[country_code][gender_group][age_group])/total_p*10000000

for country_code in d_proportion:
    if country_code == 'US':
        print(country_code, d_proportion[country_code])
    if country_code == 'NO':
        print(country_code, d_proportion[country_code])
    if country_code == 'PA':
        print(country_code, d_proportion[country_code])
    if country_code == 'GB':
        print(country_code, d_proportion[country_code])
    if country_code == 'FR':
        print(country_code, d_proportion[country_code])    
    if country_code == 'SE':
        print(country_code, d_proportion[country_code])
    if country_code == 'TW':
        print(country_code, d_proportion[country_code])
    if country_code == 'DE':
        print(country_code, d_proportion[country_code])

    

"""
for filename in glob.iglob('./*.gz'):
    for line in gzip.open(filename, 'rb'):
        fields = json.loads(line.strip())
        country_code = fields['reporting_country'].lower()

        if 
"""