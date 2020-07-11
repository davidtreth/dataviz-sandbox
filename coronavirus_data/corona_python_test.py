import json
import time
import datetime
from collections import defaultdict
from operator import itemgetter
import sys
if sys.version_info[0] < 3:
	from urllib import urlopen
else:
	from urllib.request import urlopen
    
# read and parse files
# by default use a saved file
with open('20200710/coronavirus-cases_latest.json', 'r') as myfile:
    data=myfile.read()
    cases = json.loads(data)

with open('20200710/coronavirus-deaths_latest.json', 'r') as myfile:
    data=myfile.read()
    deaths=json.loads(data)

# data from coronavirus.data.gov.uk
# note the JSON and CSV data download links that appear 
# on the website are redirects to the ones below

#casesURL = "https://c19downloads.azureedge.net/downloads/json/coronavirus-cases_latest.json"
#deathsURL = "https://c19downloads.azureedge.net/downloads/json/coronavirus-deaths_latest.json"
#casesdata = urlopen(casesURL).read()
#cases = json.loads(casesdata)
#deathsdata = urlopen(deathsURL).read()
#deaths = json.loads(deathsdata)

# print summary information

print(str(cases['metadata']))
print(str(cases['dailyRecords']))


cases_by_country = defaultdict(list)
for i in cases['countries']:
    # it turns out that only England and Cornwall is listed day by day basis on coronavirus.data.gov.uk
    areaname = i['areaName']
    cases_by_country[areaname].append((i['specimenDate'],i['dailyLabConfirmedCases']))

deaths_by_country = defaultdict(list)
for i in deaths['countries']:
    # deaths are not listed at regional or local authority level on coronavirus.data.gov.uk
    areaname = i['areaName']
    deaths_by_country[areaname].append((i['reportingDate'],i['dailyChangeInDeaths']))

cases_by_region = defaultdict(list)
for i in cases['regions']:
    areaname = i['areaName']
    cases_by_region[areaname].append((i['specimenDate'],i['dailyLabConfirmedCases']))

cases_by_utla = defaultdict(list)
for i in cases['utlas']:
    areaname = i['areaName']
    cases_by_utla[areaname].append((i['specimenDate'],i['dailyLabConfirmedCases']))

cases_by_ltla = defaultdict(list)
for i in cases['ltlas']:
    areaname = i['areaName']
    cases_by_ltla[areaname].append((i['specimenDate'],i['dailyLabConfirmedCases']))

def datestr_to_date(datestr):
    y = int(datestr[0:4])
    m = int(datestr[5:7])
    d = int(datestr[8:10])
    return datetime.date(y,m,d)
    
def get_cases_by_date(cases_utla, startDate, endDate):
    cases_by_date = {}
    for d in cases_utla:
        cases_by_date[datestr_to_date(d[0])] = d[1]
        
    d = startDate
    while d <=endDate:
        if d not in cases_by_date:
            cases_by_date[d] = 0
        d += datetime.timedelta(days=1)
    return cases_by_date

def print_cases_by_area(cases_by_area, symbol="*"):
    for area in sorted(cases_by_area):
        cases_by_area[area] = sorted(cases_by_area[area], key=itemgetter(0))
        startDate = cases_by_area[area][0][0]
        endDate = cases_by_area[area][-1][0]
        startDate = datestr_to_date(startDate)
        endDate = datestr_to_date(endDate)
        if area == "England":
            areaprint = "England and Cornwall"
        else:
            areaprint = area
        print(areaprint, startDate)
        time.sleep(1)
        cases_by_date = get_cases_by_date(cases_by_area[area], startDate, endDate)
        ncases_list = list(cases_by_date.items())        
        ncases_list = sorted(ncases_list, key=itemgetter(0))            
        datelist = [i[0] for i in ncases_list]
        ncases_valslist = [i[1] if i[1] else 0 for i in ncases_list]
        for n in zip(datelist, ncases_valslist):
            print(n[0], symbol*n[1])
            time.sleep(0.05)
        print("\n")

print("cases by country\n")
print_cases_by_area(cases_by_country, "*")
print("deaths (date reported) by country\n")
print_cases_by_area(deaths_by_country, "+")
print("cases by region (England and Cornwall only)\n")
print_cases_by_area(cases_by_region, "*")
print("cases by Upper-Tier Local Authority (England and Cornwall only)\n")
print_cases_by_area(cases_by_utla, "*")
print("cases by Lower-Tier Local Authority (England and Cornwall only)\n")
print_cases_by_area(cases_by_ltla, "*")
