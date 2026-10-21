# Writes data/: the documents expressions are evaluated against
# (data/docs/*.json), the rule files the programs run (data/rules/),
# and the jobs (data/jobs.tsv). oracle.py and mini_simpleeval.kara both
# read them.
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

DOCS = {}

# A signed-in user, as a web app hands one to a rule.
DOCS["user"] = {
    "name": "Ada Lovelace",
    "email": "ada@example.com",
    "age": 36,
    "plan": "pro",
    "tags": ["admin", "beta", "eu"],
    "country": "GB",
    "signup_days": 412,
    "score": 87.5,
    "address": {"city": "London", "postcode": "W1J 7NT", "lines": ["12 Mayfair Pl", "Flat 3"]},
    "items": 3,
    "keys": "k-17",
    "manager": None,
    "verified": True,
    "quota": {"used": 7.25, "limit": 10},
    "locale": "en_GB",
}

# A shop order.
DOCS["order"] = {
    "id": "A-1001",
    "items": [
        {"sku": "TEA-01", "name": "Assam tea", "qty": 2, "price": 4.5},
        {"sku": "MUG-07", "name": "Stoneware mug", "qty": 1, "price": 12.0},
        {"sku": "BIS-03", "name": "Oat biscuits", "qty": 3, "price": 2.25},
    ],
    "subtotal": 27.75,
    "currency": "EUR",
    "coupon": "SPRING10",
    "customer": {"id": 501, "tier": "gold", "orders": 14},
    "shipping": {"country": "DE", "weight_kg": 1.35, "express": False},
    "gift": None,
}

# A host's metrics at one moment.
DOCS["metrics"] = {
    "host": "db-2",
    "cpu": [71.5, 88.0, 93.25, 64.0],
    "mem": {"used_mb": 15872, "total_mb": 16384},
    "disk": {"/": 72, "/var": 91, "/home": 40},
    "load": [3.1, 2.75, 2.5],
    "errors": 17,
    "requests": 12000,
    "up": True,
    "role": "replica",
    "lag_s": 4.5,
}

# An HTTP request as a gateway sees it.
DOCS["request"] = {
    "method": "POST",
    "path": "/api/v2/orders",
    "headers": {"content-type": "application/json", "x-request-id": "r-88", "user-agent": "curl/8.5.0"},
    "query": {"page": "2", "limit": "50", "sort": "-created"},
    "client_ip": "203.0.113.9",
    "body_bytes": 1840,
    "auth": {"scheme": "Bearer", "scopes": ["orders:write", "orders:read"]},
}

# ---------------------------------------------------------------- jobs

JOBS = []


def job(profile, expr, doc="-"):
    JOBS.append((profile, expr, doc))


def group(name):
    JOBS.append(("==", name, ""))


