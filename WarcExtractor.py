from warcio.archiveiterator import ArchiveIterator
import boto3
from io import BytesIO

class WarcExtractor(object):
    """
    Extracts WARC records from a warc.gz file."""
    
    def __init__(self):
        self.s3client = boto3.client('s3')

    
    def get_record(self, offset, length, warc_file):
        rangereq = "bytes=" + str(offset) + "-" + str(offset + length - 1)
        response = self.s3client.get_object(Bucket="commoncrawl", Key=warc_file, Range=rangereq)
        record_stream = BytesIO(response["Body"].read())
        archive_iterator = ArchiveIterator(record_stream)        
        for record in archive_iterator:
            page = record.content_stream().read()            
            yield page

offset = 1124184665
length = 64704
url = "https://www.usatoday.com/"
warc_file = "crawl-data/CC-MAIN-2022-40/segments/1664030333541.98/warc/CC-MAIN-20220924213650-20220925003650-00631.warc.gz"


we = WarcExtractor()
pages = we.get_record(offset, length, warc_file)
for page in pages:
    print(page)
