# Runs data/jobs.tsv through sortedcontainers 2.4.0 (the sortedcontainers/
# package next to this file, unchanged) and prints what it did.
# mini_sortedcontainers.kara must print the same bytes.
#
# A trace job reads a command trace (see mk.py) and prints one line for
# each command: what it returned, or the exception it raised. "shape"
# prints the container's sublists, maxes and positional index, which are
# part of how sortedcontainers works rather than of its API, so the port
# has to split, merge and index exactly as it does.
#
# A key function's repr names its address, which changes every run; it
# prints as "<function name>".
import os
import re
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from sortedcontainers import SortedDict, SortedKeyList, SortedList, SortedSet  # noqa: E402

OUT = []


def emit(s):
    OUT.append(s)


def clean(s):
    return re.sub(r" at 0x[0-9a-fA-F]+>", ">", s)


def err(e):
    return "error: %s: %s" % (type(e).__name__, clean(str(e)))


def read(rel):
    with open(os.path.join(HERE, "data", rel), encoding="utf-8") as f:
        return f.read()


def mod10(x):
    return x % 10


def neg(x):
    return -x


KEYS = {"mod10": mod10, "neg": neg}


def arg(s):
    return None if s == "_" else int(s)


def shape(sl):
    if isinstance(sl, SortedKeyList):
        s = "lists: %s keys: %s" % (sl._lists, sl._keys)
    else:
        s = "lists: %s" % sl._lists
    return s + " index: %s offset: %d" % (sl._index, sl._offset)


def ints(xs):
    return [int(x) for x in xs]


def list_cmd(sl, c, a):
    if c == "add":
        return sl.add(int(a[0]))
    if c == "update":
        return sl.update(ints(a))
    if c == "discard":
        return sl.discard(int(a[0]))
    if c == "remove":
        return sl.remove(int(a[0]))
    if c == "pop":
        return sl.pop(*ints(a))
    if c == "get":
        return sl[int(a[0])]
    if c == "slice":
        return sl[arg(a[0]):arg(a[1]):arg(a[2])]
    if c == "del":
        del sl[int(a[0])]
        return None
    if c == "delslice":
        del sl[arg(a[0]):arg(a[1]):arg(a[2])]
        return None
    if c == "contains":
        return int(a[0]) in sl
    if c == "count":
        return sl.count(int(a[0]))
    if c == "index":
        return sl.index(*ints(a))
    if c == "bl":
        return sl.bisect_left(int(a[0]))
    if c == "br":
        return sl.bisect_right(int(a[0]))
    if c == "bkl":
        return sl.bisect_key_left(int(a[0]))
    if c == "bkr":
        return sl.bisect_key_right(int(a[0]))
    if c in ("irange", "irangekey"):
        f = sl.irange if c == "irange" else sl.irange_key
        return list(f(arg(a[0]), arg(a[1]), (a[2] == "1", a[3] == "1"), a[4] == "1"))
    if c == "islice":
        return list(sl.islice(arg(a[0]), arg(a[1]), a[2] == "1"))
    if c == "rev":
        return list(reversed(sl))
    if c == "plus":
        return sl + ints(a)
    if c == "times":
        return sl * int(a[0])
    if c == "cmp":
        other = ints(a[1:])
        return {"==": sl.__eq__, "!=": sl.__ne__, "<": sl.__lt__, "<=": sl.__le__,
                ">": sl.__gt__, ">=": sl.__ge__}[a[0]](other)
    if c == "setitem":
        sl[int(a[0])] = int(a[1])
        return None
    if c == "append":
        return sl.append(int(a[0]))
    if c == "extend":
        return sl.extend([int(a[0])])
    if c == "insert":
        return sl.insert(int(a[0]), int(a[1]))
    if c == "reverse":
        return sl.reverse()
    if c == "reset":
        return sl._reset(int(a[0]))
    if c == "clear":
        return sl.clear()
    if c == "len":
        return len(sl)
    raise AssertionError(c)


def pairs(a):
    return [(int(a[i]), a[i + 1]) for i in range(0, len(a), 2)]


