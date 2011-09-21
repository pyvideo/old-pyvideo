#!/usr/bin/python

# Copyright (c) 2011 Will Kahn-Greene <willg@bluesock.org>
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This is a script that gets the enclosure video urls for all videos in
a category on PMC.
"""

import sys
import httplib
from urlparse import urlparse

# requirements not in the stdlib
try:
    from lxml import etree
except:
    print "Requires lxml.  Please install and re-run."
    sys.exit(1)

USAGE = "usage: geturls.py <category>"

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

def get_urls_atom(root):
    global total_not_valid

    entries = root.findall("{http://www.w3.org/2005/Atom}entry")
    urls = []

    for i, entry in enumerate(entries):
        link = entry.find("{http://www.w3.org/2005/Atom}link[@rel=\"enclosure\"]")
        urls.append(link.attrib["href"])

    print "\n".join(urls)
    return 0

def get_urls(data):
    root = etree.XML(data)
    if "Atom" in root.tag:
        return get_urls_atom(root)

    raise ValueError("Don't know how to handle feed of %s", root.tag)

def main(argv):
    if not argv:
        print USAGE
        return 1

    category = argv[0]
    category = category.lower().replace(" ", "-")
    url = "http://python.mirocommunity.org/feeds/category/%s?count=1000" % category
    return get_urls(get_feed(url))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
