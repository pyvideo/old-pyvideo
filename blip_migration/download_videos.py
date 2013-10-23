import os
import re
import sys
import time

try:
    import blessings
    import requests
except ImportError:
    print 'You need to install requests and blessings.'
    print 'Create a virtual environment, then do:'
    print ''
    print '    pip install requests blessings'
    print ''
    print 'Then rerun this.'
    sys.exit(1)


TERM = blessings.Terminal()
POSSIBLE_ENDINGS = ('.mp4', '.ogv', '.flv')
TSV = 'blip_videos.tsv'


def load_data():
    """Loads data and returns cat title -> list of videos map"""
    categories = {}

    # Sorry: This is lazy file reading.
    f = open(TSV, 'r')
    for line in f.readlines()[1:]:
        line = line.strip()

        if not line or line.startswith(('id', '#')):
            continue

        # It's tab-delimited, so split on tabs.
        line = line.split('\t')
        categories.setdefault(line[1], []).append(line)

    return categories


def slugify(text):
    """Slugifies a string for filename purposes"""
    # Sorry: This is really goofy, but it was really easy to write and
    # "good enough".
    text = ''.join([c if c.isalnum() else '-' for c in text.lower()])

    while '--' in text:
        text = text.replace('--', '-')

    text = text.strip('-')

    return text


def format_downloaded(sofar, total):
    return '{0:.2f}m ({1:0.2f}%)'.format(
        sofar / 1000000.0, sofar * 1.0 / total * 100)


def download_video(url, fn):
    """Downloads a video at or near url to filename"""
    # Sorry: This is terrible code, but I'm kind of throwing it
    # together as I discover more about it.
    print '   Downloading {0} to {1}'.format(url, fn)

    resp = requests.get(url)
    if resp.status_code != 200:
        print '   GAH! MY EYES! {0} kicked up {1}'.format(url, resp.status_code)
        return

    rss_url_m = re.search(r'"(/rss/flash/\d+)"', resp.content)
    rss_url = 'http://blip.tv' + rss_url_m.group(0).strip('"')
    resp = requests.get(rss_url)

    rss_content = resp.content

    for ending in POSSIBLE_ENDINGS:
        regex = r'"http://blip.tv[^"]+?' + ending + '"'

        download_m = re.search(regex, rss_content)
        if not download_m:
            print '   No {0} url found'.format(ending)
            continue

        download_url = download_m.group(0).strip('"')
        print '   Attempting to download {0}'.format(download_url)

        try:
            resp = requests.get(download_url, stream=True)
            print '      Downloading {0}'.format(download_url)
            if resp.status_code == 200:
                total_length = int(resp.headers['content-length'])
                with open(fn + ending, 'w') as fp:
                    total_downloaded = 0

                    tic_chunk = total_downloaded
                    tic = time.time()
                    for chunk in resp.iter_content(chunk_size=1024):
                        if chunk:
                            fp.write(chunk)
                            fp.flush()
                            tic_chunk += len(chunk)
                            total_downloaded += len(chunk)

                            if time.time() - tic > 1:
                                with TERM.location(x=0):
                                    line = '      {0} {1}kbps'.format(
                                        format_downloaded(total_downloaded, total_length),
                                        int(tic_chunk / (time.time() - tic) / 1000))
                                    sys.stdout.write(line + TERM.clear_eol)
                                    sys.stdout.flush()
                                tic_chunk = 0
                                tic = time.time()
                    print ''

                print '   Done! {0}'.format(fn + ending)
                return

            else:
                print '   HTTP{0}! GAH! SPUTTER!'.format(resp.status_code)

        except requests.exceptions.ConnectionError as exc:
            print '   CONNECTIONERROR! GAH! SPUTTER! {0}'.format(exc)

    print '   SO MANY FAILURES!'


def get_existing_file_ids():
    files = [fn for fn in os.listdir('.') if fn.endswith(POSSIBLE_ENDINGS)]
    return [fn.split('_')[0] for fn in files]


def download_videos(data, category):
    """Downloads all the videos in data[category]"""
    file_ids = get_existing_file_ids()

    for line in data[category]:
        print ''
        print 'Working on {0} - {1}'.format(line[0], line[2])

        if line[0] in file_ids:
            print '   Skipping -- already got it'
            continue

        fn = '{0}_{1}'.format(line[0], slugify(line[2]))
        download_video(line[3], fn)

    return 0


def main(argv):
    data = load_data()

    if not argv or argv[0] not in data:
        print 'Available categories:'
        for cat in data.keys():
            print '-', cat
        return 0

    return download_videos(data, argv[0])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