group("numbers")
for e in [
    "20 + 30", "20 + 30 - ( 10 * 5)", "7 / 2", "7 // 2", "-7 // 2", "7 % 3", "-7 % 3", "7 % -3",
    "7.5 // 2", "-7.5 // 2", "7.5 % 2", "-7.5 % 2", "7.5 % -2", "2 ** 10", "2 ** -2", "2 ** 0.5",
    "(-8) ** 2", "2 ** 100", "10 ** 30", "1.5e3 * 2", "0.1 + 0.2", "1 / 3", "2 / 3 * 3",
    "100 * 1.1", "1e16", "1e15 + 0.5", "12345678901234567.0", "1e-5", "0.0001", "1/1024",
    "-0.0", "3.0", "1e300 * 1e10", "-(1e300 * 1e10)", "1e300 * 1e10 - 1e300 * 1e10",
    "0x1F + 0o17 + 0b101", "1_000_000 + 1", "1 + True", "True + True", "True * 2.5",
    "-True", "~5", "~-1", "+3", "--3", "not 0", "not 3", "5 & 3", "5 | 3", "5 ^ 3",
    "True & False", "True | False", "True ^ True", "1 << 10", "1024 >> 3", "-1024 >> 3",
    "3 * (2 + 4) ** 2 / 9", "2 ** 3 ** 2", "-2 ** 2", "(-2) ** 2", "10 - 2 - 3",
    "1 / 0", "1.0 / 0", "1 // 0", "1 % 0", "1.0 // 0", "1.0 % 0", "0 ** -1",
    "10.0 ** 400", "2 ** 4000001", "4000001 ** 2", "1 << 10001", "1 >> 10001",
    "1.5 >> 1", "1 >> 1.5", "(1e300 * 1e10) >> 1", "1.5 & 1", "~1.5", "-'a'",
    "999999999 * 999999999", "2 ** 64 - 1", "-(2 ** 63)", "7 // -2", "-7 // -2",
    "0.5 // 0.1", "1 % 0.3", "5 // 1.5", "-5 % 1.5", "3.5 ** 2", "9 ** 0.5", "0 ** 0",
    "int(7.9)", "int(-7.9)", "int('  42 ')", "int('1_000')", "int('-17')", "int('3.5')",
    "int('abc')", "int('')", "int(True)", "int(None)", "int('ff', 16)", "int('0x1f', 16)",
    "int('z', 36)", "int('12', base=8)", "int('9', 8)", "int()",
    "float('1e3')", "float(' 2.5 ')", "float('inf')", "float('-Infinity')", "float('nan') == float('nan')",
    "float('1_5.0')", "float('abc')", "float(None)", "float(3)", "float()", "float('')",
    "int(float('inf'))", "int(float('nan'))", "str(1.0)", "str(2 ** 70)", "str(None)",
    "str(True) + str(1/4)", "str()", "str(1e22)", "str(-1e-7)", "str(123456.789)",
    "randint(1)", "rand() < 1", "rand() >= 0",
]:
    job("basic", e)

group("strings")
for e in [
    "'hello' + ' ' + 'world'", "'ab' * 3", "3 * 'ab'", "'ab' * 0", "'ab' * -1", "'ab' * True",
    "'ab' * 'cd'", "[1] * 1.5", "'a' + 1", "1 + 'a'", "'x' * 100001", "'x' * 50000 + 'y' * 50001",
    "'abc'[0]", "'abc'[-1]", "'abc'[5]", "'abc'[1:]", "'abcdef'[::2]", "'abcdef'[::-1]",
    "'abcdef'[-3:-1]", "'abcdef'[4:1]", "'abc'['x']", "'abc'[1.0]", "'abc'[::0]", "'abc'['a':]",
    "'abc'[True]", "'hello world'.upper()", "'Hello'.lower()", "'  pad  '.strip()",
    "'xxpadxx'.strip('x')", "'  pad'.lstrip()", "'pad  '.rstrip() + '|'", "'a,b,,c'.split(',')",
    "' a  b c '.split()", "'a,b,c'.split(',', 1)", "'k=v=w'.split('=', maxsplit=1)",
    "'report.csv'.endswith('.csv')", "'report.csv'.endswith(('.tsv', '.csv'))",
    "'https://x'.startswith('http')", "'a-b-c'.replace('-', '+')", "'a-b-c'.replace('-', '', 1)",
    "'hello world'.title()", "'hELLO'.capitalize()", "', '.join(['a', 'b'])", "'-'.join('abc')",
    "'banana'.find('an')", "'banana'.find('x')", "'banana'.count('a')", "'2024'.isdigit()",
    "'abc'.isalpha()", "'42'.zfill(5)", "'-42'.zfill(5)", "'ab'.ljust(5, '.')", "'ab'.rjust(5)",
    "'v1.2'.removeprefix('v')", "'file.tar.gz'.removesuffix('.gz')", "'abc'.upper",
    "'abc'.nope", "'abc'.nope()", "'abc'.__class__", "'abc'.func_x", "'abc'.format",
    "'{}'.format(1)", "'a' in 'cat'", "'x' not in 'cat'", "1 in 'cat'", "'' in 'cat'",
    "'apple' < 'banana'", "'Zebra' < 'apple'", "'a' < 1", "'abc' == 'abc'", "'a' != 'b'",
    "'%s items' % 3", "'%d%%' % 42", "'%5.2f|' % 3.14159", "'%s and %s' % ('a', 'b')",
    "'%r' % 'q'", "'%x' % 255", "'%s' % (1, 2)", "'%s %s' % 'a'", "'%-6s|' % 'ab'",
    "'%05d' % 42", "'%+d' % 7", "'%.3s' % 'abcdef'", "'%i' % 3.9", "'%d' % 'x'",
    "'caf\\u00e9'.upper()", "'stra\\u00dfe'.upper()", "len('caf\\u00e9')", "'\\u00e9'[0]",
    "'tab\\there'", "'quote\\'s'", "\"both ' and \\\"\"", "'line\\nbreak'.split('\\n')",
    "f'{1 + 1}'", "f'x={3!r}'", "f'{\"a\"!r}'", "f'{3.14159:.2f}'", "f'{42:>6}|'",
    "f'{42:06d}'", "f'{1234567:,}'", "f'{0.256:.1%}'", "f'{255:x}'", "f'{255:#x}'",
    "f'{255:b}'", "f'{7:o}'", "f'{\"ab\":*^6}'", "f'{12.5:e}'", "f'{-3:+d}'", "f'{3:+d}'",
    "f'{1e6:,.2f}'", "f'{\"x\":5}|'", "f'{3.0}'", "f'{None}'", "f'{\"a\":d}'", "f'{1.5:d}'",
    "f'{2:.{3}f}'", "f'{1:{\"<\"}4}|'", "f'{-0.0:.1f}'",
    "f'{0.125:.2f} {0.375:.2f} {2.5:.0f} {3.5:.0f}'", "f'{1/3:.10f}'", "f'{1e-7:f}'",
    "f'{123.456:10.1f}|'", "f'{-1.5:08.2f}'", "f'{5:_}'", "f'{10**10:_d}'",
]:
    job("basic", e)

