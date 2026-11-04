"""The oracle for mini_ledger: the same ledger written plainly in Python
from the rules in README.md. Prints what the program prints, and writes
data/out/ledger.journal.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import os

ONE = 1000000
TYPES = ("Assets", "Liabilities", "Equity", "Income", "Expenses")
RANK = {"open": 0, "balance": 1, "txn": 2, "price": 2, "close": 3}


def rdiv(n, d):
    """n / d rounded half away from zero, d > 0."""
    q = (abs(n) * 2 + d) // (2 * d)
    return -q if n < 0 else q


def mul(a, b):
    return rdiv(a * b, ONE)


def round_to(x, prec):
    u = 10 ** (6 - prec)
    return rdiv(x, u) * u


def fmt_num(x, prec):
    x = round_to(x, prec)
    neg = x < 0
    x = abs(x)
    whole = x // ONE
    frac = x % ONE
    digits = str(whole)
    groups = []
    while len(digits) > 3:
        groups.insert(0, digits[-3:])
        digits = digits[:-3]
    groups.insert(0, digits)
    s = ",".join(groups)
    if prec > 0:
        s += "." + str(frac).rjust(6, "0")[:prec]
    if neg and x != 0:
        s = "-" + s
    return s


# ------------------------------------------------------------ dates

def leap(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def mdays(y, m):
    if m == 2:
        return 29 if leap(y) else 28
    return 30 if m in (4, 6, 9, 11) else 31


def valid_date(s):
    if len(s) != 10 or s[4] != "-" or s[7] != "-":
        return False
    y, m, d = s[:4], s[5:7], s[8:]
    if not (y.isdigit() and m.isdigit() and d.isdigit()):
        return False
    y, m, d = int(y), int(m), int(d)
    return 1 <= m <= 12 and 1 <= d <= mdays(y, m)


def next_day(s):
    y, m, d = int(s[:4]), int(s[5:7]), int(s[8:])
    d += 1
    if d > mdays(y, m):
        d = 1
        m += 1
        if m > 12:
            m = 1
            y += 1
    return f"{y:04d}-{m:02d}-{d:02d}"


# ------------------------------------------------------------ syntax

def is_upper(c):
    return "A" <= c <= "Z"


def is_digit(c):
    return "0" <= c <= "9"


def is_alnum(c):
    return is_upper(c) or is_digit(c) or "a" <= c <= "z"


def valid_account(s):
    parts = s.split(":")
    if len(parts) < 2 or parts[0] not in TYPES:
        return False
    for p in parts[1:]:
        if p == "" or not (is_upper(p[0]) or is_digit(p[0])):
            return False
        if not all(is_alnum(c) or c == "-" for c in p):
            return False
    return True


def valid_commodity(s):
    return 2 <= len(s) <= 10 and is_upper(s[0]) and all(is_upper(c) or is_digit(c) for c in s)


def parse_number(s):
    """(micro, decimals) or None."""
    neg = s.startswith("-")
    body = s[1:] if neg else s
    if body.count(".") > 1:
        return None
    whole, dot, frac = body.partition(".")
    if dot and frac == "":
        return None
    groups = whole.split(",")
    if len(groups) > 1:
        if not 1 <= len(groups[0]) <= 3 or any(len(g) != 3 for g in groups[1:]):
            return None
    whole = "".join(groups)
    if whole == "" or not all(is_digit(c) for c in whole):
        return None
    if not all(is_digit(c) for c in frac) or len(frac) > 6:
        return None
    v = int(whole) * ONE + (int(frac.ljust(6, "0")) if frac else 0)
    return (-v if neg else v, len(frac))


def parse_amount(s):
    """(micro, commodity, decimals) or None, from `NUMBER COMMODITY`."""
    toks = s.split()
    if len(toks) != 2 or not valid_commodity(toks[1]):
        return None
    n = parse_number(toks[0])
    if n is None:
        return None
    return (n[0], toks[1], n[1])


def strip_comment(line):
    i = line.find(";")
    return line if i < 0 else line[:i]


class ParseError(Exception):
    pass


def parse_posting(text):
    """{account, amount, cost, price} from a posting line's text."""
    text = text.strip()
    toks = text.split(None, 1)
    account = toks[0]
    if not valid_account(account):
        raise ParseError(f'bad account name "{account}"')
    rest = toks[1].strip() if len(toks) > 1 else ""
    p = {"account": account, "amount": None, "cost": None, "price": None}
    if rest == "":
        return p
    bad = ParseError(f'bad amount "{rest}"')
    left = rest
    i = rest.find("@")
    if i >= 0:
        left = rest[:i].strip()
        total = rest[i + 1:i + 2] == "@"
        pa = parse_amount(rest[i + 2:] if total else rest[i + 1:])
        if pa is None or pa[0] < 0:
            raise bad
        p["price"] = ("total" if total else "unit", pa)
    j = left.find("{")
    if j >= 0:
        k = left.find("}")
        if k < j or left[k + 1:].strip() != "":
            raise bad
        inner = left[j + 1:k].strip()
        left = left[:j].strip()
        if inner == "":
            p["cost"] = "any"
        else:
            ca = parse_amount(inner)
            if ca is None or ca[0] <= 0:
                raise bad
            p["cost"] = ca
    a = parse_amount(left)
    if a is None:
        raise bad
    p["amount"] = a
    if p["cost"] == "any" and a[0] > 0:
        raise ParseError("an added lot needs a cost")
    if p["price"] is not None and p["price"][0] == "total" and a[0] == 0:
        raise bad
    return p


