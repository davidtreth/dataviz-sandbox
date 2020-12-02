#  write out the daily case numbers from the start of the pandemic to 
#  todays date
#  for UK total, nations, regions
from uk_covid19 import Cov19API
import csv
import datetime
import os
import numpy as np
from collections import defaultdict

now = datetime.datetime.today()

# set length to zero initially, inside the while loop
# get the length of the data via the API
# example API output if there is no data: {"data": [],
# "lastUpdate": "2020-11-28T15:17:43.000000Z", "length": 0, "totalPages": 0}
# reset length to the "length" from the API output

print(f"new cases by date")
print(f"date ; newCasesBySpecimenDate; newCasesByPublishDate")

nonzero = 0
datearr = defaultdict(list)
newSpecarr = defaultdict(list) 
newPubarr = defaultdict(list)
zippedarr = defaultdict(list)

# UK totals
all_UK = [
    "areaType=overview",
]
# Eng, Scot, Wales, NI
all_nations = [
    "areaType=nation",
]
# regions of England only
all_regions = [
    "areaType=region",
]
# upper tier local authorities
all_UTLAs = [
    "areaType=utla",
]

# lower tier local authorities
all_LTLAs = [
    "areaType=ltla",
]

cases_spec_pub = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate"
    }

for level, areatype in enumerate([all_UK, all_nations, all_regions,
                                  all_UTLAs, all_LTLAs]):
    startdate = datetime.datetime(year=2020, month=2, day=1)
    date = startdate    
    api = Cov19API(
            filters=areatype,
            structure=cases_spec_pub
        )
    data = api.get_json()
    # print(data)

    # collect names of the areas
    all_UTLAs = []
    for d in data['data']:
        # print(d)
        if d['areaName'] not in all_UTLAs:
            all_UTLAs.append(d['areaName'])

    all_UTLAs = sorted(all_UTLAs)
    # print(all_UTLAs)
    
    while(date < now):
        y, m, day = date.year, date.month, date.day
        # print(f"{y:d}-{m:02}-{day:02}")
        for a in all_UTLAs:
            # print(a, end = ": ")
            # select out the data for each area
            # and then on a particular date
            utladata = [d for d in data['data'] if d['areaName'] == a]
            utladata_day = [
                        d for d in utladata if datetime.datetime.fromisoformat(
                        d['date']) == date]
            for k in utladata_day:
                newSpec = k['newCasesBySpecimenDate']
                newPub = k['newCasesByPublishDate']
                if newSpec is None:
                    newSpec = 0
                if newPub is None:
                    newPub = 0
                nonzero += newSpec
                nonzero += newPub
                if nonzero > 0:
                    print(a, k['date'], newSpec, newPub)
                    datearr[a].append(k['date'])
                    newSpecarr[a].append(newSpec)
                    newPubarr[a].append(newPub)
        # increment date before going back to top of while loop              
        date = date + datetime.timedelta(days=1)
    # output directory, where the UK and national totals are saved
    outdir = "data_all"
    # subdirectories to save data for regions and local authorities
    outdir2 = "regions"
    outdir3 = "UTLAs"
    outdir4 = "LTLAs"
    if level == 2:
        outdir = os.path.join(outdir, outdir2)
    elif level == 3:
        outdir = os.path.join(outdir, outdir3)
    elif level == 4:
        outdir = os.path.join(outdir, outdir4)    
    for a in all_UTLAs:        
        zippedarr[a] = zip(datearr[a], newSpecarr[a], newPubarr[a])
        # print(a, list(zippedarr[a]))
        # write to csv file
        # replace spaces with underscores and remove commas
        outfilename = f'{a.replace(" ", "_").replace(",", "")}-cases.csv'

        outfilename = os.path.join(outdir, outfilename)
        with open(outfilename, 'w', newline='') as csvfile:
            fieldnames = ['date', 'newCasesBySpecimenDate',
                          'newCasesByPublishDate']
            spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                        delimiter=",")
            spamwriter.writeheader()
            for r in zippedarr[a]:
                spamwriter.writerow({'date': r[0],
                                    'newCasesBySpecimenDate': r[1],
                                    'newCasesByPublishDate': r[2]})
