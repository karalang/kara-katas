# Runs data/jobs.txt on the vendored parsimonious and prints the results.
# Run as: python3 -I -B oracle.py > expected.out
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'vendor'))
# parsimonious imports the third-party `regex` module as `re`. The grammars
# here use only syntax that `regex` and the standard `re` treat alike, and
# the port's engine is a port of `re`, so the oracle runs on `re`.
sys.modules['regex'] = re
from parsimonious.grammar import Grammar, rule_grammar  # noqa: E402
from parsimonious.nodes import Node, NodeVisitor  # noqa: E402

D = os.path.join(HERE, 'data')


def read(path):
    with open(os.path.join(D, path), encoding='utf-8', newline='') as f:
        return f.read()


def block(s):
    if s:
        for line in s.split('\n'):
            print('  ' + line)


def fail(e):
    block('%s: %s' % (type(e).__name__, e))


def items(x):
    # An empty `*` or `?` visits to its Node, as generic_visit returns it.
    return [] if isinstance(x, Node) else x


class Calc(NodeVisitor):
    def visit_line(self, node, ch):
        return ch[1]

    def visit_expr(self, node, ch):
        v, rest = ch
        for op, t in items(rest):
            v = v + t if op == '+' else v - t
        return v

    def visit_term(self, node, ch):
        v, rest = ch
        for op, f in items(rest):
            if op == '*':
                v = v * f
            elif op == '/':
                v = v // f
            else:
                v = v % f
        return v

    visit_factor = NodeVisitor.lift_child

    def visit_neg(self, node, ch):
        return -ch[2]

    def visit_paren(self, node, ch):
        return ch[2]

    def visit_call(self, node, ch):
        name, args = ch[0], items(ch[3])
        args = args[0] if args else []
        if name == 'max':
            return max(args)
        if name == 'min':
            return min(args)
        if name == 'abs':
            if len(args) != 1:
                raise TypeError('abs takes 1 argument, got %d' % len(args))
            return abs(args[0])
        if name == 'pow':
            if len(args) != 2:
                raise TypeError('pow takes 2 arguments, got %d' % len(args))
            return args[0] ** args[1]
        raise NameError('unknown function %r' % name)

    def visit_args(self, node, ch):
        first, rest = ch
        return [first] + [e for _, _, e in items(rest)]

    def visit_addop(self, node, ch):
        return node.text.strip()

    visit_mulop = visit_addop

    def visit_number(self, node, ch):
        return int(node.text)

    def visit_name(self, node, ch):
        return node.text

    def generic_visit(self, node, ch):
        return ch or node


class Json(NodeVisitor):
    def visit_value(self, node, ch):
        return ch[1][0]

    def visit_object(self, node, ch):
        d = {}
        for m in items(ch[2]):
            for k, v in m:
                d[k] = v
        return d

    def visit_members(self, node, ch):
        first, rest = ch
        return [first] + [p for _, _, p in items(rest)]

    def visit_pair(self, node, ch):
        return (ch[0], ch[3])

    def visit_array(self, node, ch):
        out = []
        for m in items(ch[2]):
            out.extend(m)
        return out

    def visit_items(self, node, ch):
        first, rest = ch
        return [first] + [v for _, v in items(rest)]

    def visit_string(self, node, ch):
        return json.loads(node.text)

    def visit_number(self, node, ch):
        return int(node.text)

    def visit_true(self, node, ch):
        return True

    def visit_false(self, node, ch):
        return False

    def visit_null(self, node, ch):
        return None

    def generic_visit(self, node, ch):
        return ch or node


def leaves(v, path, out):
    if isinstance(v, dict) and v:
        for k, x in v.items():
            leaves(x, path + '.' + k if path else k, out)
    elif isinstance(v, list) and v:
        for i, x in enumerate(v):
            leaves(x, '%s[%d]' % (path, i), out)
    else:
        out.append('%s = %s' % (path or '.', json.dumps(v)))


class Ini(NodeVisitor):
    def visit_file(self, node, ch):
        sections = {}
        cur = None
        for [item] in ch:
            if item is None:
                continue
            if item[0] == 'section':
                cur = sections.setdefault(item[1], {})
            else:
                if cur is None:
                    cur = sections.setdefault('DEFAULT', {})
                cur[item[1]] = item[2]
        return sections

    def visit_section(self, node, ch):
        return ('section', ch[1].text.strip())

    def visit_pair(self, node, ch):
        raw = ch[5].text.strip()
        if raw.isdigit():
            val = int(raw)
        elif raw.lower() in ('yes', 'true', 'on'):
            val = True
        elif raw.lower() in ('no', 'false', 'off'):
            val = False
        elif raw == '':
            val = None
        else:
            val = raw
        return ('pair', ch[1].text, val)

    def visit_comment(self, node, ch):
        return None

    visit_blank = visit_comment

    def generic_visit(self, node, ch):
        return ch or node