def parse_journal(path, fidx, text):
    """(directives, errors) for one journal file."""
    out, errs = [], []
    txn = None
    skipping = False
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()

    def end():
        nonlocal txn
        if txn is not None and not txn.get("bad"):
            if not txn["postings"]:
                errs.append(f"{path}:{txn['line']}: transaction has no postings")
            else:
                out.append(txn)
        txn = None

    for n, raw in enumerate(lines, 1):
        if raw.strip() == "":
            end()
            skipping = False
            continue
        if raw.startswith("#"):
            continue
        line = strip_comment(raw).rstrip()
        if line.strip() == "":
            continue
        if raw[0] in " \t":
            if skipping:
                continue
            if txn is None:
                errs.append(f"{path}:{n}: posting outside a transaction")
                skipping = True
                continue
            if txn.get("bad"):
                continue
            try:
                p = parse_posting(line)
                p["line"] = n
                txn["postings"].append(p)
            except ParseError as e:
                errs.append(f"{path}:{n}: {e}")
                txn["bad"] = True
            continue
        end()
        skipping = False
        toks = line.split()
        date = toks[0]
        if not valid_date(date):
            if len(date) == 10 and date[4] == "-" and date[7] == "-":
                errs.append(f'{path}:{n}: bad date "{date}"')
            else:
                errs.append(f"{path}:{n}: cannot parse line")
            skipping = True
            continue
        if len(toks) < 2:
            errs.append(f"{path}:{n}: cannot parse line")
            skipping = True
            continue
        kind = toks[1]
        d = {"date": date, "file": path, "fidx": fidx, "line": n}
        try:
            if kind in ("*", "!"):
                head = line.split(None, 2)
                rest = head[2].strip() if len(head) > 2 else ""
                payee, _, narr = rest.partition("|")
                payee, narr = payee.strip(), narr.strip()
                if payee == "":
                    raise ParseError("transaction needs a payee")
                txn = dict(d, kind="txn", flag=kind, payee=payee, narration=narr, postings=[])
                continue
            if kind == "open":
                if len(toks) not in (3, 4):
                    raise ParseError("cannot parse line")
                if not valid_account(toks[2]):
                    raise ParseError(f'bad account name "{toks[2]}"')
                comms = toks[3].split(",") if len(toks) == 4 else []
                for c in comms:
                    if not valid_commodity(c):
                        raise ParseError(f'bad commodity "{c}"')
                out.append(dict(d, kind="open", account=toks[2], comms=comms))
            elif kind == "close":
                if len(toks) != 3:
                    raise ParseError("cannot parse line")
                if not valid_account(toks[2]):
                    raise ParseError(f'bad account name "{toks[2]}"')
                out.append(dict(d, kind="close", account=toks[2]))
            elif kind == "balance":
                if len(toks) != 5:
                    raise ParseError("cannot parse line")
                if not valid_account(toks[2]):
                    raise ParseError(f'bad account name "{toks[2]}"')
                a = parse_amount(" ".join(toks[3:]))
                if a is None:
                    raise ParseError(f'bad amount "{" ".join(toks[3:])}"')
                out.append(dict(d, kind="balance", account=toks[2], amount=a))
            elif kind == "price":
                if len(toks) != 5 or not valid_commodity(toks[2]):
                    raise ParseError("cannot parse line")
                a = parse_amount(" ".join(toks[3:]))
                if a is None or a[0] <= 0:
                    raise ParseError(f'bad amount "{" ".join(toks[3:])}"')
                out.append(dict(d, kind="price", comm=toks[2], amount=a))
            else:
                raise ParseError(f'unknown directive "{kind}"')
        except ParseError as e:
            errs.append(f"{path}:{n}: {e}")
            skipping = True
    end()
    return out, errs


