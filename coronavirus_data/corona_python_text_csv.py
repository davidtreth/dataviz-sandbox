#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
from collections import defaultdict
from operator import itemgetter
import csv
import argparse
import numpy
from corona_python_text import datestr_to_date
    
# this version uses the .csv files available at https://github.com/tomwhite/covid-19-uk-data

# print summary information


# either local authorities or health board areas

areas_all = []
countries = []
countries_areaarr = defaultdict(list)
datearray = []
with open('20200713/covid-19-cases-uk.csv', newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter = ",")
    for row in spamreader:
        #print(row['Date'], row['Country'], row['Area'], row['TotalCases'])
        d = row['Date']
        c = row['Country']
        a = row['Area']
        t = row['TotalCases']
        if d not in datearray:
            datearray.append(d)
        if c not in countries:
            countries.append(c)
        if a not in areas_all:
            areas_all.append(a)
        if a not in countries_areaarr[c]:
            countries_areaarr[c].append(a)

datearray_obj = [datestr_to_date(d) for d in datearray]
mindate = min(datearray_obj)
maxdate = max(datearray_obj)

print(mindate, maxdate)

# create arrays of the dates, filling gaps
# and also the cumulative numbers of cases

countries_datearrays = defaultdict(list)
areas_datearrays = defaultdict(list)
countries_casearrays = defaultdict(list)
areas_casearrays = defaultdict(list)

for c in countries:
    d = mindate
    while d <= maxdate:
        countries_datearrays[c].append(d)
        d += datetime.timedelta(days=1)
    countries_casearrays[c] = numpy.zeros(len(countries_datearrays[c]))
        
for a in areas_all:
    d = mindate
    while d <= maxdate:
        areas_datearrays[a].append(d)
        d += datetime.timedelta(days=1)
    areas_casearrays[a] = numpy.zeros(len(areas_datearrays[a]))
    

with open('20200713/covid-19-cases-uk.csv', newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter = ",")
    for row in spamreader:
        #print(row['Date'], row['Country'], row['Area'], row['TotalCases'])
        d = row['Date']
        c = row['Country']
        a = row['Area']
        t = row['TotalCases']
        if t == "NaN":
            t = 0
        else:
            t = int(t)
        dobj = datestr_to_date(d)
        tdelta = int((dobj-mindate)/datetime.timedelta(days=1))
        #countries_casearrays[c][tdelta] += t
        areas_casearrays[a][tdelta] += t
        
        
        
# fill gaps in cumulative totals        
#for c in countries_casearrays:
#    maxv = 0
#    for i, v in enumerate(countries_casearrays[c]):
#        if v > maxv:
#            maxv = v
#        if maxv > 0 and v == 0:
#            countries_casearrays[c][i] = countries_casearrays[c][i-1]
#    print(c, countries_casearrays[c])

for a in areas_casearrays:
    maxv = 0
    for i, v in enumerate(areas_casearrays[a]):
        if v > maxv:
            maxv = v
        if maxv > 0 and v == 0:
            areas_casearrays[a][i] = areas_casearrays[a][i-1]
        for c in countries_areaarr:
            if a in countries_areaarr[c]:
                countries_casearrays[c][i] += areas_casearrays[a][i]
             
    #print(a, areas_casearrays[a])

#for c in countries_casearrays:
    #print(c, countries_casearrays[c])    
# create daily arrays:

countries_dailyarrays = {}
for c in countries_casearrays:
    countries_dailyarrays[c] = numpy.zeros(len(countries_casearrays[c]))
    for i, v in enumerate(countries_casearrays[c]):        
        if i > 0:
            countries_dailyarrays[c][i] = countries_casearrays[c][i]-countries_casearrays[c][i-1]
        else:
            countries_dailyarrays[c][i] = countries_casearrays[c][i]
    #print(c, countries_casearrays[c], countries_dailyarrays[c])

areas_dailyarrays = {}            
for a in areas_casearrays:
    areas_dailyarrays[a] = numpy.zeros(len(areas_casearrays[a]))
    for i, v in enumerate(areas_casearrays[a]):
        if i > 0:
            areas_dailyarrays[a][i] = areas_casearrays[a][i] - areas_casearrays[a][i-1]
        else:
            areas_dailyarrays[a][i] = areas_casearrays[a][i]
    #print(a, areas_dailyarrays[a])

def print_cases_by_area(areaname, datearray_obj, casearray, dailyarray, tsleep=0, symbol="*"):
    if areaname == "England":
        areaname = "England and Cornwall"
    headerstr = "{d:<10} {n:<6} {s:<60}{c} {l}".format(d="Date", s="cases/deaths", n="dailyN", c="cumulative", l="last 14 days")
    print(areaname)
    print(headerstr)
    last14days = 0
    #print(dailyarray)
    for i, (d, c, n) in enumerate(zip(datearray_obj, casearray, dailyarray)):    
        last14days += int(n)
        if i >= 14:
            last14days -= int(dailyarray[i-14])
        outstr = "{d} {n:<5} {s:<60}{c:>7}{l:>7}".format(d=d, n = int(n), s=symbol*int(n), c=int(c), l=last14days)
        print(outstr)
        time.sleep(tsleep)
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
        
    if args.sleep:
        tsleep = 0.05
    else:
        tsleep = 0
        
    for c in countries:
        print_cases_by_area(c, datearray_obj, countries_casearrays[c], countries_dailyarrays[c], tsleep, cases_sym)

# remove Northern Ireland due to problems with the data
# some of the area names are not consistent with each other
# could go by area codes but then there are certain lines
# without an area code in the Wales data, i.e. for those outside of Wales
# or Unknown

    countries.remove("Northern Ireland")
    for c in countries:
        for a in sorted(countries_areaarr[c]):
            print_cases_by_area(a, datearray_obj, areas_casearrays[a], areas_dailyarrays[a], tsleep, cases_sym)