group("logic")
for e in [
    "1 < 2 < 3", "1 < 3 < 2", "3 > 2 > 1 > 0", "1 == 1.0", "1 == True", "1 is 1",
    "None is None", "None is not None", "1 if True else 2", "'yes' if 0 else 'no'",
    "0 or 'default'", "'' or 0", "1 and 2", "0 and 1/0", "1 or 1/0", "None and 1",
    "1 and 2 and 3", "0 or '' or None", "not None", "not ''", "not 'x'", "1 < 'a'",
    "1 == 'a'", "None < 1", "1 != 1.0", "True == 1 == 1.0", "2 > 1 == True", "1 < 2 > 1.5",
    "(1 < 2) + (2 < 3)", "1 in 2", "1 not in 2", "x", "unknown_func(1)", "int", "str(int)[:5]",
    "x.y", "(1).real", "(1).nope", "(2.5).real", "(5).bit_length()", "(2.0).is_integer()",
    "True.real", "None.x", "[1, 2]", "(1, 2)", "{1: 2}", "{1, 2}", "[x for x in 'ab']",
    "'a' if 1 else", "1 +", "(1", "1 2", "", "   ", "# comment", "x = 5", "x = y = 2 + 3",
    "x += 1", "1; 2", "a; b", "import os", "from os import path", "def f(): pass",
    "lambda: 1", "(lambda: 1)()", "assert 1", "for i in 'ab': pass", "pass", "del x",
    "yield 1", "await x", "x := 3", "(y := 3)", "1 @ 2", "...", "b'bytes'", "1j",
    "print(1)", "type(1)", "eval('1')", "open('x')", "getattr(1, 'x')", "int.__name__",
    "''.__class__", "(1).__class__", "'abc'.mro", "'a'.format_map", "[1][0].x",
    "'abc'[1:2:None]", "'abc'[None:None]", "str(1)(2)", "'abc'.upper()()", "1(2)",
    "int(*'1')", "int(**{'base': 2})", "int(nope1, base=nope2)", "int(x='1')",
    "'ab'.upper(1)", "'ab'.split(1)", "'ab'.startswith(1)", "', '.join([1, 2])",
    "'ab'.replace('a')", "'ab'.zfill('5')", "'abc'.find()", "'ab'.count(1)", "(1).bit_length(2)",
    "f'{x}'", "f'{1/0}'", "f'{1:!}'", "'a' 'b'", "'''tri\nple'''", "(1 +\n 2)",
    "1 if 2", "if 1: 2", "1 +* 2", "'unterminated", "\\\\",
    "\"\"", "''.join([])", "0.1 + 0.7", "float('0.1') * 3", "1 if None else None",
]:
    job("basic", e)

