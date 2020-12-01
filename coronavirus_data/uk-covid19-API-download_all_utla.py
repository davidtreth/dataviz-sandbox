#  write out the daily case numbers from the start of the pandemic to 
# todays date
# for all UTLAs
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

startdate = datetime.datetime(year=2020, month=2, day=1)

date = startdate

print(f"new cases by date")
print(f"date ; newCasesBySpecimenDate; newCasesByPublishDate")

nonzero = 0
datearr = defaultdict(list)
newSpecarr = defaultdict(list) 
newPubarr = defaultdict(list)
zippedarr = defaultdict(list)

all_UTLAs = [
    "areaType=utla",
]

cases_spec_pub = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate"
    }

api = Cov19API(
        filters=all_UTLAs,
        structure=cases_spec_pub
    )
data = api.get_json()
print(data)

all_UTLAs = []
for d in data['data']:
    # print(d)
    if d['areaName'] not in all_UTLAs:
        all_UTLAs.append(d['areaName'])

all_UTLAs = sorted(all_UTLAs)
            
while(date < now):
    y, m, day = date.year, date.month, date.day
    #print(f"{y:d}-{m:02}-{day:02}")
    for a in all_UTLAs:
        #print(a, end = ": ")
        utladata = [d for d in data['data'] if d['areaName'] == a]
        utladata_day = [
    d for d in utladata if datetime.datetime.fromisoformat(d['date']) == date]
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
                  
    date = date + datetime.timedelta(days=1)

outdir = "data_all_utla"
for a in all_UTLAs:        
    zippedarr[a] = zip(datearr[a], newSpecarr[a], newPubarr[a])

    # write to csv file
    outfilename = f'{a.replace(" ", "_")}-up-to-{y}-{m:02d}-{day:02d}.csv'
    outfilename = os.path.join(outdir, outfilename)
    with open(outfilename, 'w', newline='') as csvfile:
        fieldnames = ['date', 'newCasesBySpecimenDate', 'newCasesByPublishDate']
        spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                    delimiter=",")
        spamwriter.writeheader()
        for r in zippedarr[a]:
            spamwriter.writerow({'date': r[0], 'newCasesBySpecimenDate': r[1],
                                'newCasesByPublishDate': r[2]})

