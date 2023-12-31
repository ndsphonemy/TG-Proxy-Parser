import requests
import threading
import json
import os 
import time
import random
import re
import base64
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

requests.post = lambda url, **kwargs: requests.request(
    method="POST", url=url, verify=False, **kwargs
)
requests.get = lambda url, **kwargs: requests.request(
    method="GET", url=url, verify=False, **kwargs
)

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

os.system('cls' if os.name == 'nt' else 'clear')

if not os.path.exists('config-tg.txt'):
    with open('config-tg.txt', 'w'): pass

thrd_pars = int(input('Threads for parsing: '))
print()

start_time = datetime.now()

sem_pars = threading.Semaphore(thrd_pars)

def json_load(path):
    with open(path, 'r', encoding="utf-8") as file:
        list_content = json.load(file)
    return list_content

tg_name_json = json_load('telegram channels.json')

config_all = list()
tg_name = list()
new_tg_name_json = list()

print(f'Try get new tg channels name from proxy configs in config-tg.txt...')

with open("config-tg.txt", "r", encoding="utf-8") as config_all_file:
    config_all=config_all_file.readlines()

pattern_telegram_user = r'(?:@)(\w{5,})|(?:%40)(\w{5,})'

for config in config_all:
    if config.startswith('vmess://'):
        try:
            config=base64.b64decode(config[8:]).decode("utf-8")
        except:
            pass
    if config.startswith('ssr://'):
        try:
            config=base64.b64decode(config[6:]).decode("utf-8")
        except:
            pass
    matches_usersname = re.findall(pattern_telegram_user, config, re.IGNORECASE)
    try:
        matches_usersname = re.findall(pattern_telegram_user, base64.b64decode(config).decode("utf-8"), re.IGNORECASE)
    except:
        pass
    
    for index, element in enumerate(matches_usersname):
        if element[0]!='':
            tg_name.append(element[0].lower().encode('ascii', 'ignore').decode())
        if element[1]!='':
            tg_name.append(element[1].lower().encode('ascii', 'ignore').decode()) 

tg_name[:] = [x for x in tg_name if len(x) >= 5]
tg_name_json[:] = [x for x in tg_name_json if len(x) >= 5]    
tg_name=list(set(tg_name))
print(f'\nFound tg channel names - {len(tg_name)}')
print(f'Total old names        - {len(tg_name_json)}')
tg_name_json.extend(tg_name)
tg_name_json=list(set(tg_name_json))
tg_name_json=sorted(tg_name_json)
print(f'In the end, new names  - {len(tg_name_json)}')

with open('telegram channels.json', 'w', encoding="utf-8") as telegram_channels_file:
    json.dump(tg_name_json, telegram_channels_file, indent = 4)

print(f'\nSearch for new names is over - {str(datetime.now() - start_time).split(".")[0]}')

print(f'\nStart Parsing...')

def process(i_url):
    sem_pars.acquire()
    html_pages = list()
    while True:
        try:
            response = requests.get(f'https://t.me/s/{i_url}')
        except:
            time.sleep(random.randint(10,30))
            pass
        else:
            print(f'{tg_name_json.index(i_url)+1} of {walen} - {i_url}')
            html_pages.append(response.text)
            for page in html_pages:
                soup = BeautifulSoup(page, 'html.parser')
                code_tags = soup.find_all(class_='tgme_widget_message_text')
                for code_tag in code_tags:
                    code_content2 = str(code_tag).split('<br/>')
                    for code_content in code_content2:
                        if "vless://" in code_content or "ss://" in code_content or "vmess://" in code_content or "trojan://" in code_content or "tuic://" in code_content or "hysteria://" in code_content or "hy2://" in code_content or "hysteria2://" in code_content or "juicity://" in code_content or "nekoray://" in code_content or "socks4://" in code_content or "socks5://" in code_content or "socks://" in code_content or "naive+" in code_content:
                            codes.append(re.sub(htmltag_pattern, '', code_content))
                            new_tg_name_json.append(i_url)
            break
    sem_pars.release()

