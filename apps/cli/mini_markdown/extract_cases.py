"""Pull the cases out of Python-Markdown's test suite without running it.

python3 -I -B extract_cases.py <sdist>/tests > cases.json

Walks each test_syntax module's AST for self.assertMarkdownRenders(...)
calls and evaluates their arguments from a small set of node kinds
(string literals, implicit concatenation, +, self.dedent, lists, dicts,
tuples, numbers, booleans, None and calls of the extension classes).
A call with any other node is counted and skipped. The legacy file
tests are read from their directories with the kwargs test_legacy.py
gives them.
"""
import ast
import json
import os
import sys
import textwrap

EXT_CLASSES = {
    'TocExtension': 'toc', 'Nl2BrExtension': 'nl2br', 'AbbrExtension': 'abbr',
    'AdmonitionExtension': 'admonition', 'AttrListExtension': 'attr_list',
    'CodeHiliteExtension': 'codehilite', 'DefListExtension': 'def_list',
    'FencedCodeExtension': 'fenced_code', 'FootnoteExtension': 'footnotes',
    'LegacyAttrExtension': 'legacy_attrs', 'LegacyEmExtension': 'legacy_em',
    'MarkdownInHtmlExtension': 'md_in_html', 'SmartyExtension': 'smarty',
    'TableExtension': 'tables', 'ExtraExtension': 'extra',
    'SaneListExtension': 'sane_lists', 'WikiLinkExtension': 'wikilinks',
    'MetaExtension': 'meta',
}


class Skip(Exception):
    pass


def ev(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (str, int, float, bool)) or node.value is None:
            return node.value
        raise Skip('constant')
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        a, b = ev(node.left), ev(node.right)
        if isinstance(a, str) and isinstance(b, str):
            return a + b
        raise Skip('add')
    if isinstance(node, ast.List) or isinstance(node, ast.Tuple):
        return [ev(e) for e in node.elts]
    if isinstance(node, ast.Dict):
        out = {}
        for k, v in zip(node.keys, node.values):
            if k is None:
                raise Skip('dict splat')
            out[ev(k)] = ev(v)
        return out
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        v = ev(node.operand)
        if isinstance(v, (int, float)):
            return -v
        raise Skip('neg')
    if isinstance(node, ast.Call):
        f = node.func
        if isinstance(f, ast.Attribute) and f.attr == 'dedent' and isinstance(f.value, ast.Name) and f.value.id == 'self':
            if len(node.args) != 1 or node.keywords:
                raise Skip('dedent args')
            s = ev(node.args[0])
            if not isinstance(s, str):
                raise Skip('dedent type')
            return textwrap.dedent(s).strip()
        if isinstance(f, ast.Name) and f.id in EXT_CLASSES:
            if node.args:
                raise Skip('ext positional')
            cfg = {}
            for kw in node.keywords:
                if kw.arg is None:
                    raise Skip('ext splat')
                cfg[kw.arg] = ev(kw.value)
            return {'__ext__': EXT_CLASSES[f.id], 'config': cfg}
        raise Skip('call ' + ast.dump(f)[:40])
    raise Skip(type(node).__name__)


def class_defaults(cls):
    for st in cls.body:
        if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name) \
                and st.targets[0].id == 'default_kwargs':
            return ev(st.value)
    return {}


