from warcio.archiveiterator import ArchiveIterator, WARCIterator

warc_file = '/home/cr625/webads/2mdn_simgad-INTERNETARCHIVE-000000.extracted.warc.gz'

with open(warc_file, 'rb') as stream:
    records = ArchiveIterator(stream, arc2warc=True)

    for record in records:

        #        print(record.format)
        #        print(record.rec_type)
        #        print(record.rec_headers)
        print(record.http_headers)

        # print(http_headers)