htmltag_pattern = re.compile(r'<.*?>')

codes = list()

walen = len(tg_name_json)
for url in tg_name_json:
    threading.Thread(target=process, args=(url,)).start()
    
while threading.active_count() > 1:
    time.sleep(1)

print(f'\nParsing completed - {str(datetime.now() - start_time).split(".")[0]}')

print(f'\nStart check and remove duplicate from parsed configs...')

codes = list(set(codes))

processed_codes = list()

for part in codes:
    part = re.sub('amp;', '', part)
    if "vmess://" in part:
        part = f'vmess://{part.split("vmess://")[1]}'
        processed_codes.append(part)
        continue
    elif "vless://" in part:
        part = f'vless://{part.split("vless://")[1]}'
        if "@" in part and ":" in part[8:]:
            processed_codes.append(part)
        continue
    elif "ss://" in part:
        part = f'ss://{part.split("ss://")[1]}'
        processed_codes.append(part)
        continue
    elif "trojan://" in part:
        part = f'trojan://{part.split("trojan://")[1]}'
        if "@" in part and ":" in part[9:]:
            processed_codes.append(part)
        continue
    elif "tuic://" in part:
        part = f'tuic://{part.split("tuic://")[1]}'
        if ":" in part[7:] and "@" in part:
            processed_codes.append(part)
        continue
    elif "hysteria://" in part:
        part = f'hysteria://{part.split("hysteria://")[1]}'
        if ":" in part[11:] and "=" in part:
            processed_codes.append(part)
        continue
    elif "hysteria2://" in part:
        part = f'hysteria2://{part.split("hysteria2://")[1]}'
        if "@" in part and ":" in part[12:]:
            processed_codes.append(part)
        continue
    elif "hy2://" in part:
        part = f'hy2://{part.split("hy2://")[1]}'
        if "@" in part and ":" in part[6:]:
            processed_codes.append(part)
        continue
    elif "juicity://" in part:
        part = f'juicity://{part.split("juicity://")[1]}'
        processed_codes.append(part)
        continue
    elif "nekoray://" in part:
        part = f'nekoray://{part.split("nekoray://")[1]}'
        processed_codes.append(part)
        continue
    elif "socks4://" in part:
        part = f'socks4://{part.split("socks4://")[1]}'
        if ":" in part[9:]:
            processed_codes.append(part)
        continue
    elif "socks5://" in part:
        part = f'socks5://{part.split("socks5://")[1]}'
        if ":" in part[9:]:
            processed_codes.append(part)
        continue
    elif "socks://" in part:
        part = f'socks://{part.split("socks://")[1]}'
        if ":" in part[8:]:
            processed_codes.append(part)
        continue
    elif "naive+" in part:
        part = f'naive+{part.split("naive+")[1]}'
        if ":" in part[13:] and "@" in part:
            processed_codes.append(part)
        continue

print(f'\nTrying to delete corrupted configurations...') 

processed_codes = list(set(processed_codes))
processed_codes = [x for x in processed_codes if (len(x)>13) and (("…" in x and "#" in x) or ("…" not in x))]
processed_codes = sorted(processed_codes)

print(f'\nDelete tg channels that not contains proxy configs...')

new_tg_name_json = list(set(new_tg_name_json))
new_tg_name_json = sorted(new_tg_name_json)

print(f'\nRemaining tg channels after deletion - {len(new_tg_name_json)}')

print(f'\nSave new telegram channels.json and config-tg.txt...')

with open('telegram channels.json', 'w', encoding="utf-8") as telegram_channels_file:
    json.dump(new_tg_name_json, telegram_channels_file, indent = 4)

with open("config-tg.txt", "w", encoding="utf-8") as file:
    for code in processed_codes:
        file.write(code.encode("utf-8").decode("utf-8") + "\n")

print(f'\nTime spent - {str(datetime.now() - start_time).split(".")[0]}')
#print(f'\nTime spent - {timedelta(seconds=int((datetime.now() - start_time).total_seconds()))}')

input('\nPress Enter to finish ...')
