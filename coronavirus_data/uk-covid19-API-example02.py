# like uk-covid19-API-example01 but with date not hardcoded
# this time use today's date
from uk_covid19 import Cov19API
import json
import datetime

now = datetime.datetime.today()

# set length to zero initially, inside the while loop
# get the length of the data via the API
# example API output if there is no data: {"data": [],
# "lastUpdate": "2020-11-28T15:17:43.000000Z", "length": 0, "totalPages": 0}
# reset length to the "length" from the API output
length = 0
while(length==0):
    y, m, day, h = now.year, now.month, now.day, now.hour
    print(y, m, day)
        
    all_nations = [
        "areaType=utla",
        f"date={y:d}-{m:02}-{day:02}"
    ]

    cases_spec_pub = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate"
    }

    api = Cov19API(
        filters=all_nations,
        structure=cases_spec_pub
    )

    data = api.get_json()

    all_UTLAs = []
    for d in data['data']:
        # print(d)
        if d['areaName'] not in all_UTLAs:
            all_UTLAs.append(d['areaName'])

    all_UTLAs = sorted(all_UTLAs)
    print(f"newCasesByPublishDate for all UTLAs")
    for a in all_UTLAs:
        print(a, end = ": ")
        utladata = [d for d in data['data'] if d['areaName'] == a]
        for k in utladata:
            print(k['newCasesByPublishDate'])
        
    # find out how long output is
    length = data['length']
    # if it's zero, today's data hasn't been published yet
    if length == 0:
        # go back one day and back to the while statement
        now = now - datetime.timedelta(days=1)
    
json_str = json.dumps(data)
print(f"data for day {y}-{m}-{day}")
outfilename = f'json-{y}-{m:02}-{day:02}.json'
print(f"output file name is: {outfilename}")
with open(outfilename, "w") as f:
    f.write(json_str)
