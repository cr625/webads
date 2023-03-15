'https://web.archive.org/web/timemap/screenshot/https://www.cnn.com/'
'https://web.archive.org/web/timemap/cdxj/http://web.archive.org/screenshot/https://www.bbc.com/'
import requests
import shutil
import json 


site = 'aljazeera'
prefix = 'http://web.archive.org/web/'
suffix = '/http://web.archive.org/screenshot/https://www.' + site + '.com/'


with open(site + '.txt', 'r') as f:
    for line in f:
        date_time = line.split(' ')[1]
        file_name = date_time + '.png'
        url = prefix + date_time + suffix        
        print(file_name)
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open('screenshots/' + site + '/' + file_name, 'wb') as g:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, g)
    