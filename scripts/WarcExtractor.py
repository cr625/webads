from warcio.archiveiterator import ArchiveIterator
import boto3
from io import BytesIO
import requests
import json

default_collection = "CC-MAIN-2022-40"

class WarcExtractor(object):
    """
    Extracts WARC records from a warc.gz file."""
    
    def __init__(self, target_url):
        self.s3client = boto3.client('s3')
        self.target_url = target_url
        self.collection = default_collection

    def get_index(self):
        cdx_server = "https://index.commoncrawl.org/{collection}-index?url={url}&matchType=domain&output=json"
        cdx_response = requests.get(cdx_server.format(collection=self.collection, url=self.target_url)).content.splitlines()
        return [json.loads(line) for line in cdx_response]
        

    
    def get_record(self, offset, length, warc_file):
        rangereq = "bytes=" + str(offset) + "-" + str(offset + length - 1)
        response = self.s3client.get_object(Bucket="commoncrawl", Key=warc_file, Range=rangereq)
        record_stream = BytesIO(response["Body"].read())
        archive_iterator = ArchiveIterator(record_stream)        
        for record in archive_iterator:
            page = record.content_stream().read()            
            yield page

if __name__ == "__main__":

    we = WarcExtractor('https://www.usatoday.com/')
    index = we.get_index()

    for entry in index:
        print(entry['offset'], entry['length'], entry['filename'])


    
    