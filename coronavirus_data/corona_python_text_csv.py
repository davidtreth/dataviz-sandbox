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
    print(c, countries_dailyarrays[c])

areas_dailyarrays = {}            
for a in areas_casearrays:
    areas_dailyarrays[a] = numpy.zeros(len(areas_casearrays[a]))
    for i, v in enumerate(areas_casearrays[a]):
        if i > 0:
            areas_dailyarrays[a][i] = areas_casearrays[a][i] - areas_casearrays[a][i-1]
    print(a, areas_dailyarrays[a])
