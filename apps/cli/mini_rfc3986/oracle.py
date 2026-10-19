# Reference: runs data/jobs.jsonl through the vendored rfc3986 (and the
# vendored idna it uses for IRIs), then prints a webhook report. Prints
# every step as "<job>.<step> <op>: <result>"; a step that raises prints
# "raised <Type>: <first argument>".
import json, os, sys, warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.simplefilter("ignore")

import rfc3986
from rfc3986 import normalizers, validators, parseresult, exceptions
from rfc3986.builder import URIBuilder
from rfc3986.validators import Validator
from rfc3986.parseresult import ParseResult, ParseResultBytes


class Valid:
    pass


VALID = Valid()


def show(v):
    if v is VALID:
        return "valid"
    if isinstance(v, Validator):
        return "Validator()"
    if isinstance(v, bool):
        return str(v)
    return repr(v)


def make(step):
    op = step[0]
    if op == "uri":
        return rfc3986.uri_reference(step[1])
    if op == "uri_b":
        return rfc3986.uri_reference(bytes.fromhex(step[1]))
    if op == "iri":
        return rfc3986.iri_reference(step[1])
    if op == "urlparse":
        return rfc3986.urlparse(step[1])
    if op == "urlparse_b":
        return rfc3986.urlparse(bytes.fromhex(step[1]))
    if op == "parse":
        return ParseResult.from_string(step[1], strict=step[2], lazy_normalize=step[3])
    if op == "parse_bytes":
        return ParseResultBytes.from_string(step[1], strict=step[2], lazy_normalize=step[3])
    if op == "parts":
        return ParseResult.from_parts(**step[1])
    if op == "parts_bytes":
        return ParseResultBytes.from_parts(**{("lazy_normalize" if k == "lazy" else k): v for k, v in step[1].items()})
    if op == "builder":
        return URIBuilder()
    if op == "builder_from":
        return URIBuilder.from_uri(step[1])
    if op == "validator":
        return Validator()
    return None


def call_fn(name, args):
    if name == "normalize_authority":
        return getattr(normalizers, name)(tuple(args[0]))
    if name == "encode_component":
        return normalizers.encode_component(args[0], "utf-8")
    if name in ("valid_ipv4_host_address",):
        return validators.valid_ipv4_host_address(args[0])
    if name == "host_is_valid":
        return bool(validators.host_is_valid(args[0]))
    if name == "split_authority":
        return parseresult.split_authority(args[0])
    if name == "is_valid_uri":
        kw = args[1] if len(args) > 1 else {}
        return rfc3986.is_valid_uri(args[0], **kw)
    if name == "normalize_uri":
        return rfc3986.normalize_uri(args[0])
    return getattr(normalizers, name)(args[0])


def apply(cur, step):
    op = step[0]
    a = step[1:]
    if op == "fn":
        return False, call_fn(a[0], a[1:])
    if op == "unsplit":
        return False, cur.unsplit()
    if op == "unsplit_idna":
        return False, cur.unsplit(use_idna=True)
    if op == "geturl":
        return False, cur.geturl()
    if op == "attr":
        return False, getattr(cur, a[0])
    if op == "authority_info":
        return False, cur.authority_info()
    if op == "is_absolute":
        return False, cur.is_absolute()
    if op == "is_valid":
        return False, cur.is_valid(**(a[0] if a else {}))
    if op == "eq":
        return False, cur == a[0]
    if op == "eq_tuple":
        return False, cur == tuple(a[0])
    if op == "resolve":
        return True, cur.resolve_with(a[0], strict=a[1])
    if op == "copy_with":
        return True, cur.copy_with(**a[0])
    if op == "normalize":
        return True, cur.normalize()
    if op == "encode_iri":
        return True, cur.encode()
    if op == "encode":
        return True, cur.encode(a[0])
    if op == "add_credentials":
        return True, cur.add_credentials(a[0], a[1])
    if op in ("add_query_from", "extend_query_with"):
        return True, getattr(cur, op)([tuple(p) for p in a[0]])
    if op == "finalize":
        return True, cur.finalize()
    if op == "validate":
        cur.validate(rfc3986.uri_reference(a[0]))
        return False, VALID
    if op == "validate_with_path":
        cur.validate(rfc3986.uri_reference(a[0]).copy_with(path=a[1]))
        return False, VALID
    if op in ("allow_schemes", "allow_hosts", "allow_ports", "check_validity_of", "require_presence_of"):
        return True, getattr(cur, op)(*a)
    if op in ("allow_use_of_password", "forbid_use_of_password"):
        return True, getattr(cur, op)()
    # builder steps taking one argument
    return True, getattr(cur, op)(*a)


def run_jobs(out):
    with open(os.path.join(HERE, "data", "jobs.jsonl"), encoding="utf-8") as f:
        jobs = [json.loads(l) for l in f if l.strip()]
    for j, steps in enumerate(jobs, 1):
        cur = None
        for k, step in enumerate(steps, 1):
            op = step[0] if step[0] != "fn" else step[1]
            try:
                if k == 1 and step[0] != "fn":
                    cur = make(step)
                    res = show(cur)
                else:
                    new, val = apply(cur, step)
                    if new and val is not None and not isinstance(val, (str, bytes, bool, dict, tuple, Valid)) or isinstance(val, (rfc3986.URIReference, rfc3986.IRIReference, ParseResult, ParseResultBytes)):
                        cur = val
                    res = show(val)
            except Exception as e:
                res = "raised %s: %s" % (type(e).__name__, e.args[0] if e.args else "")
            out.append("%d.%d %s: %s" % (j, k, op, res))
            if cur is None and step[0] != "fn":
                break  # the constructor raised: nothing to call methods on
    out.append("== %d jobs" % len(jobs))


def webhook_report(out):
    policy = (Validator().allow_schemes("https").allow_ports("443", "8443").forbid_use_of_password()
              .require_presence_of("scheme", "host")
              .check_validity_of("scheme", "userinfo", "host", "port", "path", "query", "fragment"))
    tenants = {}
    order = []
    with open(os.path.join(HERE, "data", "webhooks.tsv"), encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            tenant, base, cb = line.split("\t")
            if tenant not in tenants:
                tenants[tenant] = []
                order.append(tenant)
            tenants[tenant].append((base, cb))
    out.append("== webhooks")
    accepted = rejected = 0
    for tenant in order:
        kept = []
        out.append("tenant %s" % tenant)
        for base, cb in tenants[tenant]:
            try:
                ref = rfc3986.uri_reference(cb)
                if not ref.is_absolute():
                    ref = ref.resolve_with(base)
                ref = ref.copy_with(fragment=None).normalize()
                policy.validate(ref)
            except exceptions.RFC3986Exception as e:
                rejected += 1
                out.append("  reject %r: %s: %s" % (cb, type(e).__name__, e.args[0]))
                continue
            dup = next((i for i, (k, _) in enumerate(kept) if k == ref), None)
            if dup is not None:
                kept[dup][1].append(cb)
                out.append("  dup    %r = %s" % (cb, kept[dup][0].unsplit()))
                continue
            accepted += 1
            kept.append((ref, [cb]))
            out.append("  accept %r -> %s" % (cb, ref.unsplit()))
        for ref, cbs in kept:
            out.append("  endpoint %s (%d registration%s, port %s)" % (
                ref.unsplit(), len(cbs), "" if len(cbs) == 1 else "s", ref.port or "default"))
    out.append("== %d accepted, %d rejected" % (accepted, rejected))


def main():
    out = []
    run_jobs(out)
    webhook_report(out)
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
