#!/usr/bin/python

"""
This is a script that gets the titles for all videos in a category on
PMC.
"""

import sys
import httplib
from urlparse import urlparse
import csv

# requirements not in the stdlib
try:
    from lxml import etree
except:
    print "Requires lxml.  Please install and re-run."
    sys.exit(1)

USAGE = "usage: gettitles.py <category>"

def get_feed(url):
    parsed = urlparse(url)
    conn = httplib.HTTPConnection(parsed.hostname, parsed.port)
    if parsed.query:
        path = parsed.path + "?" + parsed.query
    else:
        path = parsed.path
    conn.request("GET", path)
    resp = conn.getresponse()
    if resp.status != 200:
        raise ValueError("Bad url?: Error: status: %s reason: %s",
                         resp.status, resp.reason)
        
    return resp.read()

def get_titles_atom(root):
    global total_not_valid

    entries = root.findall("{http://www.w3.org/2005/Atom}entry")
    print "Total number of entries: %s" % len(entries)
    titles = []

    for i, entry in enumerate(entries):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()
        titles.append(title)

    titles.sort()
    print "\n".join(titles)
    return 0

def get_titles(data):
    root = etree.XML(data)
    if "Atom" in root.tag:
        return get_titles_atom(root)

    raise ValueError("Don't know how to handle feed of %s", root.tag)

def main(argv):
    if not argv:
        print USAGE
        return 1

    category = argv[0]
    category = category.lower().replace(" ", "-")
    url = "http://python.mirocommunity.org/feeds/category/%s?count=1000" % category
    return get_titles(get_feed(url))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