def dict_cmd(d, c, a):
    if c == "set":
        d[int(a[0])] = a[1]
        return None
    if c == "del":
        del d[int(a[0])]
        return None
    if c == "pop":
        return d.pop(int(a[0]), *a[1:])
    if c == "popitem":
        return d.popitem(*ints(a))
    if c == "peek":
        return d.peekitem(*ints(a))
    if c == "setdefault":
        return d.setdefault(int(a[0]), a[1])
    if c == "get":
        return d[int(a[0])]
    if c == "in":
        return int(a[0]) in d
    if c == "keys":
        return d.keys()[int(a[0])]
    if c == "items":
        return d.items()[int(a[0])]
    if c == "values":
        return d.values()[int(a[0])]
    if c == "keyslice":
        return d.keys()[arg(a[0]):arg(a[1]):arg(a[2])]
    if c == "itemslice":
        return d.items()[arg(a[0]):arg(a[1]):arg(a[2])]
    if c == "valueslice":
        return d.values()[arg(a[0]):arg(a[1]):arg(a[2])]
    if c in ("delkey", "delitem", "delvalue"):
        view = {"delkey": d.keys, "delitem": d.items, "delvalue": d.values}[c]()
        del view[int(a[0])]
        return None
    if c == "delkeyslice":
        del d.keys()[arg(a[0]):arg(a[1]):arg(a[2])]
        return None
    if c == "bl":
        return d.bisect_left(int(a[0]))
    if c == "br":
        return d.bisect_right(int(a[0]))
    if c == "index":
        return d.index(int(a[0]))
    if c == "irange":
        return list(d.irange(arg(a[0]), arg(a[1]), (a[2] == "1", a[3] == "1"), a[4] == "1"))
    if c == "islice":
        return list(d.islice(arg(a[0]), arg(a[1]), a[2] == "1"))
    if c == "update":
        return d.update(pairs(a))
    if c == "or":
        return d | dict(pairs(a))
    if c == "ror":
        return dict(pairs(a)) | d
    if c == "copy":
        return d.copy()
    if c == "clear":
        return d.clear()
    if c == "len":
        return len(d)
    raise AssertionError(c)


def set_cmd(s, c, a):
    if c == "add":
        return s.add(int(a[0]))
    if c == "discard":
        return s.discard(int(a[0]))
    if c == "remove":
        return s.remove(int(a[0]))
    if c == "pop":
        return s.pop(*ints(a))
    if c == "get":
        return s[int(a[0])]
    if c == "slice":
        return s[arg(a[0]):arg(a[1]):arg(a[2])]
    if c == "del":
        del s[int(a[0])]
        return None
    if c == "delslice":
        del s[arg(a[0]):arg(a[1]):arg(a[2])]
        return None
    if c == "in":
        return int(a[0]) in s
    if c == "count":
        return s.count(int(a[0]))
    if c == "index":
        return s.index(int(a[0]))
    if c == "bl":
        return s.bisect_left(int(a[0]))
    if c == "br":
        return s.bisect_right(int(a[0]))
    if c == "irange":
        return list(s.irange(arg(a[0]), arg(a[1]), (a[2] == "1", a[3] == "1"), a[4] == "1"))
    if c == "islice":
        return list(s.islice(arg(a[0]), arg(a[1]), a[2] == "1"))
    vs = ints(a)
    if c == "union":
        return s.union(vs)
    if c == "inter":
        return s.intersection(vs)
    if c == "diff":
        return s.difference(vs)
    if c == "symdiff":
        return s.symmetric_difference(vs)
    if c == "subset":
        return s.issubset(vs)
    if c == "superset":
        return s.issuperset(vs)
    if c == "disjoint":
        return s.isdisjoint(vs)
    if c in ("eq", "lt", "le", "gt", "ge"):
        return {"eq": s.__eq__, "lt": s.__lt__, "le": s.__le__, "gt": s.__gt__, "ge": s.__ge__}[c](set(vs))
    if c == "update":
        return s.update(vs)
    if c == "diff_update":
        return s.difference_update(vs)
    if c == "inter_update":
        return s.intersection_update(vs)
    if c == "symdiff_update":
        return s.symmetric_difference_update(vs)
    if c == "copy":
        return s.copy()
    if c == "clear":
        return s.clear()
    if c == "len":
        return len(s)
    raise AssertionError(c)


