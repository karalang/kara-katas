# Writes data/: the inputs of four programs built on sorted containers (a
# limit order book, a game leaderboard, a latency monitor and a room
# booking calendar), command traces that drive SortedList, SortedKeyList,
# SortedDict and SortedSet through their whole API, and data/jobs.tsv,
# the jobs mini_sortedcontainers.kara and oracle.py run.
#
# The traces use a load factor of 4, so a few dozen values already span
# many sublists, and they print the sublists and the positional index as
# they go. A trace line is a command and its arguments; "_" stands for
# None.
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def write(rel, text):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def opt(r, lo, hi):
    return "_" if r.random() < 0.2 else str(r.randint(lo, hi))


def slice_args(r, n):
    step = r.choice(["_", "_", "_", "1", "2", "3", "-1", "-2", "0"])
    return "%s %s %s" % (opt(r, -n - 2, n + 2), opt(r, -n - 2, n + 2), step)


def list_trace(seed, ops, header, keyed):
    r = random.Random(seed)
    out = [header]
    n = 0
    for i in range(ops):
        if i % 40 == 39:
            out.append("shape")
            out.append("check")
            continue
        c = r.random()
        v = str(r.randint(-30, 60))
        if c < 0.30:
            out.append("add " + v)
            n += 1
        elif c < 0.34:
            k = r.randint(1, 12) if r.random() < 0.7 else r.randint(10, 60)
            out.append("update " + " ".join(str(r.randint(-30, 60)) for _ in range(k)))
            n += k
        elif c < 0.40:
            out.append("discard " + v)
        elif c < 0.45:
            out.append("remove " + v)
        elif c < 0.50:
            out.append("pop" + ("" if r.random() < 0.3 else " " + str(r.randint(-n - 3, n + 3))))
        elif c < 0.54:
            out.append("get " + str(r.randint(-n - 3, n + 3)))
        elif c < 0.58:
            out.append("slice " + slice_args(r, n))
        elif c < 0.61:
            out.append("del " + str(r.randint(-n - 3, n + 3)))
        elif c < 0.64:
            out.append("delslice " + slice_args(r, n))
        elif c < 0.67:
            out.append("contains " + v)
        elif c < 0.70:
            out.append("count " + v)
        elif c < 0.74:
            extra = ""
            if r.random() < 0.5:
                extra = " " + str(r.randint(-n - 3, n + 3))
                if r.random() < 0.5:
                    extra += " " + str(r.randint(-n - 3, n + 3))
            out.append("index " + v + extra)
        elif c < 0.77:
            out.append(r.choice(["bl ", "br "]) + v)
        elif c < 0.80 and keyed:
            out.append(r.choice(["bkl ", "bkr "]) + str(r.randint(-12, 12)))
        elif c < 0.85:
            lo = opt(r, -30, 60)
            hi = opt(r, -30, 60)
            cmd = "irangekey" if keyed and r.random() < 0.5 else "irange"
            if cmd == "irangekey":
                lo = opt(r, -12, 12)
                hi = opt(r, -12, 12)
            out.append("%s %s %s %d %d %d" % (cmd, lo, hi, r.randint(0, 1), r.randint(0, 1), r.randint(0, 1)))
        elif c < 0.89:
            out.append("islice %s %s %d" % (opt(r, -n - 2, n + 2), opt(r, -n - 2, n + 2), r.randint(0, 1)))
        elif c < 0.90:
            out.append("rev")
        elif c < 0.91:
            out.append("plus " + " ".join(str(r.randint(-30, 60)) for _ in range(r.randint(0, 3))))
        elif c < 0.92:
            out.append("times " + str(r.randint(0, 2)))
        elif c < 0.94:
            op = r.choice(["==", "!=", "<", "<=", ">", ">="])
            out.append("cmp " + op + " " + " ".join(str(r.randint(-30, 60)) for _ in range(r.randint(0, 4))))
        elif c < 0.95:
            out.append(r.choice(["setitem 0 1", "append 3", "extend 4", "insert 0 5", "reverse"]))
        elif c < 0.96:
            out.append("reset " + str(r.choice([4, 5, 8])))
        elif c < 0.965:
            out.append("clear")
            n = 0
        elif c < 0.98:
            out.append("len")
        else:
            out.append("repr")
    out.append("shape")
    out.append("check")
    out.append("repr")
    return "\n".join(out) + "\n"


WORDS = ["ash", "birch", "cedar", "elm", "fir", "hazel", "larch", "maple", "oak", "pine", "rowan", "yew"]


