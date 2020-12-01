#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
from collections import defaultdict
from operator import itemgetter
import csv
import argparse
import numpy
import glob
import os


# this version uses the fiels generated using the Public Health England API
# publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/index.html
# first run uk-covid19-API-download_all_utla.py
# and uk-covid19-API-download_all_nation.py   

cases_by_country = defaultdict(list)
cases_by_region = defaultdict(list)
cases_by_UTLA = defaultdict(list)


nationdatadir = 'data_all'
os.chdir(nationdatadir)

# get UK total
UK_csvs = list(glob.glob("United_Kingdom*csv"))
UK_csvs.sort(reverse=True)
#print(UK_csvs[0])

areaname = UK_csvs[0].split("-")[0]



datearray = []
with open(UK_csvs[0]) as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter = ",")
    for row in spamreader:
        d = row['date']
        s = row['newCasesBySpecimenDate']
        p = row['newCasesByPublishDate']
        datearray.append(d)
        cases_by_country['United Kingdom'].append((d, int(s)))
                    
datearray_obj = [datetime.datetime.fromisoformat(d) for d in datearray]
mindate = min(datearray_obj)
maxdate = max(datearray_obj)

# nations
nation_csvs = list(glob.glob("*csv"))
nation_csvs = [n for n in nation_csvs if n.split("-")[0] != "United_Kingdom"]

#print(nation_csvs)
for n in nation_csvs:
    areaname = n.split("-")[0]
    with open(n) as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter = ",")
        for row in spamreader:
            d = row['date']
            s = row['newCasesBySpecimenDate']
            p = row['newCasesByPublishDate']            
            cases_by_country[areaname].append((d, int(s)))    

# regions of England
os.chdir("regions")
region_csvs = list(glob.glob("*csv"))
#print(region_csvs)
for r in region_csvs:
    areaname = r.split("-")[0]
    with open(r) as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter = ",")
        for row in spamreader:
            d = row['date']
            s = row['newCasesBySpecimenDate']
            p = row['newCasesByPublishDate']            
            cases_by_region[areaname].append((d, int(s)))    
os.chdir("..")

# Upper Tier Local Authorities
os.chdir("UTLAs")
UTLA_csvs = list(glob.glob("*csv"))
#print(UTLA_csvs)
for n in UTLA_csvs:
    areaname = n.split("-")[0]
    with open(n) as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter = ",")
        for row in spamreader:
            d = row['date']
            s = row['newCasesBySpecimenDate']
            p = row['newCasesByPublishDate']            
            cases_by_UTLA[areaname].append((d, int(s)))    
os.chdir("..")

os.chdir("..")

    
        


