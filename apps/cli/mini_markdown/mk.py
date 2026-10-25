r"""Write data/jobs.txt (the test-suite cases) and data/site/ (copied from site/).

python3 -s -P -B mk.py

cases.json holds the cases extract_cases.py pulled out of Python-Markdown's
own test suite. Each becomes a job:

    #job <name>
    #ext <extension>                 one per extension, in order
    #cfg <extension> <key> <t> <v>   t is b (bool), n (None), i (int), s (str)
    #attr toc | toc_tokens           print md.toc / md.toc_tokens too
    #src
    |<line>                          the source, line by line
    #end

In <v> and in source lines, a backslash is written \\, a carriage return
\r and any other control character but tab \xHH. A key of the form
sub.key is a setting extra hands on to one of its extensions.
"""
import json
import os
import shutil


def esc(s):
    out = []
    for ch in s:
        o = ord(ch)
        if ch == '\\':
            out.append('\\\\')
        elif ch == '\r':
            out.append('\\r')
        elif (o < 0x20 and ch != '\t') or o == 0x7f:
            out.append('\\x%02x' % o)
        else:
            out.append(ch)
    return ''.join(out)


def cfg_lines(ext, cfg, prefix=''):
    out = []
    for key, value in cfg.items():
        if isinstance(value, dict):
            out.extend(cfg_lines(ext, value, prefix + key + '.'))
            continue
        if isinstance(value, bool):
            t, v = 'b', 'True' if value else 'False'
        elif value is None:
            t, v = 'n', 'None'
        elif isinstance(value, int):
            t, v = 'i', str(value)
        elif isinstance(value, str):
            t, v = 's', esc(value)
        else:
            raise ValueError('config %r' % (value,))
        out.append('#cfg %s %s%s %s %s' % (ext, prefix, key, t, v))
    return out


def job_lines(name, kwargs, attrs, source):
    lines = ['#job ' + name]
    configs = kwargs.get('extension_configs', {})
    for e in kwargs.get('extensions', []):
        if isinstance(e, dict):
            ext, cfg = e['__ext__'], e['config']
        else:
            ext, cfg = e, configs.get(e, {})
        lines.append('#ext ' + ext)
        lines.extend(cfg_lines(ext, cfg))
    for a in attrs:
        lines.append('#attr ' + a)
    lines.append('#src')
    for line in source.split('\n'):
        lines.append('|' + esc(line))
    lines.append('#end')
    return lines


def main():
    with open('cases.json', encoding='utf-8') as f:
        data = json.load(f)
    if os.path.isdir('data'):
        shutil.rmtree('data')
    os.makedirs('data/site')
    out = []
    for c in data['cases']:
        out.extend(job_lines(c['name'], c['kwargs'], c['attrs'], c['source']))
    pages = sorted(n for n in os.listdir('site') if n.endswith('.md'))
    for name in pages:
        shutil.copyfile(os.path.join('site', name), os.path.join('data/site', name))
    out.append('#site ' + ' '.join(pages))
    with open('data/jobs.txt', 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(out) + '\n')
    print('%d jobs, %d site pages' % (len(data['cases']), len(pages)))


main()