def dict_trace(seed, ops):
    r = random.Random(seed)
    out = ["dict 4"]
    for i in range(ops):
        if i % 40 == 39:
            out.append("shape")
            out.append("check")
            continue
        c = r.random()
        k = str(r.randint(0, 80))
        w = r.choice(WORDS)
        if c < 0.35:
            out.append("set %s %s" % (k, w))
        elif c < 0.40:
            out.append("del " + k)
        elif c < 0.45:
            out.append("pop " + k + ("" if r.random() < 0.5 else " " + w))
        elif c < 0.50:
            out.append("popitem" + ("" if r.random() < 0.4 else " " + str(r.randint(-12, 12))))
        elif c < 0.54:
            out.append("peek" + ("" if r.random() < 0.4 else " " + str(r.randint(-12, 12))))
        elif c < 0.57:
            out.append("setdefault %s %s" % (k, w))
        elif c < 0.61:
            out.append("get " + k)
        elif c < 0.63:
            out.append("in " + k)
        elif c < 0.66:
            out.append(r.choice(["keys", "items", "values"]) + " " + str(r.randint(-12, 12)))
        elif c < 0.70:
            out.append(r.choice(["keyslice", "itemslice", "valueslice"]) + " " + slice_args(r, 12))
        elif c < 0.72:
            out.append(r.choice(["delkey ", "delitem ", "delvalue "]) + str(r.randint(-12, 12)))
        elif c < 0.74:
            out.append("delkeyslice " + slice_args(r, 12))
        elif c < 0.77:
            out.append(r.choice(["bl ", "br ", "index "]) + k)
        elif c < 0.80:
            out.append("irange %s %s %d %d %d" % (opt(r, 0, 80), opt(r, 0, 80), r.randint(0, 1), r.randint(0, 1), r.randint(0, 1)))
        elif c < 0.83:
            out.append("islice %s %s %d" % (opt(r, -14, 14), opt(r, -14, 14), r.randint(0, 1)))
        elif c < 0.87:
            pairs = []
            for _ in range(r.randint(1, 3) if r.random() < 0.7 else r.randint(6, 30)):
                pairs.append("%d %s" % (r.randint(0, 80), r.choice(WORDS)))
            out.append("update " + " ".join(pairs))
        elif c < 0.89:
            out.append("or " + " ".join("%d %s" % (r.randint(0, 80), r.choice(WORDS)) for _ in range(r.randint(0, 3))))
        elif c < 0.90:
            out.append("ror " + " ".join("%d %s" % (r.randint(0, 80), r.choice(WORDS)) for _ in range(r.randint(0, 3))))
        elif c < 0.92:
            out.append("copy")
        elif c < 0.93:
            out.append("clear")
        elif c < 0.96:
            out.append("len")
        else:
            out.append("repr")
    out += ["shape", "check", "repr"]
    return "\n".join(out) + "\n"


def set_trace(seed, ops):
    r = random.Random(seed)
    out = ["set 4"]
    size = 0

    def vals(k):
        return " ".join(str(r.randint(0, 70)) for _ in range(k))

    for i in range(ops):
        if i % 40 == 39:
            out.append("shape")
            out.append("check")
            continue
        c = r.random()
        v = str(r.randint(0, 70))
        if c < 0.30:
            out.append("add " + v)
            size += 1
        elif c < 0.36:
            out.append("discard " + v)
        elif c < 0.40:
            out.append("remove " + v)
        elif c < 0.45:
            out.append("pop" + ("" if r.random() < 0.4 else " " + str(r.randint(-size - 2, size + 2))))
        elif c < 0.49:
            out.append("get " + str(r.randint(-size - 2, size + 2)))
        elif c < 0.52:
            out.append("slice " + slice_args(r, size))
        elif c < 0.54:
            out.append("del " + str(r.randint(-size - 2, size + 2)))
        elif c < 0.56:
            out.append("delslice " + slice_args(r, size))
        elif c < 0.59:
            out.append(r.choice(["in ", "count ", "index ", "bl ", "br "]) + v)
        elif c < 0.62:
            out.append("irange %s %s %d %d %d" % (opt(r, 0, 70), opt(r, 0, 70), r.randint(0, 1), r.randint(0, 1), r.randint(0, 1)))
        elif c < 0.64:
            out.append("islice %s %s %d" % (opt(r, -size - 2, size + 2), opt(r, -size - 2, size + 2), r.randint(0, 1)))
        elif c < 0.74:
            out.append(r.choice(["union ", "inter ", "diff ", "symdiff ", "subset ", "superset ", "disjoint ", "eq ", "lt ", "le ", "gt ", "ge "]) + vals(r.randint(0, 25)))
        elif c < 0.84:
            # A small update or difference_update walks a Python set in
            # hash order, so these are either one value or big enough
            # that the sorted list is rebuilt.
            op = r.choice(["update", "diff_update", "inter_update", "symdiff_update"])
            k = 1 if r.random() < 0.5 else r.randint(30, 60)
            out.append(op + " " + vals(k))
            size += k if op == "update" else 0
        elif c < 0.86:
            out.append("copy")
        elif c < 0.87:
            out.append("clear")
            size = 0
        elif c < 0.93:
            out.append("len")
        else:
            out.append("repr")
    out += ["shape", "check", "repr"]
    return "\n".join(out) + "\n"


