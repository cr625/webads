from warcio.archiveiterator import ArchiveIterator, WARCIterator
from warcio.warcwriter import WARCWriter

path_to_warc ='/home/cr625/webads/crawl-data/CC-MAIN-2022-49/segments/1669446706285.92/warc/CC-MAIN-20221126080725-20221126110725-00000.warc.gz'
#path_to_warc = "/home/cr625/webads/crawl-data/CC-MAIN-2017-13/segments/1490218186353.38/warc/CC-MAIN-20170322212946-00000-ip-10-233-31-227.ec2.internal.warc.gz"
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


ad_item = b'data-item-title'

def run():
    file_no = 0
    with open(path_to_warc, 'rb') as stream:
        records = ArchiveIterator(stream, arc2warc=True)        
        
        for record in records:
                if record.rec_type == 'response':                
                    if is_html(record):
                        contents = record.content_stream().read()
                        if contents.find(ad_item) != -1:
                            print('ad server record found')
                            file_no += 1
                            file_name = 'adserver/data-item' + str(file_no) + '.warc'   
                            f = open(file_name, 'wb')         
                            writer = WARCWriter(f, gzip=False)
                            writer.write_record(record, contents)
                            f.write(contents)
                            f.close()
            


if __name__ == '__main__':
    run()

