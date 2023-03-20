from warcio.archiveiterator import ArchiveIterator, WARCIterator
from warcio.warcwriter import WARCWriter

path_to_warc = '/home/cr625/webads/2mdn-INTERNETARCHIVE-000001.extracted.warc.gz'

with open(path_to_warc, 'rb') as stream:
    records = ArchiveIterator(stream, arc2warc=True)
    for record in records:
        warc_headers = record.rec_headers
        http_headers = record.http_headers
        print("WARC headers:")
        print(warc_headers)
        
        print("HTTP headers:")
        print(http_headers)
        print("-----------------")