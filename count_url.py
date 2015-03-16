#!/usr/bin/python
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import URLError
import sys
import operator

def famous_url(urls):
    url_count = {}
    for url in urls:
        url_count[url] = url_count.get(url, 0) + 1

    sorted_urls = sorted(url_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_urls[0][0]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python2.6 famous_url.py <url>")
        sys.exit(-1)

    remote_url = sys.argv[1]
    #server_log = "server_log.txt"
    #urllib.urlretrieve(remote_url, server_log)
    #urls = [url.strip() for url in open(server_log).readlines()]
    req = Request(remote_url)
    try:
        response = urlopen(req)
    except URLError as e:
        print(e)
        sys.exit(-1)
    else:
        page = response.read()
        page = str(page.strip())
        urls = page.split("\\n")
        if len(urls) < 1:
            sys.exit(-1)

        print(famous_url(urls))
