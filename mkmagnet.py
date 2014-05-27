"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

"""

import argparse
import base64
import bencode
import hashlib
import sys
import urllib

from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Path to torrent file')

    parser.add_argument('-q', '--quiet', action='store_true', help='Be quiet')
    parser.add_argument('--base32', action='store_true',
                        help=('Use base32 instead of hex digest '
                              '(for compatibility with old clients)'))
    return parser.parse_args()


def link(metadata, use_base32=False, log=lambda x: x):

    log('Comment:\t%s' % metadata.get('comment', ''))

    created_by = metadata.get('created by')
    if created_by:
        log('Created by:\t%s' % created_by)

    created_date = metadata.get('creation date')
    if created_date:
        created_date = datetime.fromtimestamp(created_date)
        log('Created:\t%s' % datetime.strftime(created_date, '%x %X'))

    params = [('dn', metadata['info']['name'])]

    for announce_list in metadata.get(
            'announce-list',
            [[metadata['announce']]] if 'announce' in metadata else []):
        for announce in announce_list:
            log('Announce:\t%s' % announce)
            params.append(('tr', announce))

    url_list = metadata.get('url-list', [])
    if isinstance(url_list, basestring):
        url_list = [url_list]

    for url in url_list:
        log('Web Seed:\t%s' % url)
        params.append(('ws', url))

    hashcontents = bencode.bencode(metadata['info'])
    sha1 = hashlib.sha1(hashcontents)

    if use_base32:
        hashstr = base64.b32encode(sha1.digest())
    else:
        hashstr = sha1.hexdigest()

    return 'magnet:?xt=urn:btih:%s&%s' % (hashstr, urllib.urlencode(params))


def main():
    args = parse_args()
    with open(args.file, 'r') as f:
        torrent = f.read()
    metadata = bencode.bdecode(torrent)
    if args.quiet:
        def log(_text):
            pass
    else:
        def log(text):
            sys.stderr.write(text)
            sys.stderr.write('\n')
    print link(metadata, use_base32=args.base32, log=log)


if __name__ == '__main__':
    main()
