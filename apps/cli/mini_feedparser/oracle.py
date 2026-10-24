# Runs data/jobs.txt on the vendored feedparser and prints the results.
# Run as: python3 -I -B oracle.py > expected.out
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'vendor'))
import feedparser  # noqa: E402
from feedparser import datetimes  # noqa: E402
from feedparser.sanitizer import _sanitize_html  # noqa: E402
from feedparser.urls import resolve_relative_uris  # noqa: E402

D = os.path.join(HERE, 'data')

# The port has the w3dtf and rfc822 handlers only. Check that every date the
# jobs meet is either taken by one of them or refused by all the others.
_ported = (datetimes._parse_date_w3dtf, datetimes._parse_date_rfc822)


def _guard(handlers):
    def wrap(h):
        def f(s):
            r = h(s)
            if h not in _ported and r:
                raise SystemExit('unported date handler %s took %r' % (h.__name__, s))
            return r
        return f
    return [wrap(h) for h in handlers]


datetimes._date_handlers[:] = _guard(datetimes._date_handlers)


def scalar(v):
    if isinstance(v, time.struct_time):
        return repr(tuple(v))
    return repr(v)


def dump(v, ind, out):
    if isinstance(v, dict):
        for k, x in v.items():
            if isinstance(x, (dict, list)) and x:
                out.append('%s%s:' % (ind, k))
                dump(x, ind + '  ', out)
            else:
                out.append('%s%s: %s' % (ind, k, '{}' if isinstance(x, dict) else scalar(x)))
    else:
        for i, x in enumerate(v):
            if isinstance(x, (dict, list)) and x:
                out.append('%s- [%d]' % (ind, i))
                dump(x, ind + '  ', out)
            else:
                out.append('%s- %s' % (ind, '{}' if isinstance(x, dict) else scalar(x)))


def parse(path, base=None):
    with open(os.path.join(D, path), 'rb') as f:
        data = f.read()
    hdrs = {'content-location': base} if base else None
    return feedparser.parse(data, response_headers=hdrs)


def exc_text(r):
    e = r.get('bozo_exception')
    return '%s: %s' % (type(e).__name__, e) if e is not None else '-'


def stamp(t):
    return time.strftime('%Y-%m-%d %H:%M:%S', t) if t else '-'


def unesc(s):
    out, i = [], 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            out.append({'n': '\n', 'r': '\r', '\\': '\\'}[s[i + 1]])
            i += 2
        else:
            out.append(s[i])
            i += 1
    return ''.join(out)


def xml_attr(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def main():
    with open(os.path.join(D, 'jobs.txt')) as f:
        jobs = f.read().splitlines()
    for job in jobs:
        print('> ' + job)
        w = job.split(' ')
        if w[0] == 'parse':
            r = parse(w[1], w[2] if len(w) > 2 else None)
            out = []
            for k in ('bozo', 'encoding', 'version'):
                out.append('  %s: %s' % (k, scalar(r.get(k))))
            out.append('  bozo_exception: ' + exc_text(r))
            for k in ('headers', 'namespaces', 'feed'):
                out.append('  %s:' % k)
                dump(r[k], '    ', out)
            out.append('  entries: %d' % len(r['entries']))
            dump(r['entries'], '    ', out)
            print('\n'.join(out))
        elif w[0] == '!dates':
            with open(os.path.join(D, w[1])) as f:
                for s in f.read().split('\n')[:-1]:
                    t = datetimes._parse_date(s)
                    print('  %r -> %s' % (s, scalar(t) if t else 'None'))
        elif w[0] in ('!sanitize', '!resolve'):
            with open(os.path.join(D, w[1])) as f:
                for s in f.read().split('\n')[:-1]:
                    s = unesc(s)
                    if w[0] == '!sanitize':
                        o = _sanitize_html(s, 'utf-8', 'text/html')
                    else:
                        o = resolve_relative_uris(s, w[2], 'utf-8', 'text/html')
                    print('  %r\n    => %r' % (s, o))
        elif w[0] == '!digest':
            rows = []
            for n, p in enumerate(w[1:]):
                r = parse(p)
                for e in r['entries']:
                    t = e.get('updated_parsed') or e.get('published_parsed')
                    rows.append((t, n, r['feed'].get('title', '?'), e.get('title', '(untitled)'), e.get('link', '-')))
            dated = sorted([x for x in rows if x[0]], key=lambda x: tuple(x[0])[:6], reverse=True)
            undated = [x for x in rows if not x[0]]
            print('  %d entries from %d feeds, %d undated' % (len(rows), len(w) - 1, len(undated)))
            for t, n, ft, et, ln in (dated + undated)[:10]:
                print('  %s  %-16s %s <%s>' % (stamp(t), ft[:16], et, ln))
        elif w[0] == '!tags':
            counts = {}
            for p in w[1:]:
                r = parse(p)
                for e in [r['feed']] + r['entries']:
                    for t in e.get('tags', []):
                        term = (t.get('term') or '').lower()
                        if term:
                            counts[term] = counts.get(term, 0) + 1
            for term, c in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
                print('  %3d %s' % (c, term))
        elif w[0] == '!opml':
            print('  <opml version="2.0"><body>')
            for p in w[1:]:
                r = parse(p)
                f = r['feed']
                if r['bozo'] and not r['entries']:
                    print('  <!-- skipped %s: %s -->' % (p, type(r['bozo_exception']).__name__))
                    continue
                print('    <outline text="%s" type="%s" xmlUrl="%s" htmlUrl="%s"/>' % (
                    xml_attr(f.get('title', p)), 'atom' if r['version'].startswith('atom') else 'rss',
                    xml_attr(p), xml_attr(f.get('link', ''))))
            print('  </body></opml>')
        elif w[0] == '!health':
            for p in w[1:]:
                r = parse(p)
                e = r.get('bozo_exception')
                print('  %-28s %-8s %-12s %2d entries  %s' % (
                    p[6:], r['version'] or '?', r.get('encoding', '') or '-', len(r['entries']),
                    'ok' if not r['bozo'] else 'bozo ' + type(e).__name__))


main()
