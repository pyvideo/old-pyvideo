import sys
import json
import datetime
import itertools
import traceback

import requests
import vidscraper

from videos.models import create_videos, Video, Speaker
from django.core import serializers


URL = 'http://veyepar.nextdayvideo.com:8081/main/C/psf/S/pycon_2012.json'


def get_pycon_data():
    r = requests.get(URL)
    r.raise_for_status()

    data = r.text
    return json.loads(data)


CARL_TO_RICHARD = {
    'host_url': 'source_url',
    'name': 'title',
    'license': 'copyright_text'
    }


def get_data_from_youtube(url):
    video = vidscraper.auto_scrape(url)
    return {
        'thumbnail_url': video['thumbnail_url'],
        'embed': video['embed']
        }


def import_video(data):
    print 'Working on %s...' % data['name']
    new_data = {
        'state': 1,  # live
        'category': 17,
        'title': data['name'],
        'summary': '<p>%s</p>' % data['description'],
        'source_url': data['host_url'],
        'copyright_text': data['license'],
        'speakers': data['authors'].split(','),
        'recorded': datetime.datetime.strptime(data['start'],
                                               '%Y-%m-%d %H:%M:%S'),
        'added': datetime.datetime.now()
        }

    new_data.update(get_data_from_youtube(data['host_url']))

    try:
        return create_videos([new_data])
    except Exception, e:
        print "".join(traceback.format_exc())
        print "Probably a new source_url: %s" % data['host_url']
        print ""


def oh_right_round_trip_that_please():
    videos = Video.objects.filter(category_id=17)
    data = serializers.serialize('json', videos, indent=2)
    f = open('fixtures/pycon-2012.json', 'w')
    f.write(data)
    f.close()

    speakers = Speaker.objects.all()
    data = serializers.serialize('json', speakers, indent=2)
    f = open('fixtures/speakers.json', 'w')
    f.write(data)
    f.close()


def absorb_pycon_data():
    print datetime.datetime.now()
    json_data = get_pycon_data()

    results = [import_video(mem['fields']) for mem in json_data
               if mem['fields'].get('host_url')]

    for mem in itertools.chain.from_iterable(results):
        if mem:
            print 'Added %s' % mem.title

    oh_right_round_trip_that_please()
    return 0


def main(argv):
    return absorb_pycon_data()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