def trace_job(rel):
    lines = read(rel).splitlines()
    head = lines[0].split()
    if head[0] == "list":
        obj = SortedList()
        obj._reset(int(head[1]))
        run, inner = list_cmd, lambda: obj
    elif head[0] == "keylist":
        obj = SortedKeyList(key=KEYS[head[1]])
        obj._reset(int(head[2]))
        run, inner = list_cmd, lambda: obj
    elif head[0] == "dict":
        obj = SortedDict()
        obj._reset(int(head[1]))
        run, inner = dict_cmd, lambda: obj._list
    else:
        obj = SortedSet()
        obj._reset(int(head[1]))
        run, inner = set_cmd, lambda: obj._list
    for line in lines[1:]:
        f = line.split()
        c, a = f[0], f[1:]
        if c == "shape":
            emit("%s: %s" % (line, shape(inner())))
            continue
        if c == "check":
            obj._check()
            emit("check: ok")
            continue
        if c == "repr":
            emit("repr: " + clean(repr(obj)))
            continue
        try:
            r = run(obj, c, a)
        except Exception as e:
            emit("%s: %s" % (line, err(e)))
            continue
        emit("%s: %s" % (line, clean(repr(r))))


# ------------------------------------------------------------ order book

def orderbook_job(rel):
    bids = SortedDict()
    asks = SortedDict()
    where = {}
    rows = read(rel).splitlines()[1:]

    def match(buy, oid, limit, qty):
        book = asks if buy else bids
        while qty > 0 and book:
            price, level = book.peekitem(0 if buy else -1)
            if limit is not None and (price > limit if buy else price < limit):
                break
            head = level[0]
            take = min(qty, head[1])
            if buy:
                emit("  trade buy %d sell %d %d @ %d" % (oid, head[0], take, price))
            else:
                emit("  trade buy %d sell %d %d @ %d" % (head[0], oid, take, price))
            head[1] -= take
            qty -= take
            if head[1] == 0:
                level.pop(0)
                del where[head[0]]
            if not level:
                del book[price]
        return qty

    def depth(book, top):
        keys = list(reversed(book.keys()[-3:])) if top else book.keys()[:3]
        return " ".join("%d x %d" % (p, sum(q for _, q in book[p])) for p in keys)

    for n, row in enumerate(rows, 1):
        oid, side, kind, price, qty = row.split(",")
        oid = int(oid)
        if side == "cancel":
            target = int(kind)
            if target not in where:
                emit("#%d cancel %d: not resting" % (oid, target))
            else:
                tside, tprice = where.pop(target)
                book = bids if tside == "buy" else asks
                level = book[tprice]
                for i, entry in enumerate(level):
                    if entry[0] == target:
                        emit("#%d cancel %d: %d left at %d" % (oid, target, entry[1], tprice))
                        del level[i]
                        break
                if not level:
                    del book[tprice]
        else:
            buy = side == "buy"
            qty = int(qty)
            if kind == "market":
                emit("#%d market %s %d" % (oid, side, qty))
                rest = match(buy, oid, None, qty)
                if rest:
                    emit("  unfilled %d" % rest)
            else:
                price = int(price)
                emit("#%d limit %s %d @ %d" % (oid, side, qty, price))
                rest = match(buy, oid, price, qty)
                if rest:
                    own = bids if buy else asks
                    own.setdefault(price, []).append([oid, rest])
                    where[oid] = (side, price)
                    emit("  rests %d" % rest)
        if n % 50 == 0:
            emit("book after %d orders" % n)
            emit("  bids: " + depth(bids, True))
            emit("  asks: " + depth(asks, False))
            if bids and asks:
                bb = bids.peekitem(-1)[0]
                ba = asks.peekitem(0)[0]
                emit("  spread %d mid %s" % (ba - bb, (bb + ba) / 2))
                emit("  levels within 25 of mid: bids %d asks %d" % (
                    len(list(bids.irange(bb - 25, bb))), asks.bisect_right(ba + 25)))
    emit("resting orders: %d" % len(where))
    emit("bid levels: %s" % list(bids.keys()))
    emit("ask levels: %s" % list(asks.keys()))
    if bids:
        emit("best bid: %r" % (bids.peekitem(-1),))
    if asks:
        emit("best ask: %r" % (asks.peekitem(0),))


# ----------------------------------------------------------- leaderboard

def rank_key(entry):
    return (-entry[1], entry[0])


def leaderboard_job(rel):
    totals = {}
    board = SortedKeyList(key=rank_key)
    for n, line in enumerate(read(rel).splitlines(), 1):
        t, player, pts = line.split()
        old = totals.get(player)
        if old is not None:
            board.remove((player, old))
            new = old + int(pts)
        else:
            new = int(pts)
        totals[player] = new
        board.add((player, new))
        if n % 30 == 0:
            emit("t=%s after %d events" % (t, n))
            emit("  top 5: " + ", ".join("%s %d" % e for e in board[:5]))
            emit("  bottom 3: " + ", ".join("%s %d" % e for e in reversed(board[-3:])))
            emit("  rank of %s: %d of %d" % (player, board.index((player, new)) + 1, len(board)))
            emit("  at 100 or more: %d" % board.bisect_key_left((-99, "")))
            band = [e[0] for e in board.irange_key((-200, ""), (-100, "~"))]
            emit("  between 100 and 200: " + " ".join(band))
            emit("  same total as %s: %d" % (player, len(list(board.irange_key((-new, ""), (-new, "~"))))))
    emit("final: " + clean(repr(board)))