group("names")
for e in [
    "name", "age >= 18", "plan == 'pro' and verified", "country in ('GB', 'IE')",
    "'admin' in tags", "address.city", "address['city']", "address.lines[0]",
    "address.postcode.split()[0]", "email.endswith('@example.com')", "name.split()[-1].upper()",
    "score / 100", "round(score)", "round(score / 3, 2)", "round(2.5)", "round(3.5)",
    "round(-0.5)", "round(1234, -2)", "round(1250, -2)", "round(2.675, 2)", "round(0.125, 2)",
    "round(7.25)", "round(quota.used / quota.limit, 3)", "quota.limit - quota.used",
    "len(f'{\"x\" * 60000}{\"y\" * 50000}')", "len(f'{\"x\" * 100001}')",
    "len(name)", "len(tags)", "len(address)", "len(age)", "len(items)", "items",
    "keys", "manager", "manager is None", "manager.name", "manager['name']",
    "missing", "missing.x", "tags[3]", "tags[-1]", "tags[1:]", "tags['a']", "address.zip",
    "address.get('zip', '-')", "address.get('city')", "address.keys", "len(address.keys())",
    "'city' in address", "'city' in address.keys()", "'London' in address.values()",
    "address.items", "len(address.items)", "min(age, signup_days)", "max(3, 9, 4)",
    "max(tags)", "min('b', 'a', 'c')", "max([])", "max()", "max(1, 'a')", "min(1, 'a')",
    "abs(-age)", "abs(-2.5)", "abs('a')", "abs(True)", "age * 2 if verified else 0",
    "f'{name} <{email}>'", "f'{name.split()[0]}, you have {items} items'",
    "f'{score:.1f}% of {quota.limit}'", "f'{age:>5}|{plan:<5}|'", "f'{tags}'",
    "f'{address}'", "f'{manager}'", "f'{verified}'", "f'{quota}'", "str(tags)",
    "tags + ['new']", "tags + 'x'", "tags * 2", "tags == ['admin', 'beta', 'eu']",
    "tags < ['b']", "tags[0] < tags[1]", "address == address", "address < address",
    "verified + 1", "len", "len(len)", "round", "round(None)", "round(1.5, 'a')",
    "round(1, 2)", "round(1.234567e10, -3)", "round(-1.5)", "round(float('inf'))",
    "round(float('nan'), 2)", "locale.split('_')", "locale[:2].lower() == 'en'",
    "name.lower().replace(' ', '.') + '@corp'", "signup_days // 7", "signup_days % 7",
    "int(address.postcode[1])", "address.lines.count('Flat 3')", "address.lines.index('Flat 3')",
    "address.lines.index('x')", "tags.index('eu')", "name[0] + name.split()[1][0]",
    "age > 30 and 'senior' or 'junior'", "plan in 'enterprise pro'",
    "(age > 30) + (score > 50) + verified", "address.lines[1].startswith('Flat')",
]:
    job("ctx", e, "user")

for e in [
    "id", "currency", "coupon[:6]", "items[0].name", "items[0]['qty'] * items[0]['price']",
    "items[1].price", "len(items)", "items.price", "customer.tier", "customer.orders > 10",
    "shipping.weight_kg * 4.2", "round(shipping.weight_kg * 4.2, 2)", "shipping.express",
    "not shipping.express", "subtotal * 0.9", "round(subtotal * 0.9, 2)",
    "subtotal - 5 if coupon == 'SPRING10' else subtotal", "gift", "gift or 'no gift'",
    "max(items[0].price, items[1].price, items[2].price)", "items[-1].sku.split('-')[0]",
    "customer.id // 100", "f'{id}: {subtotal:.2f} {currency}'", "f'{items[1].name!r}'",
    "items[0].qty + items[1].qty + items[2].qty", "items[5]", "items.x", "shipping.country.lower()",
]:
    job("ctx", e, "order")

