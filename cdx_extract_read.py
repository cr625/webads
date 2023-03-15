from warcio.archiveiterator import ArchiveIterator, WARCIterator
from warcio.warcwriter import WARCWriter

path_to_warc = '/home/cr625/webads/2mdn-INTERNETARCHIVE-000000.extracted.warc.gz'

with open(path_to_warc, 'rb') as stream:
    records = ArchiveIterator(stream, arc2warc=True)
    for record in records:
        target_uri = record.rec_headers.get_header('WARC-Source-URI')
        print(target_uri)
        