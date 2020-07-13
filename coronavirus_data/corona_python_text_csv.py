#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
from collections import defaultdict
from operator import itemgetter
import csv
import argparse
    
# this version uses the .csv files available at https://github.com/tomwhite/covid-19-uk-data

# print summary information

with open('20200713/covid-19-cases-uk.csv', newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter = ",")
    for row in spamreader:
        print(row['Date'], row['Country'], row['Area'], row['TotalCases'])
