# Runs data/jobs.tsv through tldextract itself; the output is
# expected.out. No network: every extractor reads the snapshot of the
# Public Suffix List that tldextract ships, as one with no cache and no
# suffix list URLs does.
import contextlib
import io
import json
import os
import sys
import types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests.adapters  # noqa: E402

# tldextract imports these for its disk cache and file:// URLs, neither of
# which an extractor without a cache directory or URLs uses: it only mounts
# the adapter on a session it then closes.
sys.modules["filelock"] = types.SimpleNamespace(FileLock=None)
sys.modules["requests_file"] = types.SimpleNamespace(FileAdapter=requests.adapters.HTTPAdapter)

import tldextract  # noqa: E402
import tldextract.cli  # noqa: E402
from tldextract.suffix_list import extract_tlds_from_suffix_list  # noqa: E402


def make(**kw):
    return tldextract.TLDExtract(cache_dir=None, suffix_list_urls=(), **kw)


tldextract.cli.TLDExtract = lambda **kw: make(**{k: v for k, v in kw.items() if k != "fallback_to_snapshot"})


def show(ext):
    print("   %r" % (ext,))
    print("   registered_domain=%r fqdn=%r ipv4=%r ipv6=%r" % (ext.registered_domain, ext.fqdn, ext.ipv4, ext.ipv6))


def site_of(ext):
    return ext.registered_domain or ext.ipv4 or ext.ipv6 or ext.domain


def referrers(ex, path):
    counts = {}
    subs = {}
    suffixes = {}
    total = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            ref = line.split('"')[3]
            total += 1
            if ref == "-":
                site = "(direct)"
            else:
                ext = ex(ref, include_psl_private_domains=True)
                site = site_of(ext) or "(no host)"
                subs.setdefault(site, set()).add(ext.subdomain or "@")
                suffixes[ext.suffix or "(none)"] = suffixes.get(ext.suffix or "(none)", 0) + 1
            counts[site] = counts.get(site, 0) + 1
    print("   %d requests from %d sites" % (total, len(counts)))
    for site, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        extra = " (%s)" % ", ".join(sorted(subs[site])) if site in subs else ""
        print("     %3d %s%s" % (n, site, extra))
    print("   by public suffix:")
    for suf, n in sorted(suffixes.items(), key=lambda kv: (-kv[1], kv[0])):
        print("     %3d %s" % (n, suf))


def cookies(ex, path):
    tally = {}
    with open(path, encoding="utf-8") as f:
        rows = [line.rstrip("\n").split("\t") for line in f if not line.startswith("#")]
    for host, attr in rows:
        h = host.lower()
        d = attr.lstrip(".").lower()
        eh = ex(h, include_psl_private_domains=True)
        ed = ex(d, include_psl_private_domains=True)
        if eh.ipv4 or eh.ipv6:
            verdict = "accepted, host only" if d == h else "rejected: the host is an IP address"
        elif ed.suffix and not ed.domain:
            verdict = "accepted, host only (Domain is a public suffix)" if d == h else "rejected: Domain is a public suffix"
        elif h != d and not h.endswith("." + d):
            verdict = "rejected: Domain does not match the host"
        elif h == d:
            verdict = "accepted for %s" % d
        else:
            verdict = "accepted for %s and its subdomains" % d
        key = verdict.split(":")[0].split(" for ")[0].split(",")[0]
        tally[key] = tally.get(key, 0) + 1
        print("   %s Domain=%s: %s" % (host, attr, verdict))
    for k in sorted(tally):
        print("     %s: %d" % (k, tally[k]))


def samesite(ex, path):
    with open(path, encoding="utf-8") as f:
        rows = [line.rstrip("\n").split("\t") for line in f if not line.startswith("#")]
    for a, b in rows:
        sa = site_of(ex(a, include_psl_private_domains=True))
        sb = site_of(ex(b, include_psl_private_domains=True))
        if sa and sa == sb:
            print("   %s and %s: same site, %s" % (a, b, sa))
        else:
            print("   %s and %s: different sites, %s and %s" % (a, b, sa or "(none)", sb or "(none)"))


def cli(args):
    out = io.StringIO()
    code = 0
    sys.argv = ["tldextract"] + args
    with contextlib.redirect_stdout(out):
        try:
            tldextract.cli.main()
        except SystemExit as e:
            code = e.code
    for line in out.getvalue().splitlines():
        print("   " + line)
    print("   exit %d" % code)


def main():
    ex = make()
    with open("data/jobs.tsv", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    for line in lines:
        if line.startswith("== "):
            print(line)
            continue
        fields = line.split("\t")
        op = fields[0]
        if op == "extract":
            url, flag = fields[1], fields[2]
            if flag:
                private = flag == "private"
                print("-- extract(%r, include_psl_private_domains=%r)" % (url, private))
                show(ex(url, include_psl_private_domains=private))
            else:
                print("-- extract(%r)" % (url,))
                show(ex(url))
        elif op == "extractor":
            kw = json.loads(fields[1])
            print("-- TLDExtract(%s)" % ", ".join("%s=%r" % kv for kv in kw.items()))
            ex = make(**kw)
        elif op == "cli":
            args = json.loads(fields[1])
            print("-- tldextract %s" % " ".join(args))
            cli(args)
        elif op == "tlds":
            with open("data/public_suffix_list.dat", encoding="utf-8") as f:
                public, private = extract_tlds_from_suffix_list(f.read())
            print("   %d public rules, %d private rules" % (len(public), len(private)))
            print("   %d wildcard rules, %d exceptions" % (sum(r.startswith("*") for r in public + private),
                                                         sum(r.startswith("!") for r in public + private)))
            print("   %d suffixes without private domains, %d with" % (len(ex.tlds), len(ex._get_tld_extractor().tlds(True))))
        elif op == "referrers":
            referrers(ex, "data/" + fields[1])
        elif op == "cookies":
            cookies(ex, "data/" + fields[1])
        elif op == "samesite":
            samesite(ex, "data/" + fields[1])


main()
