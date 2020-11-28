#  write out the daily case numbers from the start of the pandemic to 
# todays date - in this example for Cornwall and Isles of Scilly
from uk_covid19 import Cov19API
import csv
import datetime
import numpy as np

now = datetime.datetime.today()

# set length to zero initially, inside the while loop
# get the length of the data via the API
# example API output if there is no data: {"data": [],
# "lastUpdate": "2020-11-28T15:17:43.000000Z", "length": 0, "totalPages": 0}
# reset length to the "length" from the API output

startdate = datetime.datetime(year=2020, month=2, day=1)

date = startdate

print(f"new cases by date for Cornwall and IoS")
print(f"date ; newCasesBySpecimenDate; newCasesByPublishDate")

nonzero = 0
datearr = []
newSpecarr = []
newPubarr = []

while(date < now):
    y, m, day = date.year, date.month, date.day
    #print(f"{y:d}-{m:02}-{day:02}")
        
    #all_nations = [
    #    "areaType=utla",
    #    f"date={y:d}-{m:02}-{day:02}"
    #]
    cornwallIoS = [
        "areaType=utla",
        "areaName=Cornwall and Isles of Scilly",
        f"date={y:d}-{m:02}-{day:02}"
    ]

    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate"
    }

    api = Cov19API(
        filters=cornwallIoS,
        structure=cases_and_deaths
    )

    data = api.get_json()
    # print(data)
    all_UTLAs = []
    for d in data['data']:
        # print(d)
        if d['areaName'] not in all_UTLAs:
            all_UTLAs.append(d['areaName'])

    all_UTLAs = sorted(all_UTLAs)
    
    
    for a in all_UTLAs:
        #print(a, end = ": ")
        utladata = [d for d in data['data'] if d['areaName'] == a]
        for k in utladata:
            newSpec = k['newCasesBySpecimenDate']
            newPub = k['newCasesByPublishDate']
            if newSpec is None:
                newSpec = 0
            if newPub is None:
                newPub = 0
            nonzero += newSpec
            nonzero += newPub
            if nonzero > 0:
                print(k['date'], newSpec, newPub)
                datearr.append(k['date'])
                newSpecarr.append(newSpec)
                newPubarr.append(newPub)
                  
    date = date + datetime.timedelta(days=1)
        
zippedarr = zip(datearr, newSpecarr, newPubarr)

# write to csv file
outfilename = f'cornwallIoS-all-up-to-{y}-{m:02d}-{day:02d}.csv'
with open(outfilename, 'w', newline='') as csvfile:
    fieldnames = ['date', 'newCasesBySpecimenDate', 'newCasesByPublishDate']
    spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=",")
    spamwriter.writeheader()
    for r in zippedarr:
        spamwriter.writerow({'date': r[0], 'newCasesBySpecimenDate': r[1],            
                             'newCasesByPublishDate': r[2]})
# print(f"output file name is: {outfilename}")
# with open(outfilename, "w") as f:
    # f.write(json_str)
