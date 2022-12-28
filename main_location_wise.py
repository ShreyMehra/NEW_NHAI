from extract_details_location_wise import Extract
import requests
import re
from collections import defaultdict
data = defaultdict(dict)
import json

def fetch_ids():
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
        }

        data = '{\'TollName\':\'\'}'

        response = requests.post('https://tis.nhai.gov.in/TollPlazaService.asmx/GetTollPlazaInfoGrid', headers=headers, data=data)

        toll_lists = re.findall('javascript:TollPlazaPopup\(\d+\)', response.text)
        toll_ids = [int(re.findall('\d+', id)[0]) for id in toll_lists]

        return toll_ids

def etl():
    i = 0
    ids = fetch_ids()
    for id in ids:
        etl_details = Extract(id)
        etl_details.extract1()
        latitude, longitiude, details = etl_details.extract2(id)
        data[(latitude, longitiude)] = details 
        print(i, id, data)
        i += 1
        
etl()
f = open('final_state_wise.json', 'w+')
json.dump(data, f)
print('Done')
f.close()