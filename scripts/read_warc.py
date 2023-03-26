import re
from warcio.archiveiterator import ArchiveIterator
from warcio import WARCWriter
from itertools import islice


path_to_warc = "/home/cr625/webads/crawl-data/CC-MAIN-2017-13/segments/1490218186353.38/warc/CC-MAIN-20170322212946-00000-ip-10-233-31-227.ec2.internal.warc.gz"

warc_file = open(path_to_warc, 'rb')
records = ArchiveIterator(warc_file, arc2warc=True)


log = open('/home/cr625/webads/output/warc-images.log')
images = []
for line in log:
    path = line.split('/')
    image_file = (path[-1].strip())

    images.append(image_file)
   
   


file_no = 0

for record in records:
    if record.rec_type == 'response':
        if record.http_headers.get_header('Content-Type') == 'text/html':
            contents = record.content_stream().read()
            for image in images:
                if image == '.jpg' or image =='1.jpg':
                    break                            
                re_image = re.compile(image.encode('ASCII'))
                if re_image.search(contents):
                    print('img record found')
                    
                    print(record.rec_headers.get_header('WARC-Target-URI'))
                    file_no += 1
                    file_name = 'html/test' + str(file_no) + '.html'                      
                    f = open(file_name, 'wb')   
                    
                    f.write(contents)
                    f.close()