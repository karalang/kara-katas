"""Run data/jobs.tsv against the vendored atoma 0.0.17 and print what
mini_atoma must print.

atoma needs attrs, python-dateutil and defusedxml (pip install attrs
python-dateutil==2.9.0.post0 defusedxml==0.7.1). dateutil reads three
things from the machine, and they are pinned here: the local zone is UTC,
"this year" is 2026 (it decides the century of a two-digit year) and
"today" is 2026-10-23 (it fills the fields a date leaves out).

Run: python3 -I -B oracle.py > expected.out
"""
import os
import sys
import time

os.environ["TZ"] = "UTC"
time.tzset()

import datetime  # noqa: E402
import enum  # noqa: E402
import types  # noqa: E402
import warnings  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
os.chdir(HERE)
warnings.simplefilter("ignore")

import attr  # noqa: E402
import dateutil  # noqa: E402
from dateutil.parser import _parser  # noqa: E402

assert dateutil.__version__ == "2.9.0.post0"
_parser.DEFAULTPARSER.info._year = 2026
_parser.DEFAULTPARSER.info._century = 2000


class _Today(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 10, 23, 9, 30)


_dt = types.ModuleType("datetime")
_dt.__dict__.update(datetime.__dict__)
_dt.datetime = _Today
_parser.datetime = _dt

import atoma  # noqa: E402
from atoma import simple, opml  # noqa: E402
from atoma.utils import try_parse_date  # noqa: E402

assert atoma.__version__ == "0.0.17"


def fmt(v):
    if v is None or isinstance(v, (bool, int)):
        return str(v)
    if isinstance(v, str):
        return repr(v)
    if isinstance(v, datetime.datetime):
        return v.isoformat()
    if isinstance(v, datetime.timedelta):
        return str(v)
    if isinstance(v, enum.Enum):
        return str(v)
    if isinstance(v, list):
        return repr(v)
    raise TypeError(type(v))


def dump(obj, ind):
    print(ind + type(obj).__name__)
    for f in attr.fields(type(obj)):
        v = getattr(obj, f.name)
        if attr.has(type(v)):
            print("%s  %s:" % (ind, f.name))
            dump(v, ind + "    ")
        elif isinstance(v, list) and v and attr.has(type(v[0])):
            print("%s  %s: [%d]" % (ind, f.name, len(v)))
            for x in v:
                dump(x, ind + "    ")
        else:
            print("%s  %s: %s" % (ind, f.name, fmt(v)))


def read_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def utc(d):
    return d.astimezone(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")


def river(path):
    """A feed reader's front page: every feed an OPML file subscribes to,
    read from the cache, merged newest first."""
    subs = opml.parse_opml_file(path)
    urls = opml.get_feed_list(subs)
    print("  %d feeds in %s" % (len(urls), fmt(subs.title)))
    cache = {}
    with open("data/cache/urls.tsv", encoding="utf-8") as fh:
        for line in fh.read().splitlines():
            url, _, local = line.partition("\t")
            cache[url] = "data/" + local
    entries = []
    for url in urls:
        local = cache.get(url)
        if local is None:
            print("  %s: not in the cache" % url)
            continue
        try:
            feed = simple.simple_parse_file(local)
        except Exception as e:
            print("  %s: %s: %s" % (url, type(e).__name__, e))
            continue
        print("  %s: %s, %d articles" % (url, fmt(feed.title),
                                         len(feed.articles)))
        for a in feed.articles:
            entries.append((feed.title, a))
    entries.sort(key=lambda e: e[1].published_at.timestamp()
                 if e[1].published_at else float("-inf"), reverse=True)
    for title, a in entries:
        when = utc(a.published_at) if a.published_at else "-"
        print("  %-16s  %s: %s %s" % (when, title, fmt(a.title), fmt(a.link)))


def podcast(path):
    """List a podcast's episodes and files, with the totals."""
    feed = simple.simple_parse_file(path)
    print("  %s" % fmt(feed.title))
    files = 0
    size = 0
    length = datetime.timedelta(0)
    for a in feed.articles:
        for att in a.attachments:
            files += 1
            print("  %s: %s %s %s %s" % (fmt(a.title), fmt(att.title),
                                         fmt(att.mime_type),
                                         fmt(att.size_in_bytes),
                                         fmt(att.duration)))
            size += att.size_in_bytes or 0
            if att.duration:
                length += att.duration
    print("  %d episodes, %d files, %d bytes, %s" % (len(feed.articles), files,
                                                     size, length))


def run(job):
    kind, arg = job[0], job[1]
    if kind == "rss":
        dump(atoma.parse_rss_file(arg), "  ")
    elif kind == "atom":
        dump(atoma.parse_atom_file(arg), "  ")
    elif kind == "json":
        dump(atoma.parse_json_feed_file(arg), "  ")
    elif kind == "json_bytes":
        dump(atoma.parse_json_feed_bytes(read_bytes(arg)), "  ")
    elif kind == "opml":
        o = atoma.parse_opml_file(arg)
        dump(o, "  ")
        print("  feeds: %s" % fmt(opml.get_feed_list(o)))
    elif kind == "simple":
        dump(simple.simple_parse_file(arg), "  ")
    elif kind == "simple_bytes":
        dump(simple.simple_parse_bytes(read_bytes(arg)), "  ")
    elif kind == "date":
        print("  %s" % fmt(try_parse_date(arg)))
    elif kind == "river":
        river(arg)
    elif kind == "podcast":
        podcast(arg)
    else:
        raise SystemExit("unknown job " + kind)


def main():
    with open(os.path.join("data", "jobs.tsv"), encoding="utf-8") as fh:
        jobs = fh.read().split("\n")
    for job in jobs:
        if not job:
            continue
        if job.startswith("#"):
            print(job)
            continue
        print("> " + job.replace("\t", " "))
        try:
            run(job.split("\t"))
        except Exception as e:
            print("  error %s: %s" % (type(e).__name__, e))


main()