for e in [
    "headers['content-type']", "headers.get('authorization')", "headers.get('x-request-id', '')",
    "method in ('POST', 'PUT') and body_bytes > 1024", "path.startswith('/api/')",
    "path.split('/')", "path.split('/')[2]", "int(query.limit) <= 100", "query.page",
    "int(query.page) * int(query.limit)", "query.sort.startswith('-')", "query.sort[1:]",
    "auth.scheme == 'Bearer' and 'orders:write' in auth.scopes", "len(auth.scopes)",
    "client_ip.split('.')[0]", "int(client_ip.split('.')[-1]) % 2",
    "headers.user-agent", "headers['user-agent'].split('/')[1]", "headers.keys",
    "f'{method} {path} ({body_bytes} bytes)'", "query.get('offset', '0')",
]:
    job("ctx", e, "request")

group("compound")
for e in [
    "[1, 2, 3]", "(1, 2, 3)", "(1,)", "()", "[]", "{}", "{1: 'a', 'b': 2}", "{1, 2, 3}",
    "{3, 1, 2}", "{1, 1, 1}", "set()", "list('abc')", "tuple([1, 2])", "dict(a=1, b=2)",
    "dict([(1, 2), (3, 4)])", "list((1, 2))", "list(5)", "dict(5)", "tuple()", "list()",
    "dict()", "[1, 2] + [3]", "[1, 2] * 2", "[[1, 2], [3]][1][0]", "[1, 2, 3][1:]",
    "[1, 2, 3][::-1]", "[1, 2, 3][-5]", "(1, 2) + (3,)", "(1, 2)[5]", "{1: 2}[1]",
    "{1: 2}[3]", "{'a': 1}['b']", "{'a': {'b': [10, 20]}}['a']['b'][1]", "{'a': 1}.a",
    "{'a': 1}.get('a')", "{'a': 1}.keys()", "{'a': 1}.values()", "{'a': 1, 'b': 2}.items()",
    "list({'a': 1, 'b': 2}.items())", "[x * 2 for x in [1, 2, 3]]", "[x for x in range(10) if x % 3 == 0]",
    "[x + y for x in 'ab' for y in 'cd']", "[(x, y) for x in range(3) for y in range(x)]",
    "[[y for y in range(x)] for x in range(4)]", "{x: x * x for x in range(4)}",
    "{k: v for k, v in [('a', 1), ('b', 2)]}", "[a for a, b in [(1, 2, 3)]]",
    "[a for a, b in [1]]", "[x for x in 5]", "sum(x for x in range(5))", "(x for x in [1, 2])",
    "{x for x in 'ab'}", "[x for x in range(20000)]", "[x for x in range(5000) for y in range(3)]",
    "[x for x in range(3)] + [y for y in range(9999)]", "len([x for x in range(9999)])",
    "x", "[x for x in [1]] and x", "[n for n in [1, 2] if n > q]", "[1, *[2, 3], *'ab']",
    "[*5]", "{**{'a': 1}, 'b': 2}", "{**{'a': 1}, **{'a': 2}}", "{**[(1, 2)]}", "{**[(1, 2, 3)]}",
    "{**[1]}", "{**5}", "{[1]: 2}", "[1] in {1: 2}", "{1: 2, 1: 3}", "{1, 1.0, True}",
    "len({1, 2, 2})", "2 in {1, 2}", "[1, 2] == [1, 2]", "[1, 2] < [1, 3]", "(1, 'a') < (1, 'b')",
    "(1, 2) == [1, 2]", "[1, 'a'] < [1, 2]", "{'a': 1} == {'a': 1.0}", "[] or [0]",
    "[0] and 'non-empty'", "not []", "not {}", "{} == dict()", "[1, 2, 3].count(2)",
    "[1, 2, 3].index(3)", "(1, 2).index(5)", "[3, 1, 2].sort", "{'a': 1}.update",
    "list({'b': 1, 'a': 2})", "tuple('ab')", "set('aab') == set('ab')", "len(set('hello'))",
    "dict(zip='z')", "dict({'a': 1}, b=2)", "[x for x.y in [1]]", "[x for (x) in [1]]",
    "[x for [x, y] in [(1, 2)]]", "{1: [x for x in range(3)]}", "f'{[1, 2]}'",
    "f'{(1,)}'", "f'{ {1: 2} }'", "f'{[x * 2 for x in range(3)]}'", "[1, 2][True]",
    "[1, 2, 3][1:2:0]", "[1, 2, 3]['a':]", "tuple([1, [2]])", "{(1, 2): 'pair'}[(1, 2)]",
    "{(1, [2]): 3}", "dict([(1, 2), (3,)])", "dict([1])", "list({1: 2}.keys()) + [3]",
    "'b' in {'a': 1}.keys()", "len({'a': 1}.items())", "[k for k in {'x': 1, 'y': 2}]",
    "[v for k, v in {'x': 1, 'y': 2}.items() if v > 1]", "[c.upper() for c in 'abc']",
]:
    if "range(" in e or "len(" in e or "sum(" in e:
        job("cctx", e, "order")
    else:
        job("compound", e)

