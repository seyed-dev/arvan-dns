import requests
import json
import time
import argparse

BASE_URL = f'https://napi.arvancloud.ir/cdn/4.0/domains'
RECORDS = 0


parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument('--bearer_token', required=True, help='your bearer_token')
parser.add_argument('--old_ip', required=True, help='your old ip')
parser.add_argument('--new_ip', required=True, help='your new ip')
parser.add_argument('--domains_file', required=True, help='file with domains')
parser.add_argument('--sleep_time', required=False, default=10, help='sleep time between requests')
parser.add_argument('--port', required=False, default=8080, help='sleep time between requests')

args = parser.parse_args()

BEARER_TOKEN = args.bearer_token
OLD_IP = args.old_ip
NEW_IP = args.new_ip
SLEEP_TIME = int(args.sleep_time)
DOMAINS_FILE = args.domains_file
PORT = args.port

headers = {
        'authority': 'napi.arvancloud.ir',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'fa',
        'authorization': f'Bearer DwVZf8ZpyZgP5eoGVP5KUMxeLAAJziAxUBu7Cu2Vf0s6e0jRKoqzsVAbYiGDiWZ6d973Lb5xQlhzzcy2qd6CrD0Q7aCsMQ4KSQlMqjOkDy1R74HfMdSK0gG5Jwdonqe2K4LJWmL1xXRrzdzlmPr5pDmYxLkaaYAbNQYEdttFOFJK6PgJs5FS9HMXTgy27Ip7EzvRGrV6Jb0PQx4npsk2lKjXSWWnclS7SboLUs6gE7mslR92oH3e2Cku5VB9bxX.d8e200a4-1307-441e-a920-9cccf7f4b23d',
        'content-type': 'application/json',
        'origin': 'https://panel.arvancloud.ir',
        'referer': 'https://panel.arvancloud.ir/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

with open(DOMAINS_FILE) as file:
    domains = [line.rstrip() for line in file]

for domain_name in domains:
    url = f'{BASE_URL}/{domain_name}/dns-records?page=1&per_page=25'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f'request to get records for {domain_name} failed, status_code: {response.status_code}')
        continue
    print(f'trying to update {domain_name} dns records')
    for dns in response.json()['data']:
        try:
            if dns['type'] == 'a':
                if dns['value'][0]['ip'] == OLD_IP:
                    data = {
                        'type': 'A', 
                        'name': dns["name"], 
                        'cloud': True, 
                        'value': [{'ip': NEW_IP, 'port': PORT, 'weight': 100, 'country': ''}], 
                        'upstream_https': 'http', 
                        'ip_filter_mode': {'count': 'single', 'order': 'none', 'geo_filter': 'none'},
                        'id': dns["id"], 
                        'ttl': 120
                    }
                    retry = 0
                    while retry < 3:
                        url = f'{BASE_URL}/{domain_name}/dns-records/{dns["id"]}/'
                        response = requests.put(url, headers=headers, data=json.dumps(data))
                        if response.status_code == 200:
                            print(response.text)
                            print(f'DNS for {domain_name} updated')
                            RECORDS += 1
                            break
                        else:
                            print(f'DNS for {domain_name} faild to update, retry {retry + 1}')
                            print('plase wait 10 seconds')
                            time.sleep(SLEEP_TIME)
                            retry += 1
        except Exception as e:
            print(f'DNS for {domain_name} faild to update')
            print(f'Error : {e}')
            RECORDS += 1
        
print(f'All done, {RECORDS} records from {len(domains)} domains updated')