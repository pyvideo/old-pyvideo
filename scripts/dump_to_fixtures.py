import sys
import json
import datetime
import itertools
import traceback

from videos.models import Category, Video, Speaker, Tag
from sitenews.models import SiteNews
from django.core import serializers


def dump_fixtures():
    cats = Category.objects.all()
    for cat in cats:
        videos = Video.objects.filter(category_id=cat.id).order_by('id')
        data = serializers.serialize('json', videos, indent=2)
        f = open('fixtures/%s.json' % cat.slug, 'w')
        f.write(data)
        f.close()

    tags = Tag.objects.order_by('id')
    data = serializers.serialize('json', tags, indent=2)
    f = open('fixtures/tags.json', 'w')
    f.write(data)
    f.close()

    speakers = Speaker.objects.order_by('id')
    data = serializers.serialize('json', speakers, indent=2)
    f = open('fixtures/speakers.json', 'w')
    f.write(data)
    f.close()

    snews = SiteNews.objects.order_by('id')
    data = serializers.serialize('json', snews, indent=2)
    f = open('fixtures/sitenews.json', 'w')
    f.write(data)
    f.close()

    return 0


def main(argv):
    return dump_fixtures()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