for e in [
    "[i.sku for i in items]", "sum(i.qty for i in items)", "sum(i.qty * i.price for i in items)",
    "round(sum([i.qty * i.price for i in items]), 2)", "max(i.price for i in items)",
    "sorted(i.price for i in items)", "sorted([i.name for i in items], reverse=True)",
    "any(i.qty > 2 for i in items)", "all(i.price < 20 for i in items)",
    "[i.name for i in items if i.price > 3]", "{i.sku: i.qty for i in items}",
    "len([i for i in items if i.sku.startswith('TEA')])", "sorted(items[0])",
    "sorted(items)", "sum([])", "sum(['a', 'b'])", "sum([[1], [2]], [])", "sum([1, 2], 10)",
    "min([i.qty for i in items])", "any([])", "all([])", "list(range(3, 10, 3))",
    "range(5)", "len(range(10))", "list(range(-3))", "range(1, 2, 0)", "list(range('a'))",
    "[x for x in range(3)][-1]", "sorted('banana')", "sorted([3, 1, 'a'])", "sorted([], reverse=True)",
    "max([i.qty for i in items], default=0)", "max([], default=0)", "[s for s in customer]",
    "{**customer, 'tier': 'platinum'}", "[k for k in shipping if shipping[k]]",
    "sorted(shipping.keys())", "list(shipping.values())", "len(shipping.items())",
    "[p for p in [i.price for i in items] if p > 3]", "{c: len(c) for c in ['de', 'eur']}",
    "tuple(i.qty for i in items)", "set(i.qty for i in items) == {1, 2, 3}",
]:
    job("cctx", e, "order")

for e in [
    "max(cpu) > 90", "sum(cpu) / len(cpu)", "round(sum(cpu) / len(cpu), 1)",
    "[c for c in cpu if c > 80]", "len([c for c in cpu if c > 80]) >= 2",
    "mem.used_mb / mem.total_mb", "round(100 * mem.used_mb / mem.total_mb, 2)",
    "[m for m in disk if disk[m] > 70]", "sorted(disk.values())", "max(disk.values())",
    "{m: p for m, p in disk.items() if p >= 72}", "load[0] > 3 and role == 'replica'",
    "errors / requests * 1000", "f'{host}: {errors / requests:.3%} errors'",
    "up and lag_s < 5", "any(p > 90 for p in disk.values())", "all(l < 4 for l in load)",
    "sorted(disk, reverse=True)", "[f'{m}={disk[m]}%' for m in sorted(disk)]",
    "sum(range(errors))", "list(range(len(load)))", "[round(c) for c in cpu]",
]:
    job("cctx", e, "metrics")

# ---------------------------------------------------------------- the programs' files