FIELDS = ['name', 'age', 'city', 'active', 'role']


class Query(NodeVisitor):
    def visit_query(self, node, ch):
        return ch[1]

    def visit_disj(self, node, ch):
        first, rest = ch
        rest = [c for _, c in items(rest)]
        return ('or', [first] + rest) if rest else first

    def visit_conj(self, node, ch):
        first, rest = ch
        rest = [c for _, c in items(rest)]
        return ('and', [first] + rest) if rest else first

    def visit_neg(self, node, ch):
        [x] = ch
        return ('not', x[1]) if isinstance(x, list) else x

    visit_atom = NodeVisitor.lift_child

    def visit_group(self, node, ch):
        return ch[2]

    def visit_cmp(self, node, ch):
        return ('cmp', ch[0], ch[1], ch[2])

    def visit_flag(self, node, ch):
        return ('flag', ch[0])

    def visit_op(self, node, ch):
        return node.text.strip()

    def visit_value(self, node, ch):
        return ch[0][0]

    def visit_number(self, node, ch):
        return int(node.text)

    def visit_string(self, node, ch):
        return node.text[1:-1]

    def visit_field(self, node, ch):
        name = ch[1].text
        if name not in FIELDS:
            raise ValueError('unknown field %r' % name)
        return name

    def generic_visit(self, node, ch):
        return ch or node


def holds(q, rec):
    kind = q[0]
    if kind == 'or':
        return any(holds(x, rec) for x in q[1])
    if kind == 'and':
        return all(holds(x, rec) for x in q[1])
    if kind == 'not':
        return not holds(q[1], rec)
    if kind == 'flag':
        return bool(rec[q[1]])
    _, field, op, want = q
    have = rec[field]
    if op == '=':
        return have == want
    if op == '!=':
        return have != want
    if op == '<':
        return have < want
    if op == '>':
        return have > want
    if op == '<=':
        return have <= want
    if op == '>=':
        return have >= want
    return str(want).lower() in str(have).lower()


def records(path):
    lines = read(path).split('\n')
    head = lines[0].split(',')
    out = []
    for line in lines[1:]:
        if not line:
            continue
        rec = dict(zip(head, line.split(',')))
        rec['age'] = int(rec['age'])
        rec['active'] = rec['active'] == 'yes'
        out.append(rec)
    return out


def main():
    calc = Grammar(read('grammars/calc.peg'))
    jsong = Grammar(read('grammars/json.peg'))
    ini = Grammar(read('grammars/ini.peg'))
    query = Grammar(read('grammars/query.peg'))
    for job in read('jobs.txt').split('\n'):
        if not job:
            continue
        print('> ' + job)
        w = job.split(' ')
        if w[0] == 'rules':
            print('  %d rules, default %s' % (len(rule_grammar), rule_grammar.default_rule.name))
            block(str(rule_grammar))
        elif w[0] == 'grammar':
            try:
                g = Grammar(read(w[1]))
            except Exception as e:
                fail(e)
                continue
            dflt = g.default_rule.name if g.default_rule else None
            print('  %d rules, default %s' % (len(g), dflt))
            block(str(g))
        elif w[0] in ('tree', 'match'):
            text = read(w[2])
            try:
                g = Grammar(read(w[1]))
                expr = g[w[3]] if len(w) > 3 else g
                node = expr.parse(text) if w[0] == 'tree' else expr.match(text)
            except Exception as e:
                fail(e)
                continue
            if w[0] == 'match':
                print('  matched %d of %d: %r' % (node.end, len(text), node.text))
            block(node.prettily())
        elif w[0] == '!calc':
            for line in read(w[1]).split('\n'):
                if not line:
                    continue
                try:
                    print('  %r = %d' % (line, Calc().visit(calc.parse(line))))
                except Exception as e:
                    print('  %r' % line)
                    fail(e)
        elif w[0] == '!json':
            try:
                v = Json().visit(jsong.parse(read(w[1])))
            except Exception as e:
                fail(e)
                continue
            print('  ' + json.dumps(v))
            out = []
            leaves(v, '', out)
            for line in out:
                print('    ' + line)
        elif w[0] == '!ini':
            try:
                cfg = Ini().visit(ini.parse(read(w[1])))
            except Exception as e:
                fail(e)
                continue
            for name, sec in cfg.items():
                print('  [%s]' % name)
                for k, v in sec.items():
                    print('    %s = %r' % (k, v))
        elif w[0] == '!query':
            recs = records(w[1])
            for line in read(w[2]).split('\n'):
                if not line:
                    continue
                try:
                    q = Query().visit(query.parse(line))
                    names = [r['name'] for r in recs if holds(q, r)]
                except Exception as e:
                    print('  %s' % line)
                    fail(e)
                    continue
                print('  %s: %s (%d)' % (line, ', '.join(names) or '-', len(names)))


main()