# --------------------------------------------------------------- latency

def latency_job(rel):
    window = deque()
    win = SortedList()
    routes = {}
    alerting = False
    for n, line in enumerate(read(rel).splitlines(), 1):
        ts, route, ms = line.split()
        ms = int(ms)
        window.append(ms)
        win.add(ms)
        if len(window) > 50:
            win.remove(window.popleft())
        routes.setdefault(route, SortedList()).add(ms)
        if n % 25 == 0:
            k = len(win)
            p50, p95, p99 = win[k // 2], win[k * 95 // 100], win[k * 99 // 100]
            slow = k - win.bisect_right(250)
            emit("%s n=%d p50=%d p95=%d p99=%d max=%d slow=%d" % (ts, n, p50, p95, p99, win[-1], slow))
            if p95 > 400 and not alerting:
                alerting = True
                emit("  ALERT p95 %d ms over 400" % p95)
            elif p95 <= 400 and alerting:
                alerting = False
                emit("  resolved")
    for route in sorted(routes):
        sl = routes[route]
        k = len(sl)
        emit("%s count=%d p50=%d p99=%d top=%s under10=%d" % (
            route.replace("_", " "), k, sl[k // 2], sl[k * 99 // 100], list(reversed(sl[-3:])), sl.bisect_left(10)))


# --------------------------------------------------------------- booking

def hm(m):
    return "%02d:%02d" % (m // 60, m % 60)


def booking_job(rel):
    rooms = {}
    for line in read(rel).splitlines():
        f = line.split()
        cal = rooms.setdefault(f[1], SortedDict())
        if f[0] == "book":
            s, e, who = int(f[2]), int(f[3]), f[4]
            i = cal.bisect_right(s)
            clash = None
            if i > 0:
                ps, (pe, pw) = cal.peekitem(i - 1)
                if pe > s:
                    clash = (ps, pe, pw)
            if clash is None and i < len(cal):
                ns, (ne, nw) = cal.peekitem(i)
                if ns < e:
                    clash = (ns, ne, nw)
            if clash:
                emit("%s %s %s-%s %s: clashes with %s-%s %s" % (f[0], f[1], hm(s), hm(e), who, hm(clash[0]), hm(clash[1]), clash[2]))
            else:
                cal[s] = (e, who)
                emit("%s %s %s-%s %s: booked, #%d of the day" % (f[0], f[1], hm(s), hm(e), who, cal.index(s) + 1))
        elif f[0] == "cancel":
            s = int(f[2])
            if s in cal:
                e, who = cal.pop(s)
                emit("cancel %s %s: %s's booking until %s" % (f[1], hm(s), who, hm(e)))
            else:
                later = list(cal.irange(minimum=s, inclusive=(False, True)))[:1]
                emit("cancel %s %s: nothing starts then%s" % (
                    f[1], hm(s), "; next at " + hm(later[0]) if later else ""))
        elif f[0] == "free":
            need = int(f[2])
            gaps = []
            t = 480
            for s, (e, _) in cal.items():
                if s - t >= need:
                    gaps.append("%s-%s" % (hm(t), hm(s)))
                t = max(t, e)
            if 1080 - t >= need:
                gaps.append("%s-%s" % (hm(t), hm(1080)))
            emit("free %s %d min: %s" % (f[1], need, " ".join(gaps[:4]) if gaps else "none"))
        else:
            emit("agenda %s (%d)" % (f[1], len(cal)))
            for s, (e, who) in cal.items():
                emit("  %s-%s %s" % (hm(s), hm(e), who))


def main():
    for line in read("jobs.tsv").splitlines():
        job = line.split("\t")
        emit("== " + " ".join(job))
        {"trace": trace_job, "orderbook": orderbook_job, "leaderboard": leaderboard_job,
         "latency": latency_job, "booking": booking_job}[job[0]](job[1])
    sys.stdout.write("".join(s + "\n" for s in OUT))


if __name__ == "__main__":
    main()
