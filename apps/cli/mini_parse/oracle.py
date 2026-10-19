# Runs data/jobs.jsonl through parse 1.22.3 (the package in parse/,
# unchanged) and prints what mini_parse prints. Run mk.py first.
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import parse  # noqa: E402


# ------------------------------------------------------------ the extra types the jobs can name
@parse.with_pattern(r"\d+")
def Number(text):
    return int(text)


@parse.with_pattern(r"(yes|no|on|off|true|false)", regex_group_count=1)
def Bool(text):
    return text.lower() in ("yes", "on", "true")


def Word(text):
    return text.upper()


@parse.with_pattern(r"red|green|blue")
def Color(text):
    return text


@parse.with_pattern(r"(\d+)x(\d+)", regex_group_count=2)
def Size(text):
    w, h = text.lower().split("x")
    return (int(w), int(h))


# the group count is missing, as it often is
@parse.with_pattern(r"(\d+)-(\d+)")
def Range(text):
    a, b = text.split("-")
    return list(range(int(a), int(b) + 1))


@parse.with_pattern(r"[^,]+(?:,[^,]+)*")
def Csv(text):
    return [t.strip() for t in text.split(",")]


@parse.with_pattern(r"\$\d+\.\d\d")
def Money(text):
    d, c = text[1:].split(".")
    return int(d) * 100 + int(c)


CONVERTERS = {"Number": Number, "Bool": Bool, "Word": Word, "Color": Color, "Size": Size, "Range": Range,
              "Csv": Csv, "Money": Money}


def extra_of(spec):
    if not spec:
        return None
    out = {}
    for item in spec.split(","):
        if "=" in item:
            name, conv = item.split("=")
        else:
            name = conv = item
        out[name] = CONVERTERS[conv]
    return out


def exc(e):
    return "%s: %s" % (type(e).__name__, e)


def show(r):
    if r is None:
        print("  None")
        return
    print("  " + repr(r))
    print("  spans " + repr(r.spans))


def header(n, j):
    h = "== %d %s %r" % (n, j["op"], j["fmt"])
    if "s" in j:
        h += " %r" % j["s"]
    if j.get("cs"):
        h += " cs"
    if "pos" in j:
        h += " pos=%d" % j["pos"]
    if "endpos" in j:
        h += " endpos=%d" % j["endpos"]
    if j.get("extra"):
        h += " extra=" + j["extra"]
    print(h)


def run_unit(j):
    op = j["op"]
    extra = extra_of(j.get("extra"))
    cs = j.get("cs", False)
    try:
        if op == "parse":
            show(parse.parse(j["fmt"], j["s"], extra_types=extra, case_sensitive=cs))
        elif op == "search":
            show(parse.search(j["fmt"], j["s"], pos=j.get("pos", 0), endpos=j.get("endpos"), extra_types=extra,
                              case_sensitive=cs))
        elif op == "findall":
            n = 0
            for r in parse.findall(j["fmt"], j["s"], pos=j.get("pos", 0), endpos=j.get("endpos"),
                                   extra_types=extra, case_sensitive=cs):
                show(r)
                n += 1
            print("  %d found" % n)
        elif op == "expr":
            p = parse.compile(j["fmt"], extra_types=extra)
            print("  " + repr(p))
            print("  " + p._expression)
            print("  named %r fixed %r" % (p.named_fields, p.fixed_fields))
    except Exception as e:
        print("  " + exc(e))


def read(name):
    with open(os.path.join("data", name), encoding="utf-8") as f:
        return f.read()


