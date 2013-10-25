import argparse
from collections import defaultdict
import os

try: 
    import pyrax
    from pyrax.exceptions import PyraxException
except ImportError:
    print """
    You need to install pyrax. Create a virutal environment,
    then do:

    pip install pyrax

    Then rerun this.
    """


def upload_files(filenames, container):
    results = defaultdict(dict)
    for filename in filenames:
        results[filename].update({'status': 'processing'})

        print 'Uploading {}'.format(filename)
        try:
            obj = container.upload_file(filename)
        except PyraxException as e:
            print 'Help! PyraxException {} while trying to upload {}. skipping to next file'.format(e, filename)
            results[filename].update({
                'status': 'problem',
                'exception': e,
            })
        results[filename].update({
            'status': 'finished',
            'obj': obj,
        })
        print 'Finished {}'.format(filename)
    return results


def setup_pyrax_environment(credentials='~/.rackspace'):
    pyrax.set_setting("identity_type", "rackspace")
    creds_file = os.path.expanduser(credentials)
    pyrax.set_credential_file(creds_file)
    return pyrax.cloudfiles


def make_parser():
    parser = argparse.ArgumentParser(description="""
        Upload files to the pyvideo cdn container
    """)
    parser.add_argument('files', metavar='N', nargs='*',
        help='files to upload')
    parser.add_argument('--container', default='testing')
    parser.add_argument('--credentials', default='~/.rackspace')
    return parser


if __name__ == '__main__':
    args = make_parser().parse_args()
    cf = setup_pyrax_environment(args.credentials)
    container = cf.get_container(args.container)
    results = upload_files(args.files, container)


"""
notes

[pmc] [sheila@yagi:~/repos/pmc/blip_migration:master(+,)]$ python upload_videos.py testdir/*
Uploading testdir/a.txt
Finished testdir/a.txt
Uploading testdir/b.txt
Finished testdir/b.txt

[pmc] [sheila@yagi:~/repos/pmc/blip_migration:master(+,)]$ python
Python 2.7.4 (default, Sep 26 2013, 03:20:26)
[GCC 4.7.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import upload_videos as up
>>> cf = up.setup_pyrax_environment()
>>> container = cf.get_container('testing')
>>> results = up.upload_files(['testdir/a.txt', 'testdir/b.txt'], container)
Uploading testdir/a.txt
Finished testdir/a.txt
Uploading testdir/b.txt
Finished testdir/b.txt
>>> results
defaultdict(<type 'dict'>, {'testdir/b.txt': {'status': 'finished', 'obj': <Object 'b.txt' (text/plain)>}, 'testdir/a.txt': {'status': 'finished', 'obj': <Object 'a.txt' (text/plain)>}})
>>> a = results['testdir/a.txt']['obj']
>>> a.get_metadata()
{}
>>> a.set_metadata({'X-Object-Meta-Testing':'foo'})
>>> a.get_metadata()
{'x-object-meta-testing': 'foo'}
>>> cf.set_object_metadata(container, a, {'X-Object-Meta-Testingbar':'bar'})
>>> a.get_metadata()
{'x-object-meta-testing': 'foo', 'x-object-meta-testingbar': 'bar'}
>>> 

"""
