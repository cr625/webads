from warcio.archiveiterator import ArchiveIterator, WARCIterator
from warcio.warcwriter import WARCWriter
from warcio import extractor
import re
from itertools import islice

path_to_warc = "/home/cr625/webads/crawl-data/CC-MAIN-2017-13/segments/1490218186353.38/warc/CC-MAIN-20170322212946-00000-ip-10-233-31-227.ec2.internal.warc.gz"

def is_html(record):
        """Return true if (detected) MIME type of a record is HTML"""
        html_types = ['text/html', 'application/xhtml+xml']
        if (('WARC-Identified-Payload-Type' in record.rec_headers) and
            (record.rec_headers['WARC-Identified-Payload-Type'] in
             html_types)):
            return True
        content_type = record.http_headers.get_header('content-type', None)
        if content_type:
            for html_type in html_types:
                if html_type in content_type:
                    return True
        return False

html_tag_pattern = re.compile(b'cdn.shopify.com', re.IGNORECASE)


def process_record(record):
    if record.rec_type == "response":
        if record.http_headers.get_header("Content-Type") == "text/html":
            return record.content_stream().read()

'''
with open(path_to_warc, "rb") as stream:
    for record in WARCIterator(stream):
        print(record.format)
        print(record.rec_type)
        print(record.rec_headers)
        print(record.http_headers)
        print(record.content_type)
        print(record.length)
        # print(record.content_stream().read())
'''
        
# go through the warcs and find iframes. Create links through wayback pyweb
# make a list of 100 websites and check them for ads on the wayback machine
# look for ad archives
# check existing collection (Zenodo).0

def run():
    with open(path_to_warc, 'rb') as stream:
        archive_iterator = ArchiveIterator(stream, arc2warc=True)        
        
        records = archive_iterator
        #records = random.sample(list(archive_iterator), 100)
        file_no = 0
        for record in records:
            if record.rec_type == 'response':                
                if is_html(record):
                    print('HTML record found')
                    contents = record.content_stream().read()
                    if contents.findall(html_tag_pattern):
                        file_no += 1
                        file_name = 'output/test' + str(file_no) + '.warc'   
                        f = open(file_name, 'wb')         
                        writer = WARCWriter(f, gzip=False)
                        writer.write_record(record, contents)
                        f.write(contents)
                        f.close()
                    


if __name__ == '__main__':
    run()
