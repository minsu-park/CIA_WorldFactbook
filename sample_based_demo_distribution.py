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

target_num_sample = 7000000
d_proportion = {}
for country_code in d:
    d_proportion[country_code] = {}
    d_proportion[country_code]['male'] = {}
    d_proportion[country_code]['female'] = {}
    for gender_group in d[country_code]:
        for age_group in d[country_code][gender_group]:
            d_proportion[country_code][gender_group][str(age_group)] = float(d[country_code][gender_group][age_group])/total_p*target_num_sample