# ------------------------------------------------------------ a BDD runner
def money(c):
    return "$%d.%02d" % (c // 100, c % 100)


class StepFailed(Exception):
    pass


class World:
    def __init__(self):
        self.prices = {}
        self.cart = {}
        self.discount = 0
        self.message = ""
        self.stock = {}
        self.last = None


def step_impl(name, w, a):
    if name in ("store_sells", "store_sells_quoted"):
        w.prices[a["item"]] = a["price"]
    elif name == "empty_cart":
        w.cart = {}
        w.discount = 0
    elif name in ("add_one", "add_many"):
        item = a["item"]
        qty = a.get("qty", 1)
        if item not in w.prices:
            w.message = "we do not sell %s" % item
        else:
            w.cart[item] = w.cart.get(item, 0) + qty
    elif name == "remove":
        if a["item"] not in w.cart:
            raise StepFailed("%s is not in the cart" % a["item"])
        del w.cart[a["item"]]
    elif name == "apply_code":
        codes = {"SAVE10": 10, "HALF": 50}
        if a["code"] not in codes:
            raise StepFailed("unknown code %s" % a["code"])
        w.discount = codes[a["code"]]
    elif name == "cart_count":
        n = sum(w.cart.values())
        if n != a["n"]:
            raise StepFailed("expected %d items, the cart has %d" % (a["n"], n))
    elif name == "total":
        t = sum(q * w.prices[i] for i, q in w.cart.items())
        t -= t * w.discount // 100
        if t != a["amount"]:
            raise StepFailed("expected %s, the total is %s" % (money(a["amount"]), money(t)))
    elif name == "contains":
        if a["item"] not in w.cart:
            raise StepFailed("%s is not in the cart" % a["item"])
    elif name == "not_contains":
        if a["item"] in w.cart:
            raise StepFailed("%s is in the cart" % a["item"])
    elif name == "told":
        if w.message != a["message"]:
            raise StepFailed("the last message was %r" % w.message)
    elif name in ("holds", "arrive", "leave", "holds_check", "out_of_stock"):
        item = a["item"].lower()
        have = w.stock.get(item, 0)
        if name == "holds":
            w.stock[item] = a["qty"]
        elif name == "arrive":
            w.stock[item] = have + a["qty"]
            w.last = a["day"]
        elif name == "leave":
            if a["qty"] > have:
                raise StepFailed("only %d %s left" % (have, item))
            w.stock[item] = have - a["qty"]
            w.last = a["day"]
        elif name == "holds_check":
            if have != a["qty"]:
                raise StepFailed("the warehouse holds %d %s" % (have, item))
        else:
            if have != 0:
                raise StepFailed("%d %s left" % (have, item))
    elif name == "last_move":
        if w.last != a["day"]:
            raise StepFailed("the last movement was on %s" % (w.last.isoformat() if w.last else "never"))


KEYWORDS = {"given": "given", "when": "when", "then": "then", "and": None, "but": None}


def load_steps():
    steps = []
    for line in read("steps.txt").splitlines():
        kind, name, pat = line.split("\t")
        steps.append((kind, name, parse.compile(pat, extra_types={"Money": Money})))
    return steps


def parse_feature(text):
    feature = None
    background = []
    scenarios = []
    cur = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("Feature:"):
            feature = line[len("Feature:"):].strip()
        elif line.startswith("Background:"):
            cur = {"steps": background}
        elif line.startswith("Scenario Outline:"):
            cur = {"title": line[len("Scenario Outline:"):].strip(), "steps": [], "outline": True, "rows": []}
            scenarios.append(cur)
        elif line.startswith("Scenario:"):
            cur = {"title": line[len("Scenario:"):].strip(), "steps": [], "outline": False}
            scenarios.append(cur)
        elif line.startswith("Examples:"):
            pass
        elif line.startswith("|") and cur is not None and cur.get("outline"):
            cur["rows"].append([c.strip() for c in line.strip("|").split("|")])
        elif cur is not None:
            word = line.split(" ", 1)[0]
            if word.lower() in KEYWORDS:
                cur["steps"].append((word, line[len(word):].strip()))
    return feature, background, scenarios


def expand(scenario):
    if not scenario["outline"]:
        return [(scenario["title"], scenario["steps"])]
    head = scenario["rows"][0]
    out = []
    for row in scenario["rows"][1:]:
        steps = []
        for kw, text in scenario["steps"]:
            for h, v in zip(head, row):
                text = text.replace("<%s>" % h, v)
            steps.append((kw, text))
        label = ", ".join("%s=%s" % (h, v) for h, v in zip(head, row))
        out.append(("%s [%s]" % (scenario["title"], label), steps))
    return out


def find_step(steps, kind, text):
    for k, name, p in steps:
        if k != kind:
            continue
        r = p.parse(text)
        if r is not None:
            return name, r
    return None, None


def run_bdd(j):
    steps = load_steps()
    dry = j.get("dry", False)
    totals = {"passed": 0, "failed": 0, "undefined": 0, "skipped": 0}
    sc_totals = {"passed": 0, "failed": 0, "undefined": 0}
    for path in j["files"]:
        feature, background, scenarios = parse_feature(read(path))
        print("Feature: %s" % feature)
        for sc in scenarios:
            for title, sc_steps in expand(sc):
                print("  Scenario: %s" % title)
                w = World()
                status = "passed"
                kind = "given"
                for kw, text in background + sc_steps:
                    k = KEYWORDS[kw.lower()]
                    if k is not None:
                        kind = k
                    line = "    %s %s" % (kw, text)
                    if status != "passed":
                        print(line + " ... skipped")
                        totals["skipped"] += 1
                        continue
                    try:
                        name, r = find_step(steps, kind, text)
                    except Exception as e:
                        print(line + " ... failed: " + exc(e))
                        totals["failed"] += 1
                        status = "failed"
                        continue
                    if name is None:
                        print(line + " ... undefined")
                        totals["undefined"] += 1
                        status = "undefined"
                        continue
                    if dry:
                        print(line + " -> %s %r" % (name, r.named))
                        totals["passed"] += 1
                        continue
                    try:
                        step_impl(name, w, r.named)
                        print(line + " ... passed")
                        totals["passed"] += 1
                    except StepFailed as e:
                        print(line + " ... failed: %s" % e)
                        totals["failed"] += 1
                        status = "failed"
                sc_totals[status] += 1
    print("%d scenarios (%d passed, %d failed, %d undefined)" % (
        sum(sc_totals.values()), sc_totals["passed"], sc_totals["failed"], sc_totals["undefined"]))
    print("%d steps (%d passed, %d failed, %d undefined, %d skipped)" % (
        sum(totals.values()), totals["passed"], totals["failed"], totals["undefined"], totals["skipped"]))


# ------------------------------------------------------------ an access-log report
def ranked(counts):
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def run_logs(j):
    p = parse.compile(j["fmt"])
    status = {}
    methods = {}
    paths = {}
    days = {}
    ips = set()
    total = 0
    good = 0
    first = last = None
    for n, line in enumerate(read(j["file"]).split("\n")[:-1], 1):
        try:
            r = p.search(line) if j.get("search") else p.parse(line)
        except Exception as e:
            print("line %d: %s" % (n, exc(e)))
            continue
        if r is None:
            print("line %d: no match" % n)
            continue
        good += 1
        status[r["status"]] = status.get(r["status"], 0) + 1
        if "method" in r:
            methods[r["method"]] = methods.get(r["method"], 0) + 1
            paths[r["path"]] = paths.get(r["path"], 0) + 1
        ips.add(r["ip"])
        if r["size"] != "-":
            total += int(r["size"])
        when = r["when"]
        d = when.date().isoformat()
        days[d] = days.get(d, 0) + 1
        if first is None or when < first:
            first = when
        if last is None or when > last:
            last = when
    print("%d requests from %d addresses, %d bytes" % (good, len(ips), total))
    print("status " + " ".join("%d=%d" % kv for kv in sorted(status.items())))
    if methods:
        print("methods " + " ".join("%s=%d" % kv for kv in ranked(methods)))
        print("top paths " + " ".join("%s=%d" % kv for kv in ranked(paths)[:5]))
    print("days " + " ".join("%s=%d" % kv for kv in sorted(days.items())))
    print("first %r" % first)
    print("last %r" % last)


def run_applog(j):
    p = parse.compile(j["fmt"])
    served = parse.compile("request served in {ms:d} ms")
    levels = {}
    loggers = {}
    ms = []
    for n, line in enumerate(read(j["file"]).split("\n")[:-1], 1):
        try:
            r = p.parse(line)
        except Exception as e:
            print("line %d: %s" % (n, exc(e)))
            continue
        if r is None:
            print("line %d: no match" % n)
            continue
        levels[r["level"]] = levels.get(r["level"], 0) + 1
        loggers[r["logger"]] = loggers.get(r["logger"], 0) + 1
        if r["level"] in ("ERROR", "WARNING"):
            print("%s %s %s: %s" % (r["when"].isoformat(), r["level"], r["logger"], r["message"]))
        s = served.search(r["message"])
        if s is not None:
            ms.append(s["ms"])
    print("levels " + " ".join("%s=%d" % kv for kv in sorted(levels.items())))
    print("loggers " + " ".join("%s=%d" % kv for kv in ranked(loggers)))
    if ms:
        print("served %d requests, %d ms in all, slowest %d ms" % (len(ms), sum(ms), max(ms)))


def run_scan(j):
    n = 0
    for r in parse.findall(j["fmt"], read(j["file"])):
        show(r)
        n += 1
    print("  %d found" % n)


def main():
    with open("data/jobs.jsonl", encoding="utf-8") as f:
        jobs = [json.loads(line) for line in f]
    for n, j in enumerate(jobs, 1):
        header(n, j)
        op = j["op"]
        if op == "bdd":
            run_bdd(j)
        elif op == "logs":
            run_logs(j)
        elif op == "applog":
            run_applog(j)
        elif op == "scan":
            run_scan(j)
        else:
            run_unit(j)


main()
