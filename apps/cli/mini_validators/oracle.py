# Runs data/jobs.tsv through validators itself; the output is
# expected.out.
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import validators  # noqa: E402
from validators.uri import uri as _uri  # noqa: E402

# uri is not exported from the package; the jobs call it all the same.
validators.uri = _uri



def call_text(name, args, kw):
    parts = [repr(a) for a in args] + ["%s=%r" % (k, v) for k, v in kw.items()]
    return "%s(%s)" % (name, ", ".join(parts))


def run_call(name, args, kw):
    try:
        r = getattr(validators, name)(*args, **kw)
    except Exception as e:  # noqa: BLE001
        return "raised %s: %s" % (type(e).__name__, e)
    return "True" if r is True else repr(r)


def ok(r):
    return r is True


def signups(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            rows.append(line.rstrip("\n").split("\t"))
    fields = ["username", "email", "website", "country", "card", "iban", "ip"]
    rejected = {k: 0 for k in fields}
    brands = {}
    accepted = 0
    for r in rows:
        uid, user, mail, site, cc, cardno, acct, ip = r
        bad = []
        if not ok(validators.slug(user)):
            bad.append("username")
        if not ok(validators.email(mail)):
            bad.append("email")
        if site and not ok(validators.url(site)):
            bad.append("website")
        if not ok(validators.country_code(cc, iso_format="alpha2")):
            bad.append("country")
        brand = "none"
        if ok(validators.card_number(cardno)):
            for b in ["visa", "mastercard", "amex", "discover", "jcb", "diners", "unionpay", "mir"]:
                if ok(getattr(validators, b)(cardno)):
                    brand = b
                    break
            if brand == "none":
                bad.append("card")
        else:
            bad.append("card")
        if acct and not ok(validators.iban(acct)):
            bad.append("iban")
        if not (ok(validators.ipv4(ip, cidr=False)) or ok(validators.ipv6(ip, cidr=False))):
            bad.append("ip")
        public = ok(validators.ipv4(ip, cidr=False, private=False))
        for b in bad:
            rejected[b] += 1
        if bad:
            print("   %s %s: rejected %s" % (uid, user, ", ".join(bad)))
        else:
            accepted += 1
            brands[brand] = brands.get(brand, 0) + 1
            where = "public ipv4" if public else "not a public ipv4"
            print("   %s %s: ok, %s card, %s" % (uid, user, brand, where))
    print("   %d of %d accepted" % (accepted, len(rows)))
    for k in fields:
        print("     %s rejected %d times" % (k, rejected[k]))
    for b in sorted(brands):
        print("     %s cards accepted: %d" % (b, brands[b]))


def webhooks(path):
    with open(path, encoding="utf-8") as f:
        rows = [line.rstrip("\n").split("\t") for line in f if not line.startswith("#")]
    counts = {}
    for tenant, hook in rows:
        plain = validators.url(hook)
        guarded = validators.url(hook, private=False)
        if ok(guarded):
            verdict = "accepted"
        elif ok(plain):
            verdict = "rejected: private, loopback or multicast address"
        else:
            reason = getattr(plain, "reason", "")
            verdict = "rejected: not a valid URL" + (" (%s)" % reason if reason else "")
        counts[verdict.split(" (")[0]] = counts.get(verdict.split(" (")[0], 0) + 1
        print("   %s %s: %s" % (tenant, hook, verdict))
    for k in sorted(counts):
        print("     %s: %d" % (k, counts[k]))


def main():
    with open("data/jobs.tsv", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    for line in lines:
        if line.startswith("== "):
            print(line)
            continue
        fields = line.split("\t")
        if fields[0] == "call":
            name, args, kw = fields[1], json.loads(fields[2]), json.loads(fields[3])
            print("-- " + call_text(name, args, kw))
            print("   " + run_call(name, args, kw))
        elif fields[0] == "signups":
            signups("data/" + fields[1])
        elif fields[0] == "webhooks":
            webhooks("data/" + fields[1])


main()
