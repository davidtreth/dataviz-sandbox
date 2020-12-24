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


# this version uses the files generated using the Public Health England API
# publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/index.html
# first run uk-covid19-API-download_all_utla.py
# and uk-covid19-API-download_all_nation.py   

cases_by_country = defaultdict(list)
cases_by_region = defaultdict(list)
cases_by_UTLA = defaultdict(list)
cases_by_LTLA = defaultdict(list)

# enter the directory with the csv files in
nationdatadir = 'data_all'
os.chdir(nationdatadir)

# nations and United Kingdom total
nation_csvs = list(glob.glob("*csv"))
# print(nation_csvs)
for n in nation_csvs:
    areaname = n.split("-")[0]
    with open(n) as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter = ",")
        for row in spamreader:
            d = row['date']
            s = row['newCasesBySpecimenDate']
            p = row['newCasesByPublishDate'] 
            r100k = row['rate100kSpecDateLast7Days']           
            cases_by_country[areaname].append((d, int(s), float(r100k)))    

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
            r100k = row['rate100kSpecDateLast7Days']            
            cases_by_region[areaname].append((d, int(s), float(r100k)))    
os.chdir("..")

# Upper Tier Local Authorities
os.chdir("UTLAs")
UTLA_csvs = list(glob.glob("*csv"))
# print(UTLA_csvs)
for n in UTLA_csvs:
    areaname = n.split("-")[0]
    with open(n) as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter = ",")
        for row in spamreader:
            d = row['date']
            s = row['newCasesBySpecimenDate']
            p = row['newCasesByPublishDate']
            r100k = row['rate100kSpecDateLast7Days']            
            cases_by_UTLA[areaname].append((d, int(s), float(r100k)))    
os.chdir("..")

# Lower Tier Local Authorities
# not currently used by pygame_apidata.py
os.chdir("LTLAs")
LTLA_csvs = list(glob.glob("*csv"))
# print(LTLA_csvs)
for n in LTLA_csvs:
    areaname = n.split("-")[0]
    with open(n) as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter = ",")
        for row in spamreader:
            d = row['date']
            s = row['newCasesBySpecimenDate']
            p = row['newCasesByPublishDate']
            r100k = row['rate100kSpecDateLast7Days']            
            cases_by_LTLA[areaname].append((d, int(s), float(r100k)))    
os.chdir("..")

os.chdir("..")

    
        


