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
Given a PMC category, this goes through, extracts the video urls, and
pings Universal Subtitles to find out the subtitle status.

Then it outputs all that in a .csv file sorted by transcribed status.
"""

import sys
import urllib2
import os
import json
import csv

USAGE = "Usage: check_usubs.py file-of-video-urls"

def get_usub_stats(url):
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler())
    try:
        resp = opener.open("http://www.universalsubtitles.org/api/1.0/subtitles/languages/?video_url=%s" % url)
    except urllib2.URLError, e:
        print "Error: %s %s" % (url, e)
        return []
    return json.loads(resp.read())


def parse_completed(s):
    if s == u"100 %":
        return 1000000
    return int(s.split(" ")[0])


def main(argv):
    if not argv:
        print USAGE
        return 1

    path = os.path.normpath(os.path.expanduser(argv[0]))
    if not os.path.exists(path):
        print USAGE
        print "File %s does not exist" % argv[0]
        return 1

    print "Working on %s" % path
    urls = open(path, "r").readlines()
    writer = csv.writer(open(path + ".csv", "wb"))

    rows = []

    for url in urls:
        usub_stats = [(s["id"], s["name"], s["completion"])
                      for s in get_usub_stats(url)]
        usub_stats.sort(key=lambda s: parse_completed(s[2]))
        usub_stats.reverse()
        row = [url.strip()]
        row.extend(usub_stats)
        rows.append(row)

    rows.sort(key=lambda r: len(r) > 1 and parse_completed(r[1][2]) or 0)
    rows.reverse()

    for row in rows:
        writer.writerow(row)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
