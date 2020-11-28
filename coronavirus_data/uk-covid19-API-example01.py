from uk_covid19 import Cov19API
import json

all_nations = [
    "areaType=utla",
    "date=2020-11-28"
]

cases_and_deaths = {
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    "newCasesByPublishDate": "newCasesByPublishDate"
}

api = Cov19API(
    filters=all_nations,
    structure=cases_and_deaths
)

data = api.get_json()

all_UTLAs = []
for d in data['data']:
    print(d)
    if d['areaName'] not in all_UTLAs:
        all_UTLAs.append(d['areaName'])

all_UTLAs = sorted(all_UTLAs)

for a in all_UTLAs:
    print(a)

json_str = json.dumps(data)
with open("json-2020-11-28.json", "w") as f:
    f.write(json_str)
