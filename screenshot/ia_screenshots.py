'''
search: http://web.archive.org/screenshot/https://www.usatoday.com/

image: https://web.archive.org/web/20230222123031if_/http://web.archive.org/screenshot/https://www.usatoday.com/

uri: https://web.archive.org/web/20230222123031/http://web.archive.org/screenshot/https://www.usatoday.com/

https://web.archive.org/web/20230000000000*/http://web.archive.org/screenshot/https://www.usatoday.com/
'''

import requests
import shutil
import internetarchive
from itertools import islice

search = internetarchive.search_items('webcap')

slice = islice(search, 0, 10)

for result in slice:
    print(result['identifier'])