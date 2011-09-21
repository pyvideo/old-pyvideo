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
This is a script that given an MC feed goes through all the items
in the feed and verifies that the item's enclosure url exists at
blip.tv.

If the enclosure url kicks up a 404, then this finds the correct
enclosure url and spits it out to stdout.
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

USAGE = "usage: check_enclosures.py <url-to-feed>"

total_not_valid = 0

def get_link_by_type(links, link_type):
    theone = [link for link in links
              if link.attrib["rel"] == link_type]
    if not theone:
        return None
    return theone[0]

def get_valid_blip_url(blip_id):
    conn = httplib.HTTPConnection("blip.tv")
    conn.request("GET", "/file/%s?skin=rss" % blip_id)
    resp = conn.getresponse()
    if resp.status is not 200:
        print "Bad url?: Error: status: %s reason: %s" % (resp.status, resp.reason)
        return None

    data = resp.read()
    enclosure = [line for line in data.splitlines() if "enclosure" in line]
    if enclosure:
        data = enclosure[0]
        data = data[data.find("url=")+5:]
        data = data[:data.find("\"")].strip()
        return data                    

    ffvorbis = [line for line in data.splitlines() if "ffvorbis" in line]
    if ffvorbis:
        data = ffvorbis[0]
        data = data[data.find("url=")+5:]
        data = data[:data.find("\"")].strip()
        return data

    print data
    raise ValueError("No ffvorbis option.")

def is_url_valid(url):
    parsed = urlparse(url)
    conn = httplib.HTTPConnection(parsed.hostname, parsed.port)
    conn.request("HEAD", parsed.path)
    resp = conn.getresponse()
    if resp.status == 200:
        return True
    if resp.status in (301, 302, 303):
        location = resp.getheader("Location", "")
        if location:
            print "Redirecting to %s..." % location
            return is_url_valid(location)
        print resp.getheaders()
        print resp.msg

    print "Bad url?: Error: status: %s reason: %s" % (resp.status, resp.reason)
    return False

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

def test_links_atom(root):
    global total_not_valid
    output = csv.writer(open('output.csv', 'wb'))

    entries = root.findall("{http://www.w3.org/2005/Atom}entry")
    print "Total number of entries: %s" % len(entries)
    for i, entry in enumerate(entries):
        print ""
        title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()
        print "%d/%d: Working on %s..." % (i, len(entries), title)

        links = entry.findall("{http://www.w3.org/2005/Atom}link")
        url = get_link_by_type(links, "alternate")
        if url is None:
            print "no urls?"
            continue
        url = url.attrib["href"]
        print "URL: %s" % url

        enc = get_link_by_type(links, "enclosure")
        if enc is None:
            print "error: no enclosures"
            continue
        enc = enc.attrib["href"]
        print "Link is: %s" % enc
        valid = is_url_valid(enc)
        print "Valid?: %s" % valid
        if not valid:
            total_not_valid += 1
            via = get_link_by_type(links, "via")
            if via is not None and "blip.tv" in via.attrib["href"]:
                via = via.attrib["href"]
                blip_id = via.split("/")[-1]
                newlink = get_valid_blip_url(blip_id)
                if newlink:
                    output.writerow((title, url, enc, newlink))
                    print "Working url: %s" % newlink
                else:
                    output.writerow((title, url, enc))
            else:
                output.writerow((title, url, enc))
 
            foo = raw_input("Fix it?")

    print ""
    print "Total number of entries: %s" % len(entries)
    print "Total invalid entries: %d" % total_not_valid


def test_links(data):
    root = etree.XML(data)
    if "Atom" in root.tag:
        return test_links_atom(root)

    raise ValueError("Don't know how to handle feed of %s", root.tag)

def main(argv):
    if not argv:
        print USAGE
        return 1

    url = argv[0]
    return test_links(get_feed(url))

if __name__ == "__main__":
    main(sys.argv[1:])
