#!/usr/bin/env python

import cdx_toolkit

cdx = cdx_toolkit.CDXFetcher(source='ia')
#url = 's0.2mdn.net/sadbundle/*'
#url = 's0.2mdn.net/simgad/*'
#url = 's0.2mdn.net/ads/*'
url = 'aax-us-east.amazon-adsystem.com/e/*'
warcinfo = {
    'software': 'pypi_cdx_toolkit webads',
    'isPartOf': 'aax-us-east-amazon-INTERNETARCHIVE',
    'description': 'warc extraction',
    'format': 'WARC file version 1.0',
}

writer = cdx_toolkit.warc.get_writer('aax-us-east-amazon', 'INTERNETARCHIVE', warcinfo, warc_version='1.1')

for obj in cdx.iter(url, limit=100):
    url = obj['url']
    status = obj['status']
    timestamp = obj['timestamp']

    print('considering extracting url', url, 'timestamp', timestamp)
    if status != '200':
        print(' skipping because status was {}, not 200'.format(status))
        continue

    try:
        record = obj.fetch_warc_record()
    except RuntimeError:
        print(' skipping capture for RuntimeError 404: %s %s', url, timestamp)
        continue
    writer.write_record(record)

    print(' wrote', url)