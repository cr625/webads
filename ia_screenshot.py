'https://web.archive.org/web/timemap/screenshot/https://www.cnn.com/'

import requests
import shutil

with open('forbes_timemap.txt', 'r') as f:
    for line in f:
        url = line.split(' ')[2].strip('"",')
        file_name = url[28:42] + '.png'
        print(file_name)
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open('screenshots/forbes/' + file_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