ORDERS = [
    {"id": "A-1001", "customer": {"id": 501, "tier": "gold", "orders": 14}, "items": [
        {"sku": "TEA-01", "qty": 2, "price": 4.5}, {"sku": "MUG-07", "qty": 1, "price": 12.0},
        {"sku": "BIS-03", "qty": 3, "price": 2.25}], "coupon": "SPRING10",
        "shipping": {"country": "DE", "weight_kg": 1.35, "express": False}},
    {"id": "A-1002", "customer": {"id": 502, "tier": "new", "orders": 0}, "items": [
        {"sku": "TEA-02", "qty": 10, "price": 3.8}], "coupon": None,
        "shipping": {"country": "FR", "weight_kg": 2.1, "express": True}},
    {"id": "A-1003", "customer": {"id": 503, "tier": "silver", "orders": 3}, "items": [
        {"sku": "MUG-07", "qty": 4, "price": 12.0}, {"sku": "POT-01", "qty": 1, "price": 39.0}],
        "coupon": "BULK", "shipping": {"country": "GB", "weight_kg": 6.4, "express": False}},
    {"id": "A-1004", "customer": {"id": 504, "tier": "gold", "orders": 40}, "items": [],
        "coupon": "SPRING10", "shipping": {"country": "DE", "weight_kg": 0, "express": False}},
    {"id": "A-1005", "customer": {"id": 505, "tier": "silver", "orders": 7}, "items": [
        {"sku": "BIS-03", "qty": 12, "price": 2.25}, {"sku": "TEA-01", "qty": 1, "price": 4.5}],
        "coupon": "WELCOME", "shipping": {"country": "US", "weight_kg": 2.0, "express": True}},
]

PRICING = [
    ("subtotal", "round(sum(i.qty * i.price for i in items), 2)"),
    ("units", "sum(i.qty for i in items)"),
    ("tier_discount", "{'gold': 0.1, 'silver': 0.05}.get(customer.tier, 0)"),
    ("coupon_off", "{'SPRING10': 10, 'BULK': 15}[coupon] if coupon else 0"),
    ("bulk", "any(i.qty >= 10 for i in items)"),
    ("shipping", "0 if shipping.country == 'DE' and not shipping.express else round(4.9 + shipping.weight_kg * 1.2 + (9 if shipping.express else 0), 2)"),
    ("eu", "shipping.country in ('DE', 'FR', 'IE', 'NL')"),
    ("vat", "{'DE': 0.19, 'FR': 0.2, 'GB': 0.2}[shipping.country]"),
    ("loyal", "customer.orders >= 10 or customer.tier == 'gold'"),
    ("first_sku", "items[0].sku"),
    ("cheapest", "min(i.price for i in items)"),
    ("label", "f'{customer.tier.upper()}-{len(items)}-{\"X\" if shipping.express else \"S\"}'"),
]

METRICS = [
    {"host": "web-1", "cpu": [45.0, 52.5, 61.0], "mem": {"used_mb": 3100, "total_mb": 8192},
     "disk": {"/": 55, "/var": 61}, "errors": 3, "requests": 8800, "up": True, "role": "web", "lag_s": 0},
    {"host": "web-2", "cpu": [91.0, 95.5, 97.0], "mem": {"used_mb": 7900, "total_mb": 8192},
     "disk": {"/": 58, "/var": 93}, "errors": 240, "requests": 9100, "up": True, "role": "web", "lag_s": 0},
    {"host": "db-1", "cpu": [30.0, 35.5, 28.0], "mem": {"used_mb": 15000, "total_mb": 16384},
     "disk": {"/": 40, "/data": 88}, "errors": 0, "requests": 0, "up": True, "role": "primary", "lag_s": 0},
    {"host": "db-2", "cpu": [71.5, 88.0, 93.25], "mem": {"used_mb": 15872, "total_mb": 16384},
     "disk": {"/": 72, "/data": 91}, "errors": 17, "requests": 12000, "up": True, "role": "replica", "lag_s": 12.5},
    {"host": "cache-1", "cpu": [], "mem": {"used_mb": 0, "total_mb": 4096},
     "disk": {}, "errors": 0, "requests": 0, "up": False, "role": "cache", "lag_s": None},
]