def orders():
    r = random.Random(7)
    lines = ["id,side,type,price,qty"]
    live = []
    for i in range(1, 401):
        c = r.random()
        if c < 0.12 and live:
            oid = r.choice(live)
            lines.append("%d,cancel,%d,," % (i, oid))
            continue
        side = r.choice(["buy", "sell"])
        if c < 0.22:
            lines.append("%d,%s,market,,%d" % (i, side, r.randint(1, 40)))
            continue
        mid = 10000 + int(200 * (i / 400.0))
        price = mid + (r.randint(-60, 20) if side == "buy" else r.randint(-20, 60))
        lines.append("%d,%s,limit,%d,%d" % (i, side, price, r.randint(1, 30)))
        live.append(i)
    return "\n".join(lines) + "\n"


PLAYERS = ["amara", "bjorn", "chen", "dalia", "emeka", "farah", "goran", "hana", "ivo", "jun",
           "kofi", "lena", "mateo", "nadia", "oskar", "priya", "quinn", "rafa", "sana", "tomas"]


def scores():
    r = random.Random(11)
    lines = []
    t = 0
    for _ in range(300):
        t += r.randint(1, 30)
        p = r.choice(PLAYERS)
        pts = r.choice([10, 10, 20, 25, 50, 100, -15, -30])
        lines.append("%d %s %d" % (t, p, pts))
    return "\n".join(lines) + "\n"


ROUTES = ["GET /", "GET /api/items", "POST /api/orders", "GET /static/app.js", "GET /api/search"]


def latency():
    r = random.Random(13)
    lines = []
    t = 1760000000
    for i in range(400):
        t += r.randint(0, 3)
        route = r.choice(ROUTES)
        base = {"GET /": 12, "GET /api/items": 40, "POST /api/orders": 120,
                "GET /static/app.js": 4, "GET /api/search": 90}[route]
        ms = int(r.expovariate(1.0 / base)) + 1
        if 150 <= i < 175:
            ms *= 9
        lines.append("%d %s %d" % (t, route.replace(" ", "_"), ms))
    return "\n".join(lines) + "\n"


def bookings():
    r = random.Random(17)
    lines = []
    rooms = ["atlas", "boreal", "cirrus"]
    for i in range(160):
        c = r.random()
        room = r.choice(rooms)
        if c < 0.12:
            lines.append("cancel %s %d" % (room, r.randrange(480, 1080, 15)))
        elif c < 0.2:
            lines.append("free %s %d" % (room, r.choice([30, 60, 90])))
        else:
            start = r.randrange(480, 1080, 15)
            length = r.choice([15, 30, 30, 45, 60, 90, 120])
            lines.append("book %s %d %d %s" % (room, start, start + length, r.choice(PLAYERS)))
    lines.append("agenda atlas")
    lines.append("agenda boreal")
    lines.append("agenda cirrus")
    return "\n".join(lines) + "\n"


def main():
    write("traces/list.txt", list_trace(1, 1500, "list 4", False))
    write("traces/list_load1000.txt", list_trace(2, 300, "list 1000", False))
    write("traces/keylist_mod10.txt", list_trace(3, 1200, "keylist mod10 4", True))
    write("traces/keylist_neg.txt", list_trace(4, 600, "keylist neg 5", True))
    write("traces/dict.txt", dict_trace(5, 900))
    write("traces/set.txt", set_trace(6, 900))
    write("orders.csv", orders())
    write("scores.txt", scores())
    write("latency.log", latency())
    write("bookings.txt", bookings())
    jobs = [
        "trace\ttraces/list.txt",
        "trace\ttraces/list_load1000.txt",
        "trace\ttraces/keylist_mod10.txt",
        "trace\ttraces/keylist_neg.txt",
        "trace\ttraces/dict.txt",
        "trace\ttraces/set.txt",
        "orderbook\torders.csv",
        "leaderboard\tscores.txt",
        "latency\tlatency.log",
        "booking\tbookings.txt",
    ]
    write("jobs.tsv", "\n".join(jobs) + "\n")


if __name__ == "__main__":
    main()
