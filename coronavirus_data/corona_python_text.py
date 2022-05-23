#!/usr/bin/python
# -*- coding: utf-8 -*-
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
import argparse
    
# read and parse files
# by default use a saved file
with open('20200727/coronavirus-cases_latest.json', 'r') as myfile:
    data=myfile.read()
    cases = json.loads(data)

with open('20200727/coronavirus-deaths_latest.json', 'r') as myfile:
    data=myfile.read()
    deaths=json.loads(data)

# data from coronavirus.data.gov.uk
# note the JSON and CSV data download links that appear 
# on the website are redirects to the ones below

# TO DO - add Scotland and Wales data at local authority level

# wales has a dashboard at 
# https://public.tableau.com/profile/public.health.wales.health.protection#!/vizhome/RapidCOVID-19virology-Public/Headlinesummary
# providing a download in Excel format - though its URL may not be static
# public health scotland 
# https://www.publichealthscotland.scot/our-areas-of-work/sharing-our-data-and-intelligence/coronavirus-covid-19-data/
# data available as .csv from https://www.opendata.nhs.scot/dataset/covid-19-in-scotland
# northern ireland
# https://www.nisra.gov.uk/statistics/ni-summary-statistics/coronavirus-covid-19-statistics
# but doesn't seem to have detailed daily stats in an easy to download and use format
# https://app.powerbi.com/view?r=eyJrIjoiZGYxNjYzNmUtOTlmZS00ODAxLWE1YTEtMjA0NjZhMzlmN2JmIiwidCI6IjljOWEzMGRlLWQ4ZDctNGFhNC05NjAwLTRiZTc2MjVmZjZjNSIsImMiOjh9
# since these are not in consistent formats, I will instead use the file from https://github.com/tomwhite/covid-19-uk-data


#casesURL = "https://c19downloads.azureedge.net/downloads/json/coronavirus-cases_latest.json"
#deathsURL = "https://c19downloads.azureedge.net/downloads/json/coronavirus-deaths_latest.json"
#casesdata = urlopen(casesURL).read()
#cases = json.loads(casesdata)
#deathsdata = urlopen(deathsURL).read()
#deaths = json.loads(deathsdata)

# print summary information

for d in cases['metadata']:
    print(d, cases['metadata'][d])
for d in cases['dailyRecords']:
    print(d, cases['dailyRecords'][d])
print("\n")

for d in deaths['metadata']:
    print(d, deaths['metadata'][d])

print("\n")

cases_by_country = defaultdict(list)
for i in cases['countries']:
    # it turns out that only England and Cornwall is listed day by day basis on coronavirus.data.gov.uk
    areaname = i['areaName']
    cases_by_country[areaname].append((i['specimenDate'],i['dailyLabConfirmedCases']))


deaths_by_country = defaultdict(list)
deaths_UK = defaultdict(list)

for i in deaths['overview']:
    # UK figure
    areaname = i['areaName']
    deaths_UK[areaname].append((i['reportingDate'],i['dailyChangeInDeaths']))
    
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

def print_cases_by_area(cases_by_area, symbol="*", sleep=True):
    for area in sorted(cases_by_area):
        cumulative = 0
        last14days = 0
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
        if sleep:
            time.sleep(1)
        cases_by_date = get_cases_by_date(cases_by_area[area], startDate, endDate)
        ncases_list = list(cases_by_date.items())        
        ncases_list = sorted(ncases_list, key=itemgetter(0))            
        datelist = [i[0] for i in ncases_list]
        ncases_valslist = [i[1] if i[1] else 0 for i in ncases_list]
        headerstr = "{d:<10} {s:<60}{c} {l}".format(d="Date", s="cases/deaths", c="cumulative", l="last 14 days")
        print(headerstr)
        for i, n in enumerate(zip(datelist, ncases_valslist)):
            cumulative += n[1]
            last14days += n[1]
            if i >= 14:
                last14days -= ncases_valslist[i-14]
            outstr = "{d} {s:<60}{c:>7}{l:>7}".format(d=n[0], s=symbol*n[1], c=cumulative, l=last14days)
            print(outstr)
            if sleep:
                time.sleep(0.05)
        print("\n")
        
if __name__ == '__main__':
    """
    If invoked at the command-line
    """
    # Create the command line options parser.
    parser = argparse.ArgumentParser()
    parser.add_argument("--sleep",action="store_true",
                        help="add time.sleep calls to make it possible to read the output on the terminal")
    parser.add_argument("--fullblock",action="store_true",
                        help="use the Unicode full block character U+2588 rather than the asterisk or plus for both cases and deaths")
    parser.add_argument("--microbe",action="store_true",
                        help="use the Unicode microbe emoji character U+1F9A0 rather than the asterisk for cases. takes priority over the fullblock")            
    
    args = parser.parse_args()

    if args.microbe:
        cases_sym = "🦠"
    elif args.fullblock:
        cases_sym = "█"
    else:
        cases_sym = "*"
    if args.fullblock:
        deaths_sym = "█"
    else:
        deaths_sym = "+"
        
    print("cases by country\n")
    print_cases_by_area(cases_by_country, cases_sym, args.sleep)
    print("deaths (date reported) United Kingdom\n")
    print_cases_by_area(deaths_UK, deaths_sym, args.sleep)
    print("deaths (date reported) by country\n")
    print_cases_by_area(deaths_by_country, deaths_sym, args.sleep)
    print("cases by region (England and Cornwall only)\n")
    print_cases_by_area(cases_by_region, cases_sym, args.sleep)
    print("cases by Upper-Tier Local Authority (England and Cornwall only)\n")
    print_cases_by_area(cases_by_utla, cases_sym, args.sleep)
    print("cases by Lower-Tier Local Authority (England and Cornwall only)\n")
    print_cases_by_area(cases_by_ltla, cases_sym, args.sleep)
