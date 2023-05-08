import requests
import json
import time
import argparse

BASE_URL = f'https://napi.arvancloud.ir/cdn/4.0/domains'
RECORDS = 0


parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument('--email', required=True, help='your email address')
parser.add_argument('--password', required=True, help='your password')
parser.add_argument('--old_ip', required=True, help='your old ip')
parser.add_argument('--new_ip', required=True, help='your new ip')
parser.add_argument('--domains_file', required=True, help='file with domains')
parser.add_argument('--sleep_time', required=False, default=10, help='sleep time between requests')
parser.add_argument('--port', required=False, default=8080, help='sleep time between requests')

args = parser.parse_args()

EMAIL = args.email
PASSWORD = args.password
OLD_IP = args.old_ip
NEW_IP = args.new_ip
SLEEP_TIME = int(args.sleep_time)
DOMAINS_FILE = args.domains_file
PORT = args.port

headers = {
    'authority': 'dejban.arvancloud.ir',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'fa',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://accounts.arvancloud.ir',
    'referer': 'https://accounts.arvancloud.ir/',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'x-content-type-options': 'nosniff',
    'x-frame-options': 'DENY',
    'x-redirect-uri': 'https://panel.arvancloud.ir'
}

login_url = "https://dejban.arvancloud.ir/v1/auth/login"
login_data = {
    "email": EMAIL,
    "password": PASSWORD,
    "captcha": "v3.undefined"
}
response = requests.post(login_url, data=json.dumps(login_data), headers=headers)
if response.status_code != 200:
    print(f'login failed, status_code: {response.status_code}, {response.text}')
    exit()
response = response.json()
BEARER_TOKEN = f'{response["data"]["accessToken"]}.{response["data"]["defaultAccount"]}'


headers = {
        'authority': 'napi.arvancloud.ir',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'fa',
        'authorization': f'Bearer {BEARER_TOKEN}',
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