ALERTS = [
    ("high_cpu", "critical", "len(cpu) > 0 and sum(cpu) / len(cpu) > 85"),
    ("cpu_spike", "warning", "any(c > 90 for c in cpu)"),
    ("mem", "warning", "mem.used_mb / mem.total_mb > 0.9"),
    ("disk", "critical", "any(p >= 90 for p in disk.values())"),
    ("error_rate", "critical", "errors / requests > 0.01"),
    ("replica_lag", "warning", "role == 'replica' and lag_s > 10"),
    ("down", "critical", "not up"),
    ("quiet", "info", "requests == 0 and role in ('web', 'primary')"),
    ("full_mounts", "info", "[m for m, p in disk.items() if p > 85]"),
]

USERS = [
    {"name": "Ada Lovelace", "email": "ada@example.com", "plan": "pro", "seats": 5, "used": 4,
     "renews_in": 3, "balance": 12.5, "locale": "en_GB", "tags": ["admin"]},
    {"name": "Grace Hopper", "email": "grace@example.com", "plan": "free", "seats": 1, "used": 1,
     "renews_in": 30, "balance": 0, "locale": "en_US", "tags": []},
    {"name": "Hedy Lamarr", "email": "hedy@example.at", "plan": "team", "seats": 20, "used": 21,
     "renews_in": -2, "balance": -48.0, "locale": "de_AT", "tags": ["beta", "eu"]},
]

TEMPLATES = [
    ("greeting", "f'Hi {name.split()[0]},'"),
    ("seats", "f'You are using {used} of {seats} seats ({used / seats:.0%}).'"),
    ("renewal", "f'Your {plan} plan renews in {renews_in} days.' if renews_in > 0 else f'Your {plan} plan lapsed {-renews_in} days ago.'"),
    ("balance", "f'Balance: {balance:+.2f} EUR' if balance else 'No balance due.'"),
    ("upsell", "'Upgrade to pro for more seats.' if plan == 'free' else ''"),
    ("over", "f'{used - seats} seat(s) over the limit!' if used > seats else 'ok'"),
    ("tags", "', '.join(tags) or '(none)'"),
    ("domain", "email.split('@')[1].upper()"),
    ("lang", "locale[:2] + (' (EU)' if locale[-2:] in ('GB', 'AT', 'DE') else '')"),
    ("broken", "f'{nickname}'"),
]

SHEET = [
    ("A1", "1200"),
    ("A2", "A1 * 1.05"),
    ("A3", "A2 * 1.05"),
    ("B1", "round(A1 + A2 + A3, 2)"),
    ("B2", "B1 / 3"),
    ("C1", "'growth' if A3 > A1 else 'flat'"),
    ("C2", "f'{B2:,.2f}'"),
    ("D1", "Z9 + 1"),
    ("D2", "A1 + undefined_name"),
    ("E1", "E2 + 1"),
    ("E2", "E1 + 1"),
    ("F1", "A2 > A1 and B1"),
    ("F2", "A1 + nope + B1"),
    ("G1", "C2.replace(',', '')"),
]


def write(rel, text):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def esc(s):
    return s.replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t")


def main():
    for name, doc in DOCS.items():
        write("docs/%s.json" % name, json.dumps(doc, indent=2) + "\n")
    lines = []
    for p, e, d in JOBS:
        lines.append("%s\t%s\t%s" % (p, esc(e), d))
    write("jobs.tsv", "\n".join(lines) + "\n")
    write("shop/orders.json", json.dumps(ORDERS, indent=1) + "\n")
    write("shop/pricing.tsv", "".join("%s\t%s\n" % (n, esc(e)) for n, e in PRICING))
    write("ops/hosts.json", json.dumps(METRICS, indent=1) + "\n")
    write("ops/alerts.tsv", "".join("%s\t%s\t%s\n" % (n, s, esc(e)) for n, s, e in ALERTS))
    write("mail/users.json", json.dumps(USERS, indent=1) + "\n")
    write("mail/templates.tsv", "".join("%s\t%s\n" % (n, esc(e)) for n, e in TEMPLATES))
    write("sheet.tsv", "".join("%s\t%s\n" % (n, esc(e)) for n, e in SHEET))


if __name__ == "__main__":
    main()
