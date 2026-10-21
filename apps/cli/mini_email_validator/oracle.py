# Runs data/jobs.jsonl through email-validator itself (the copy in
# email_validator/, unchanged) and prints what mini_email_validator
# prints. It uses idna 3.20 from ../mini_idna/idna and dnspython 2.7.0
# from ../mini_dnspython/dns, both unchanged, and answers DNS queries
# from data/dns.tsv instead of the network.
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(HERE, "..", "mini_idna"))
sys.path.insert(2, os.path.join(HERE, "..", "mini_dnspython"))
sys.dont_write_bytecode = True

import dns.exception  # noqa: E402
import dns.name  # noqa: E402
import dns.rdata  # noqa: E402
import dns.rdataclass  # noqa: E402
import dns.rdatatype  # noqa: E402
import dns.resolver  # noqa: E402

import email_validator  # noqa: E402
import email_validator.__main__ as ev_main  # noqa: E402
from email_validator import EmailNotValidError, EmailSyntaxError, EmailUndeliverableError, validate_email  # noqa: E402

DATA = os.path.join(HERE, "data")

FAILURES = {
    "NXDOMAIN": dns.resolver.NXDOMAIN,
    "TIMEOUT": dns.exception.Timeout,
    "NONAMESERVERS": dns.resolver.NoNameservers,
    "YXDOMAIN": dns.resolver.YXDOMAIN,
}


class Resolver:
    """Answers resolve(name, type) from data/dns.tsv, the way a cache
    filled from real answers would: a name with no records does not
    exist, a name without records of the type has no answer."""

    def __init__(self, path):
        self.records = {}
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line or line.startswith("#"):
                    continue
                name, rdtype, value = line.split("\t")
                self.records.setdefault(dns.name.from_text(name), []).append((rdtype, value))

    def resolve(self, qname, rdtype):
        name = dns.name.from_text(qname)
        rows = self.records.get(name)
        if rows is None:
            raise dns.resolver.NXDOMAIN()
        for t, _ in rows:
            if t in FAILURES:
                raise FAILURES[t]()
        answer = [dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.from_text(t), v)
                  for t, v in rows if t == rdtype]
        if not answer:
            raise dns.resolver.NoAnswer()
        return answer


RESOLVER = Resolver(os.path.join(DATA, "dns.tsv"))


def opts_text(opts):
    if not opts:
        return "(defaults)"
    return ", ".join(f"{k}={v}" for k, v in opts.items())


def run_validate(email, opts):
    kw = dict(opts)
    if kw.get("check_deliverability", True):
        kw["dns_resolver"] = RESOLVER
    return validate_email(email, **kw)


def compact(v):
    out = f"ok normalized={v.normalized!r} ascii_email={v.ascii_email!r} smtputf8={v.smtputf8}"
    if v.display_name is not None:
        out += f" display_name={v.display_name!r}"
    if hasattr(v, "domain_address"):
        out += f" address={v.domain_address!r}"
    if hasattr(v, "mx"):
        out += f" mx={v.mx!r}"
    if hasattr(v, "mx_fallback_type"):
        out += f" fallback={v.mx_fallback_type!r}"
    return out


def failure(e):
    return f"! {type(e).__name__}: {e}"


def op_validate(op, last):
    opts = op["opts"]
    if last[0] != opts:
        print("-- opts: " + opts_text(opts))
        last[0] = opts
    if "bytes" in op:
        email = bytes.fromhex(op["bytes"])
    else:
        email = op["email"]
    print(repr(email))
    try:
        print("  => " + compact(run_validate(email, opts)))
    except Exception as e:
        print("  " + failure(e))


def op_show(op):
    print(f"show {op['email']!r} with {opts_text(op['opts'])}")
    try:
        print(run_validate(op["email"], op["opts"]).as_constructor())
    except Exception as e:
        print(failure(e))


