from io import BytesIO
import boto3
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

CRAWL = "CC-MAIN-2022-40"

def html_to_text(page, record):
    try:
        encoding = record.rec_headers["WARC-Identified-Content-Charset"]
        if not encoding:
            for encoding in EncodingDetector(page, is_html=True).encodings:
                # take the first detected encoding
                break
        soup = BeautifulSoup(page, "lxml", from_encoding=encoding)
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text(" ", strip=True)
    except Exception as e:
        return ""


s3client = boto3.client("s3")
url = "https://www.usatoday.com/"
warc_path = "crawl-data/CC-MAIN-2022-40/segments/1664030333541.98/warc/CC-MAIN-20220924213650-20220925003650-00631.warc.gz"
offset = 1124184665
length = 64704
rangereq = "bytes=" + str(offset) + "-" + str(offset + length - 1)
response = s3client.get_object(Bucket="commoncrawl", Key=warc_path, Range=rangereq)
record_stream = BytesIO(response["Body"].read())
for record in ArchiveIterator(record_stream):
    page = record.content_stream().read()
    print(page)