# ------------------------------------------------------------ the bank import

def split_csv(line):
    fields, cur, i, q = [], "", 0, False
    while i < len(line):
        c = line[i]
        if q:
            if c == '"':
                if i + 1 < len(line) and line[i + 1] == '"':
                    cur += '"'
                    i += 1
                else:
                    q = False
            else:
                cur += c
        elif c == '"':
            q = True
        elif c == ",":
            fields.append(cur)
            cur = ""
        else:
            cur += c
        i += 1
    if q:
        return None
    fields.append(cur)
    return fields


def parse_rules(text):
    rules = {"account": None, "currency": None, "default": None, "match": []}
    for raw in text.split("\n"):
        line = raw.strip()
        if line == "" or line.startswith("#"):
            continue
        word, _, rest = line.partition(" ")
        rest = rest.strip()
        if word == "match":
            parts = [x.strip() for x in rest.split("=>")]
            payee = parts[2] if len(parts) > 2 else None
            rules["match"].append((parts[0].upper(), parts[1], payee))
        else:
            rules[word] = rest
    return rules


def import_csv(path, fidx, text, rules):
    """(directives, errors, summary line)."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    head = [h.strip().lower() for h in split_csv(lines[0])]
    col = {name: head.index(name) for name in ("date", "description", "amount", "balance")}
    rows, errs = [], []
    for n, line in enumerate(lines[1:], 2):
        f = split_csv(line)
        if f is None or len(f) != len(head):
            errs.append(f"{path}:{n}: cannot parse row")
            continue
        ds = f[col["date"]].strip()
        p = ds.split("/")
        date = f"{p[2]}-{p[0]}-{p[1]}" if len(p) == 3 and len(p[2]) == 4 and len(p[0]) == 2 and len(p[1]) == 2 else ""
        if not valid_date(date):
            errs.append(f'{path}:{n}: bad date "{ds}"')
            continue
        amts = []
        for key in ("amount", "balance"):
            s = f[col[key]].strip()
            neg = s.startswith("-")
            s = s[1:] if neg else s
            s = s[1:] if s.startswith("$") else s
            v = parse_number(s)
            if v is None:
                amts.append(None)
            else:
                amts.append((-v[0] if neg else v[0], v[1]))
        if amts[0] is None:
            errs.append(f'{path}:{n}: bad amount "{f[col["amount"]].strip()}"')
            continue
        desc = " ".join(f[col["description"]].split())
        rows.append((date, n, desc, amts[0], amts[1]))
    rows.sort(key=lambda r: (r[0], -r[1]))
    out = []
    matched = 0
    cur = rules["currency"]
    for date, n, desc, amt, _ in rows:
        account, payee, flag = rules["default"], desc, "!"
        for pat, acc, pay in rules["match"]:
            if pat in desc.upper():
                account, flag = acc, "*"
                if pay is not None:
                    payee = pay
                break
        if flag == "*":
            matched += 1
        out.append({"kind": "txn", "date": date, "file": path, "fidx": fidx, "line": n,
                    "flag": flag, "payee": payee, "narration": "",
                    "postings": [
                        {"account": rules["account"], "amount": (amt[0], cur, amt[1]), "cost": None, "price": None, "line": n},
                        {"account": account, "amount": None, "cost": None, "price": None, "line": n},
                    ]})
    if rows:
        newest = max(rows, key=lambda r: (r[0], -r[1]))
        if newest[4] is not None:
            out.append({"kind": "balance", "date": next_day(newest[0]), "file": path, "fidx": fidx,
                        "line": newest[1], "account": rules["account"], "amount": (newest[4][0], cur, newest[4][1])})
    summary = f"{path}: {len(rows)} rows, {matched} matched, {len(rows) - matched} to {rules['default']}"
    return out, errs, summary


# ------------------------------------------------------------ checking

def precisions(directives):
    prec = {}

    def see(a):
        prec[a[1]] = max(prec.get(a[1], 0), a[2])

    for d in directives:
        if d["kind"] == "txn":
            for p in d["postings"]:
                if p["amount"] is not None:
                    see(p["amount"])
        elif d["kind"] == "balance":
            see(d["amount"])
    return prec


def under(acc, root):
    return acc == root or acc.startswith(root + ":")


class Ledger:
    def __init__(self, directives):
        self.dirs = sorted(directives, key=lambda d: (d["date"], RANK[d["kind"]], d["fidx"], d["line"]))
        self.prec = precisions(directives)
        self.ever = {d["account"] for d in directives if d["kind"] == "open"}
        self.open = {}  # account -> commodities
        self.closed = set()
        self.bal = {}  # (account, comm) -> micro
        self.lots = {}  # (account, comm) -> [ [date, qty, cost, costcomm, scale] ]
        self.postings = []  # (date, payee, account, comm, qty)
        self.prices = []  # (date, comm, micro, target)
        self.accepted = []
        self.errors = []
        self.txns = 0
        self.refused = 0
        self.asserts = 0
        self.failed = 0

    def p(self, c):
        return self.prec.get(c, 2)

    def amt(self, x, c):
        return f"{fmt_num(x, self.p(c))} {c}"

    def err(self, d, msg):
        self.errors.append(f"{d['date']} {d['file']}:{d['line']}: {msg}")

    def run(self):
        for d in self.dirs:
            k = d["kind"]
            if k == "open":
                if d["account"] in self.open:
                    self.err(d, f"account {d['account']} is already open")
                    continue
                self.open[d["account"]] = d["comms"]
                self.accepted.append(d)
            elif k == "close":
                if d["account"] not in self.open or d["account"] in self.closed:
                    self.err(d, f"account {d['account']} is not open")
                    continue
                self.closed.add(d["account"])
                self.accepted.append(d)
            elif k == "price":
                a = d["amount"]
                self.prices.append((d["date"], d["comm"], a[0], a[1]))
                self.accepted.append(d)
            elif k == "balance":
                self.asserts += 1
                acc, (want, c, _) = d["account"], d["amount"]
                if not any(under(o, acc) for o in self.ever):
                    self.err(d, f"unknown account {acc}")
                    self.failed += 1
                    continue
                got = sum(v for (a, cc), v in self.bal.items() if cc == c and under(a, acc))
                self.accepted.append(d)
                if round_to(got, self.p(c)) != want:
                    self.failed += 1
                    self.err(d, f"balance failed: {acc} expected {self.amt(want, c)}, got {self.amt(got, c)}")
            else:
                self.txn(d)

    def txn(self, d):
        self.txns += 1
        msg = self.book(d)
        if msg is not None:
            self.refused += 1
            self.err(d, msg)

    def account_ok(self, acc, comm):
        if acc not in self.ever:
            return f"unknown account {acc}"
        if acc in self.closed:
            return f"account {acc} is closed"
        if acc not in self.open:
            return f"account {acc} is not open yet"
        comms = self.open[acc]
        if comm is not None and comms and comm not in comms:
            return f"account {acc} does not take {comm}"
        return None

    def book(self, d):
        ps = d["postings"]
        for p in ps:
            m = self.account_ok(p["account"], p["amount"][1] if p["amount"] else None)
            if m:
                return m
        elided = [p for p in ps if p["amount"] is None]
        if len(elided) > 1:
            return "more than one posting without an amount"
        lots = {}  # working copies
        weights = {}
        new_prices = []
        moves = []  # (account, comm, qty)
        for p in ps:
            if p["amount"] is None:
                continue
            q, c, _ = p["amount"]
            acc = p["account"]
            cost, price = p["cost"], p["price"]
            if price is not None:
                kind, (pv, pc, _) = price
                unit = pv if kind == "unit" else rdiv(pv * ONE, abs(q))
                new_prices.append((d["date"], c, unit, pc))
            if cost is not None:
                key = (acc, c)
                if key not in lots:
                    lots[key] = [list(x) for x in self.lots.get(key, [])]
                held = lots[key]
                if cost != "any" and q > 0:
                    cv, cc, cs = cost
                    held.append([d["date"], q, cv, cc, cs])
                    weights[cc] = weights.get(cc, 0) + mul(q, cv)
                else:
                    need = -q
                    pool = [x for x in held if cost == "any" or (x[2] == cost[0] and x[3] == cost[1])]
                    have = sum(x[1] for x in pool)
                    if have < need:
                        what = c if cost == "any" else f"{c} {{{fmt_num(cost[0], cost[2])} {cost[1]}}}"
                        return (f"not enough {what} in {acc}: have {fmt_num(have, self.p(c))}, "
                                f"need {fmt_num(need, self.p(c))}")
                    for x in pool:
                        if need == 0:
                            break
                        take = min(need, x[1])
                        x[1] -= take
                        need -= take
                        weights[x[3]] = weights.get(x[3], 0) - mul(take, x[2])
                    lots[key] = [x for x in held if x[1] > 0]
            elif price is not None:
                kind, (pv, pc, _) = price
                w = mul(q, pv) if kind == "unit" else (pv if q > 0 else -pv)
                weights[pc] = weights.get(pc, 0) + w
            else:
                weights[c] = weights.get(c, 0) + q
            moves.append((acc, c, q))
        left = {c: v for c, v in weights.items() if round_to(v, self.p(c)) != 0}
        filled = []
        if elided:
            if not left:
                return "nothing to fill in the posting without an amount"
            for c in sorted(left):
                m = self.account_ok(elided[0]["account"], c)
                if m:
                    return m
                filled.append((c, round_to(-left[c], self.p(c))))
        elif left:
            return "transaction does not balance: " + ", ".join(self.amt(left[c], c) for c in sorted(left))
        # commit
        for key, held in lots.items():
            self.lots[key] = held
        self.prices.extend(new_prices)
        out = []
        for p in ps:
            if p["amount"] is None:
                for c, v in filled:
                    out.append({"account": p["account"], "amount": (v, c, self.p(c)), "cost": None, "price": None})
                    moves.append((p["account"], c, v))
            else:
                out.append(p)
        for p in out:
            acc, (q, c, _) = p["account"], p["amount"]
            self.bal[(acc, c)] = self.bal.get((acc, c), 0) + q
            self.postings.append((d["date"], d["payee"], acc, c, q))
        self.accepted.append(dict(d, postings=out))
        return None


# ------------------------------------------------------------ writing back

def show_amount(a, ledger, own_scale):
    q, c, s = a
    return f"{fmt_num(q, s if own_scale else ledger.p(c))} {c}"


def canonical(d, L):
    k = d["kind"]
    if k == "open":
        return [f"{d['date']} open {d['account']}" + (" " + ",".join(d["comms"]) if d["comms"] else "")]
    if k == "close":
        return [f"{d['date']} close {d['account']}"]
    if k == "balance":
        return [f"{d['date']} balance {d['account']} {show_amount(d['amount'], L, False)}"]
    if k == "price":
        return [f"{d['date']} price {d['comm']} {show_amount(d['amount'], L, True)}"]
    head = f"{d['date']} {d['flag']} {d['payee']}" + (f" | {d['narration']}" if d["narration"] else "")
    out = [head]
    for p in d["postings"]:
        s = f"  {p['account']}  {show_amount(p['amount'], L, False)}"
        if p["cost"] == "any":
            s += " {}"
        elif p["cost"] is not None:
            s += " {" + show_amount(p["cost"], L, True) + "}"
        if p["price"] is not None:
            kind, a = p["price"]
            s += (" @ " if kind == "unit" else " @@ ") + show_amount(a, L, True)
        out.append(s)
    return out + [""]


# ------------------------------------------------------------ reports

def nonzero(L, amounts):
    return {c: v for c, v in amounts.items() if round_to(v, L.p(c)) != 0}


def tree_rows(L, roots, totals, depth):
    """Rows of (account, amounts) for a tree under roots, in tree order."""
    names = set()
    for acc in L.ever:
        parts = acc.split(":")
        for i in range(1, len(parts) + 1):
            names.add(":".join(parts[:i]))
    for acc, _ in L.bal:
        parts = acc.split(":")
        for i in range(1, len(parts) + 1):
            names.add(":".join(parts[:i]))
    rows = []
    for root in roots:
        sub = sorted((n for n in names if under(n, root)), key=lambda n: n.split(":"))
        base = len(root.split(":"))
        for n in sub:
            seg = len(n.split(":"))
            if depth is not None and seg > depth:
                continue
            sums = {}
            for (a, c), v in totals.items():
                if under(a, n):
                    sums[c] = sums.get(c, 0) + v
            amounts = nonzero(L, sums)
            if amounts:
                rows.append((n, seg - base, amounts))
    return rows


def sum_by_comm(L, pairs):
    s = {}
    for (a, c), v in pairs.items():
        s[c] = s.get(c, 0) + v
    return s


def print_tree(L, out, rows):
    for n, level, amounts in rows:
        first = True
        for c in sorted(amounts):
            a = L.amt(amounts[c], c).rjust(20)
            out.append(f"{a}  {'  ' * level}{n.split(':')[-1]}" if first else a)
            first = False


def totals_at(L, frm, to, roots):
    t = {}
    for date, _, acc, c, q in L.postings:
        if (frm is None or date >= frm) and (to is None or date <= to) and any(under(acc, r) for r in roots):
            t[(acc, c)] = t.get((acc, c), 0) + q
    return t


def known(L, acc):
    return any(under(o, acc) for o in L.ever)


def price_of(L, c, target, at):
    direct = inverse = None
    for date, pc, v, t in L.prices:
        if date > at:
            continue
        if pc == c and t == target:
            direct = v
        elif pc == target and t == c:
            inverse = v
    return direct, inverse


def check_period(pos):
    for x in pos:
        if not valid_date(x):
            raise ParseError(f'bad date "{x}"')
    if pos[1] < pos[0]:
        raise ParseError("the period ends before it starts")
    return pos[0], pos[1]


def report(L, line, out):
    toks = line.split()
    cmd, args = toks[0], toks[1:]
    opts, pos = {}, []
    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            if i + 1 >= len(args):
                raise ParseError(f"{args[i]} needs a value")
            opts[args[i][2:]] = args[i + 1]
            i += 2
        else:
            pos.append(args[i])
            i += 1
    for k in ("at", "from", "to"):
        if k in opts and not valid_date(opts[k]):
            raise ParseError(f'bad date "{opts[k]}"')
    if cmd == "balance":
        depth = None
        if "depth" in opts:
            if not opts["depth"].isdigit() or int(opts["depth"]) == 0:
                raise ParseError(f'bad depth "{opts["depth"]}"')
            depth = int(opts["depth"])
        roots = pos or sorted({a.split(":")[0] for a in L.ever}, key=TYPES.index)
        t = totals_at(L, None, opts.get("at"), roots)
        rows = tree_rows(L, roots, t, depth)
        print_tree(L, out, rows)
        out.append("-" * 20)
        total = nonzero(L, sum_by_comm(L, t))
        if not total:
            out.append("0".rjust(20))
        for c in sorted(total):
            out.append(L.amt(total[c], c).rjust(20))
    elif cmd == "register":
        if len(pos) != 1:
            raise ParseError("register takes one account")
        acc = pos[0]
        if not known(L, acc):
            raise ParseError(f"no account {acc}")
        run = {}
        for date, payee, a, c, q in L.postings:
            if not under(a, acc):
                continue
            if "from" in opts and date < opts["from"] or "to" in opts and date > opts["to"]:
                continue
            run[c] = run.get(c, 0) + q
            out.append(f"{date} {payee[:20].ljust(20)} {a[:28].ljust(28)} "
                       f"{L.amt(q, c).rjust(16)} {L.amt(run[c], c).rjust(16)}")
    elif cmd == "value":
        if len(pos) != 1 or not valid_commodity(pos[0]):
            raise ParseError("value takes a commodity")
        target = pos[0]
        at = opts.get("at", "9999-12-31")
        roots = ["Assets", "Liabilities"]
        t = totals_at(L, None, at, roots)
        total = 0
        for (acc, c) in sorted(t, key=lambda k: (k[0].split(":"), k[1])):
            q = t[(acc, c)]
            if round_to(q, L.p(c)) == 0:
                continue
            if c == target:
                v = q
            else:
                direct, inverse = price_of(L, c, target, at)
                if direct is not None:
                    v = mul(q, direct)
                elif inverse is not None:
                    v = rdiv(q * ONE, inverse)
                else:
                    out.append(f"{L.amt(q, c).rjust(20)}  {acc}  (no price in {target})")
                    continue
            total += v
            line = f"{L.amt(v, target).rjust(20)}  {acc}"
            if c != target:
                line += f"  ({L.amt(q, c)})"
            out.append(line)
        out.append("-" * 20)
        out.append(L.amt(total, target).rjust(20))
    elif cmd == "income":
        if len(pos) != 2:
            raise ParseError("income takes two dates")
        frm, to = check_period(pos)
        roots = ["Income", "Expenses"]
        t = totals_at(L, frm, to, roots)
        print_tree(L, out, tree_rows(L, roots, t, None))
        out.append("-" * 20)
        net = nonzero(L, {c: -v for c, v in sum_by_comm(L, t).items()})
        if not net:
            out.append(f"{'0'.rjust(20)}  net income")
        for c in sorted(net):
            out.append(f"{L.amt(net[c], c).rjust(20)}  net income")
    elif cmd == "lots":
        if len(pos) != 1:
            raise ParseError("lots takes one account")
        acc = pos[0]
        if not known(L, acc):
            raise ParseError(f"no account {acc}")
        for (a, c) in sorted(L.lots, key=lambda k: (k[0].split(":"), k[1])):
            held = L.lots[(a, c)]
            if not under(a, acc) or not held:
                continue
            out.append(f"{a} {c}")
            for date, q, cv, cc, cs in held:
                out.append(f"  {date}  {L.amt(q, c)} {{{fmt_num(cv, cs)} {cc}}}  {L.amt(mul(q, cv), cc)}")
    elif cmd == "print":
        if len(pos) != 2:
            raise ParseError("print takes two dates")
        frm, to = check_period(pos)
        for d in L.accepted:
            if frm <= d["date"] <= to:
                out.extend(canonical(d, L))
    else:
        raise ParseError(f'unknown command "{cmd}"')


# ------------------------------------------------------------ main

def load(names, texts):
    """(directives, lines to print)."""
    dirs, lines = [], []
    rules = parse_rules(texts["bank.rules"]) if "bank.rules" in texts else None
    for fidx, name in enumerate(names):
        path = f"data/{name}"
        if name.endswith(".journal"):
            ds, errs = parse_journal(path, fidx, texts[name])
            lines.append(f"{path}: {len(ds)} directives")
        else:
            ds, errs, summary = import_csv(path, fidx, texts[name], rules)
            lines.append(summary)
        lines.extend(errs)
        dirs.extend(ds)
    return dirs, lines


def balances(L):
    return {k: v for k, v in L.bal.items() if v != 0}


def main():
    names = sorted(n for n in os.listdir("data") if n.endswith(".journal") or n.endswith(".csv"))
    texts = {}
    for n in os.listdir("data"):
        if os.path.isfile(os.path.join("data", n)):
            with open(os.path.join("data", n), encoding="utf-8", newline="") as fh:
                texts[n] = fh.read()
    out = ["== load"]
    dirs, lines = load(names, texts)
    out.extend(lines)
    L = Ledger(dirs)
    L.run()
    out.append("== check")
    out.extend(L.errors)
    out.append(f"{len(L.dirs)} directives, {L.txns} transactions, {L.refused} refused, "
               f"{L.asserts} balance assertions, {L.failed} failed")
    text = []
    for d in L.accepted:
        text.extend(canonical(d, L))
    body = "\n".join(text) + "\n"
    os.makedirs("data/out", exist_ok=True)
    with open("data/out/ledger.journal", "w", encoding="utf-8", newline="") as fh:
        fh.write(body)
    out.append("== write")
    out.append(f"data/out/ledger.journal: {len(L.accepted)} directives, {len(body.encode())} bytes")
    with open("data/out/ledger.journal", encoding="utf-8", newline="") as fh:
        back = fh.read()
    ds, errs = parse_journal("data/out/ledger.journal", 0, back)
    R = Ledger(ds)
    R.run()
    if errs:
        out.append(f"round trip: {len(errs)} parse errors")
    a, b = balances(L), balances(R)
    diff = sorted(set(a) | set(b), key=lambda k: (k[0].split(":"), k[1]))
    diff = [k for k in diff if a.get(k, 0) != b.get(k, 0)]
    if diff:
        out.append(f"round trip: {diff[0][0]} differs in {diff[0][1]}")
    else:
        out.append(f"round trip: {len(ds)} directives, {len(R.errors)} reported again, every balance matches")
    out.append("== reports")
    for raw in texts["reports.txt"].split("\n"):
        line = raw.strip()
        if line == "" or line.startswith("#"):
            continue
        out.append(f"> {line}")
        try:
            report(L, line, out)
        except ParseError as e:
            out.append(f"error: {e}")
    print("\n".join(out))


main()