ENV_NAMES = ("ALLOW_SMTPUTF8", "ALLOW_QUOTED_LOCAL", "ALLOW_DOMAIN_LITERAL", "ALLOW_DISPLAY_NAME",
             "GLOBALLY_DELIVERABLE", "CHECK_DELIVERABILITY", "TEST_ENVIRONMENT", "DEFAULT_TIMEOUT")


def op_cli(op):
    print(f"$ args {op['args']!r} env {op['env']!r} stdin {op['stdin']!r}")
    saved = (sys.argv, sys.stdin, sys.stdout, {k: os.environ.get(k) for k in ENV_NAMES})
    for k in ENV_NAMES:
        os.environ.pop(k, None)
    os.environ.update(op["env"])
    sys.argv = ["email_validator"] + op["args"]
    sys.stdin = io.StringIO("".join(line + "\n" for line in op["stdin"]))
    out = io.StringIO()
    sys.stdout = out
    err = None
    try:
        ev_main.main(dns_resolver=RESOLVER)
    except Exception as e:
        err = e
    finally:
        sys.argv, sys.stdin, sys.stdout = saved[0], saved[1], saved[2]
        for k, v in saved[3].items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    for line in out.getvalue().split("\n")[:-1]:
        print("| " + line)
    if err is not None:
        print(failure(err))


FORMS = {
    "web": {},
    "mime": {"allow_display_name": True},
    "legacy": {"allow_quoted_local": True, "allow_domain_literal": True, "globally_deliverable": False,
               "check_deliverability": False},
}


def op_signups():
    accounts = []
    by_key = {}
    unknown = 0
    with open(os.path.join(DATA, "signups.tsv"), encoding="utf-8") as f:
        rows = [line.rstrip("\n").split("\t") for line in f if not line.startswith("#")]
    for when, form, name, addr in rows:
        head = f"{when} {form:<6} {addr!r}"
        try:
            v = run_validate(addr, FORMS[form])
        except EmailUndeliverableError as e:
            print(f"{head}: undeliverable: {e}")
            continue
        except EmailSyntaxError as e:
            print(f"{head}: invalid: {e}")
            continue
        key = v.normalized
        if key in by_key:
            n = by_key[key]
            print(f"{head}: duplicate of #{n} ({accounts[n - 1]['name']})")
            continue
        n = len(accounts) + 1
        by_key[key] = n
        who = name or v.display_name or v.local_part
        accounts.append({"name": who, "v": v})
        line = f"{head}: #{n} {key!r} name={who!r}"
        if getattr(v, "mx", None):
            line += f" via {v.mx[0][1]}"
            if v.mx_fallback_type:
                line += f" ({v.mx_fallback_type} fallback)"
        elif hasattr(v, "mx_fallback_type"):
            line += " deliverability unknown"
            unknown += 1
        else:
            line += " not checked"
        if v.smtputf8:
            line += " needs SMTPUTF8"
        elif v.ascii_email != v.normalized:
            line += f" ascii={v.ascii_email!r}"
        print(line)
    print(f"accounts: {len(accounts)}, needing SMTPUTF8: {sum(1 for a in accounts if a['v'].smtputf8)}, "
          f"deliverability unknown: {unknown}")
    domains = {}
    for a in accounts:
        domains.setdefault(a["v"].domain, []).append(a["v"].local_part)
    for d in sorted(domains):
        print(f"  {d}: {', '.join(sorted(domains[d]))}")


def main():
    with open(os.path.join(DATA, "jobs.jsonl"), encoding="utf-8") as f:
        jobs = [json.loads(line) for line in f]
    for j in jobs:
        print("== " + j["name"])
        last = [None]
        for op in j["ops"]:
            kind = op["op"]
            if kind == "validate":
                op_validate(op, last)
            else:
                last[0] = None
                if kind == "show":
                    op_show(op)
                elif kind == "cli":
                    op_cli(op)
                elif kind == "signups":
                    op_signups()


if __name__ == "__main__":
    main()