def syntax_cases(tests_dir, skipped):
    out = []
    root = os.path.join(tests_dir, 'test_syntax')
    for sub in sorted(os.listdir(root)):
        d = os.path.join(root, sub)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.startswith('test_') or not fn.endswith('.py'):
                continue
            with open(os.path.join(d, fn), encoding='utf-8') as f:
                tree = ast.parse(f.read())
            for cls in tree.body:
                if not isinstance(cls, ast.ClassDef):
                    continue
                try:
                    defaults = class_defaults(cls)
                except Skip as e:
                    skipped.append('%s/%s %s: defaults %s' % (sub, fn, cls.name, e))
                    continue
                for meth in cls.body:
                    if not isinstance(meth, ast.FunctionDef):
                        continue
                    n = 0
                    for node in ast.walk(meth):
                        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                                and node.func.attr == 'assertMarkdownRenders'):
                            continue
                        n += 1
                        name = '%s/%s:%s.%s#%d' % (sub, fn[:-3], cls.name, meth.name, n)
                        try:
                            if len(node.args) < 2:
                                raise Skip('args')
                            source = ev(node.args[0])
                            if not isinstance(source, str):
                                raise Skip('source type')
                            kws = dict(defaults)
                            for kw in node.keywords:
                                if kw.arg is None:
                                    raise Skip('kw splat')
                                if kw.arg == 'expected_attrs':
                                    continue
                                kws[kw.arg] = ev(kw.value)
                            attrs = []
                            if len(node.args) >= 3:
                                ea = node.args[2]
                                if isinstance(ea, ast.Dict):
                                    attrs = [ev(k) for k in ea.keys]
                            for kw in node.keywords:
                                if kw.arg == 'expected_attrs' and isinstance(kw.value, ast.Dict):
                                    attrs = [ev(k) for k in kw.value.keys]
                        except Skip as e:
                            skipped.append('%s: %s' % (name, e))
                            continue
                        out.append({'name': name, 'source': source, 'kwargs': kws, 'attrs': attrs})
    return out


LEGACY = [
    ('basic', '.txt', {}, {}),
    ('misc', '.txt', {}, {}),
    ('php', '.text', {}, {}),
    ('pl/Tests_2004', '.text', {}, {}),
    ('pl/Tests_2007', '.text', {}, {}),
    ('extensions', '.txt', {}, {
        'attr_list': {'extensions': ['attr_list', 'def_list', 'smarty']},
        'codehilite': {'extensions': ['codehilite']},
        'toc': {'extensions': ['toc']},
        'toc_invalid': {'extensions': ['toc']},
        'toc_out_of_order': {'extensions': ['toc']},
        'toc_nested': {'extensions': ['toc'], 'extension_configs': {'toc': {'permalink': True}}},
        'toc_nested2': {'extensions': ['toc'], 'extension_configs': {'toc': {'permalink': '[link]'}}},
        'toc_nested_list': {'extensions': ['toc']},
        'wikilinks': {'extensions': ['wikilinks']},
        'github_flavored': {'extensions': ['fenced_code']},
        'sane_lists': {'extensions': ['sane_lists']},
        'nl2br_w_attr_list': {'extensions': ['nl2br', 'attr_list']},
        'admonition': {'extensions': ['admonition']},
    }),
    ('extensions/extra', '.txt', {'extensions': ['extra']}, {
        'loose_def_list': {'extensions': ['def_list']},
        'simple_def_lists': {'extensions': ['def_list']},
        'abbr': {'extensions': ['abbr']},
        'footnotes': {'extensions': ['footnotes']},
        'extra_config': {'extensions': ['extra'],
                         'extension_configs': {'extra': {'footnotes': {'PLACE_MARKER': '~~~placemarker~~~'}}}},
    }),
]


def legacy_cases(tests_dir):
    out = []
    for loc, ext, default, per in LEGACY:
        d = os.path.join(tests_dir, loc)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(ext):
                continue
            stem = fn[:-len(ext)]
            with open(os.path.join(d, fn), encoding='utf-8') as f:
                source = f.read()
            kws = dict(default)
            kws.update(per.get(stem, {}))
            out.append({'name': 'legacy/%s/%s' % (loc, stem), 'source': source, 'kwargs': kws, 'attrs': []})
    return out


def main():
    tests_dir = sys.argv[1]
    skipped = []
    cases = syntax_cases(tests_dir, skipped) + legacy_cases(tests_dir)
    json.dump({'cases': cases, 'skipped': skipped}, sys.stdout, ensure_ascii=False, indent=0)


main()
