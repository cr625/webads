from warcio.archiveiterator import ArchiveIterator, WARCIterator
from warcio.warcwriter import WARCWriter
from warcio import extractor
import re

path_to_warc = "/home/chris/webarchives/collections/captures/archive/rec-20221113140013260112-CBR-ZenBook.warc.gz"

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

html_tag_pattern = re.compile(b'iframe', re.IGNORECASE)


def process_record(record):
    if record.rec_type == "response":
        if record.http_headers.get_header("Content-Type") == "text/html":
            return record.content_stream().read()


with open(path_to_warc, "rb") as stream:
    for record in WARCIterator(stream):
        print(record.format)
        print(record.rec_type)
        print(record.rec_headers)
        print(record.http_headers)
        print(record.content_type)
        print(record.length)
        # print(record.content_stream().read())

        
# go through the warcs and find iframes. Create links through wayback pyweb
# make a list of 100 websites and check them for ads on the wayback machine
# look for ad archives
# check existing collection (Zenodo).0
'''
def run():
    with open(warc_path, 'rb') as stream:
        archive_iterator = ArchiveIterator(stream, arc2warc=True)        
        
        records = islice(archive_iterator, 0, 10)        
        #records = random.sample(list(archive_iterator), 10)
        file_no = 0
        for record in records:
            if record.rec_type == 'response':                
                if is_html(record):
                    print('HTML record found')
                    
                    file_no += 1
                    file_name = 'test' + str(file_no) + '.warc'   
                    f = open(file_name, 'wb')         
                    writer = WARCWriter(f, gzip=False)
                    writer.write_record(record)
                    f.close()        


if __name__ == '__main__':
    run()
'''