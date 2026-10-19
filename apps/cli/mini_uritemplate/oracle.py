# Runs data/jobs.tsv through uritemplate itself; the output is
# expected.out.
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uritemplate import URITemplate, expand, partial, variables  # noqa: E402


def unpair(v):
    if isinstance(v, dict):
        if list(v) == ["__pairs__"]:
            return [(k, unpair(x)) for k, x in v["__pairs__"]]
        return {k: unpair(x) for k, x in v.items()}
    if isinstance(v, list):
        return [unpair(x) for x in v]
    return v


def err(e):
    return "error: %s: %s" % (type(e).__name__, e)


def describe(t):
    tpl = URITemplate(t)
    if not tpl.variables:
        print("   no variables")
    for v in tpl.variables:
        safe = "reserved" if v.safe else "unreserved"
        print("   %r: operator %r, start %r, join %r, %s" % (v.original, v.operator, v.start, v.join_str, safe))
        for name, opts in v.variables:
            print("     %r explode=%s prefix=%s" % (name, opts["explode"], opts["prefix"]))
        if v.defaults:
            print("     defaults %r" % (v.defaults,))


def host_of(url):
    rest = url.split("://", 1)[1] if "://" in url else url
    for k, c in enumerate(rest):
        if c in "/?#":
            return rest[:k]
    return rest


def api_report(api_path, req_path):
    with open(api_path, encoding="utf-8") as f:
        api = json.load(f)
    links = api["links"]
    print("   service %s, %d links" % (api["service"], len(links)))
    by_link = {}
    by_host = {}
    seen = set()
    longest = ""
    differ = 0
    with open(req_path, encoding="utf-8") as f:
        rows = [line.rstrip("\n").split("\t") for line in f if not line.startswith("#")]
    for client, link, ctx_s, call_s in rows:
        ctx = unpair(json.loads(ctx_s))
        call = unpair(json.loads(call_s))
        t = links[link]
        merged = dict(ctx)
        merged.update(call)
        url = expand(t, merged)
        print("   %s %s: %s" % (client, link, url))
        bound = partial(t, ctx)
        via = bound.expand(call)
        if via != url:
            differ += 1
            print("     bound first: %r" % (bound,))
            print("     then expanded: %s" % via)
        by_link[link] = by_link.get(link, 0) + 1
        h = host_of(url)
        by_host[h] = by_host.get(h, 0) + 1
        seen.add(url)
        if len(url) > len(longest):
            longest = url
    print("   calls per link:")
    for k in sorted(by_link):
        print("     %s %d (%s)" % (k, by_link[k], ", ".join(variables(links[k]))))
    print("   calls per host:")
    for k in sorted(by_host):
        print("     %s %d" % (k, by_host[k]))
    print("   %d calls, %d distinct URLs, %d where binding first changed the URL" % (len(rows), len(seen), differ))
    print("   longest (%d chars): %s" % (len(longest), longest))


def main():
    cur = {}
    tally = {"cases": 0, "match": 0, "one of": 0, "failure expected": 0, "mismatch": 0}
    with open("data/jobs.tsv", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    for line in lines:
        if line.startswith("== "):
            print(line)
            continue
        fields = line.split("\t")
        op, args = fields[0], fields[1:]
        if op == "vars":
            cur = unpair(json.loads(args[0]))
            print("-- vars %s" % ", ".join(sorted(cur)))
            continue
        print("-- %s %r" % (op, args[0]))
        if op == "case":
            want = json.loads(args[1])
            tally["cases"] += 1
            try:
                got = expand(args[0], cur)
            except Exception as e:
                verdict = "failure expected" if want is False else "mismatch"
                tally[verdict] += 1
                print("   %s [%s]" % (err(e), verdict))
                continue
            if want is False:
                verdict = "failure expected"
            elif isinstance(want, list):
                verdict = "one of" if got in want else "mismatch"
            else:
                verdict = "match" if got == want else "mismatch"
            tally[verdict] += 1
            note = verdict
            if verdict == "one of":
                note = "one of %d" % len(want)
            elif verdict == "failure expected":
                note = "expanded, failure expected"
            print("   %r [%s]" % (got, note))
        elif op == "expand":
            try:
                print("   %r" % expand(args[0], cur))
            except Exception as e:
                print("   " + err(e))
        elif op == "partial":
            try:
                print("   %r" % (partial(args[0], cur),))
            except Exception as e:
                print("   " + err(e))
        elif op == "variables":
            try:
                print("   %r" % (variables(args[0]),))
            except Exception as e:
                print("   " + err(e))
        elif op == "parse":
            try:
                describe(args[0])
            except Exception as e:
                print("   " + err(e))
        elif op == "api":
            api_report("data/" + args[0], "data/" + args[1])
    print("== suite: %d cases, %d match, %d one of several, %d failure expected, %d mismatch"
          % (tally["cases"], tally["match"], tally["one of"], tally["failure expected"], tally["mismatch"]))


main()
