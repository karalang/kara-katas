r"""Run data/jobs.txt through the vendored Python-Markdown 3.11.2.

python3 -I -B oracle.py > expected.out

Pygments is blocked, so codehilite takes the path it takes without it:
the plain <pre class="codehilite"><code class="language-..."> block that
the Kāra port also writes. The vendored dist-info gives the extensions'
entry points, which is how short names such as 'toc' are found.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.modules['pygments'] = None
sys.path.insert(0, os.path.join(HERE, 'vendor'))
import markdown  # noqa: E402


def unesc(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            d = s[i + 1]
            if d == '\\':
                out.append('\\')
                i += 2
                continue
            if d == 'r':
                out.append('\r')
                i += 2
                continue
            if d == 'x':
                out.append(chr(int(s[i + 2:i + 4], 16)))
                i += 4
                continue
        out.append(c)
        i += 1
    return ''.join(out)


def value(t, v):
    if t == 'b':
        return v == 'True'
    if t == 'n':
        return None
    if t == 'i':
        return int(v)
    return unesc(v)


def read_jobs(path):
    jobs = []
    site = None
    cur = None
    with open(path, encoding='utf-8', newline='') as f:
        lines = f.read().split('\n')
    for line in lines:
        if cur is not None and cur.get('in_src'):
            if line.startswith('|'):
                cur['src'].append(unesc(line[1:]))
                continue
            cur['in_src'] = False
        if line.startswith('#job '):
            cur = {'name': line[5:], 'exts': [], 'attrs': [], 'src': [], 'in_src': False}
        elif line.startswith('#ext '):
            cur['exts'].append([line[5:], {}])
        elif line.startswith('#cfg '):
            ext, key, t, v = line[5:].split(' ', 3)
            cfg = [e for e in cur['exts'] if e[0] == ext][-1][1]
            if '.' in key:
                sub, k = key.split('.', 1)
                cfg.setdefault(sub, {})[k] = value(t, v)
            else:
                cfg[key] = value(t, v)
        elif line.startswith('#attr '):
            cur['attrs'].append(line[6:])
        elif line == '#src':
            cur['in_src'] = True
        elif line == '#end':
            jobs.append(cur)
            cur = None
        elif line.startswith('#site '):
            site = line[6:].split(' ')
    return jobs, site


def token_repr(tokens):
    return repr(tokens)


def run_job(n, job):
    names = []
    configs = {}
    for ext, cfg in job['exts']:
        names.append(ext)
        if cfg:
            configs[ext] = cfg
    label = ', '.join(names) if names else '-'
    print('== %d %s | %s' % (n, job['name'], label))
    try:
        md = markdown.Markdown(extensions=names, extension_configs=configs)
        out = md.convert('\n'.join(job['src']))
    except Exception as e:  # noqa: BLE001
        print('! %s: %s' % (type(e).__name__, e))
        return
    print(out)
    if 'toc' in job['attrs']:
        print('-- toc')
        print(md.toc)
    if 'toc_tokens' in job['attrs']:
        print('-- toc_tokens')
        print(token_repr(md.toc_tokens))


SITE_EXTENSIONS = ['meta', 'toc', 'extra', 'admonition', 'codehilite', 'smarty', 'wikilinks']
SITE_CONFIGS = {'toc': {'permalink': True, 'toc_depth': '2-3'}}


def fnv(data):
    h = 0x811c9dc5
    for b in data:
        h = ((h ^ b) * 0x01000193) & 0xffffffff
    return h


def flatten(tokens, out):
    for t in tokens:
        out.append(t)
        flatten(t['children'], out)


def page_html(title, nav, toc, body):
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<title>%s - Harbor</title>\n</head>\n<body>\n<nav>\n%s\n</nav>\n'
            '<aside>\n%s\n</aside>\n<main>\n%s\n</main>\n</body>\n</html>\n') % (title, nav, toc, body)


def run_site(pages):
    print('== site | %s' % ', '.join(SITE_EXTENSIONS))
    built = []
    for name in pages:
        with open(os.path.join('data', 'site', name), encoding='utf-8', newline='') as f:
            text = f.read()
        md = markdown.Markdown(extensions=SITE_EXTENSIONS, extension_configs=SITE_CONFIGS)
        body = md.convert(text)
        meta = md.Meta
        stem = name[:-3]
        title = meta['title'][0] if 'title' in meta else stem
        order = int(meta['order'][0]) if 'order' in meta else 99
        built.append((order, stem, title, body, md.toc, meta, md.toc_tokens))
    built.sort(key=lambda b: (b[0], b[1]))
    os.makedirs(os.path.join('data', 'out'), exist_ok=True)
    for order, stem, title, body, toc, meta, tokens in built:
        print('-- %s.md: %s (order %d)' % (stem, title, order))
        print(body)
        print('-- toc')
        print(toc)
        print('-- meta')
        for key in sorted(meta):
            print('%s: %s' % (key, ' | '.join(meta[key])))
    print('-- search')
    for order, stem, title, body, toc, meta, tokens in built:
        flat = []
        flatten(tokens, flat)
        for t in flat:
            print('%s.html#%s %d %s' % (stem, t['id'], t['level'], t['name']))
    print('-- files')
    for order, stem, title, body, toc, meta, tokens in built:
        items = []
        for o2, s2, t2, b2, toc2, m2, tok2 in built:
            cls = ' class="active"' if s2 == stem else ''
            items.append('<li%s><a href="%s.html">%s</a></li>' % (cls, s2, t2))
        nav = '<ul>\n' + '\n'.join(items) + '\n</ul>'
        page = page_html(title, nav, toc, body)
        path = os.path.join('data', 'out', stem + '.html')
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(page)
        with open(path, 'rb') as f:
            data = f.read()
        print('out/%s.html %d bytes fnv %08x' % (stem, len(data), fnv(data)))


def main():
    jobs, site = read_jobs(os.path.join('data', 'jobs.txt'))
    for n, job in enumerate(jobs, 1):
        run_job(n, job)
    if site:
        run_site(site)


main()
