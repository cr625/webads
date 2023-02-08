from warcio.archiveiterator import ArchiveIterator, WARCIterator
from warcio.warcwriter import WARCWriter
from warcio import extractor
import re
from itertools import islice
from urllib.parse import urlparse
from pathlib import Path
import sys
import logging

path_to_warc = "/home/chris/webads/crawl-data/CC-MAIN-2015-48/segments/1448398444047.40/warc/CC-MAIN-20151124205404-00000-ip-10-71-132-137.ec2.internal.warc.gz"

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

def get_path(url):
    uri = urlparse(url)
    return Path(uri.netloc + uri.path + uri.query)

def main():
    logging.basicConfig(filename="wacz-images.log", level=logging.INFO)
    with open(path_to_warc, 'rb') as stream:        
        archive_iterator = ArchiveIterator(stream, arc2warc=True)        
        records = islice(archive_iterator, 0, 1000)        
        for record in records:
            extract(record)
                
           
def extract(rec):
    if rec.rec_type == "response" and rec.http_headers.get("Content-Type", "").startswith("image/jpeg"):
        path = get_path(rec.rec_headers["WARC-Target-URI"])
        if not path.parent.is_dir():
            path.parent.mkdir(parents=True)
        try:
            logging.info(path)
            path.open('wb').write(rec.content_stream().read())
        except OSError as e:
            logging.error(e)

def get_path(url):
    uri = urlparse(url)
    return Path(uri.netloc + uri.path + uri.query)

if __name__ == '__main__':
    main()
