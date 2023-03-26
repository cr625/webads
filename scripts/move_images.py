import shutil
import os
import copy

log = open('/home/cr625/webads/output/warc-images.log')
images = []
for line in log:
    if "[Errno 36]" in line:
        print('file name too long')
    else:
        path = line.split('INFO:root:')
        path = path[1].strip()
        
        try:
        
            shutil.copy(path, '/home/cr625/webads/html/' + path.replace('/','_'))
        except:
            print('file not found')
        print(path)
            