# Runs data/jobs.tsv through pyotp itself (vendor/pyotp, unchanged) and
# prints what each job gives; expected.out is this output.
import base64
import datetime
import hashlib
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.dont_write_bytecode = True
os.environ["TZ"] = "UTC"
time.tzset()

import pyotp  # noqa: E402
from pyotp import contrib, utils  # noqa: E402

DATA = os.path.join(HERE, "data")
CLASSES = {"hotp": pyotp.HOTP, "totp": pyotp.TOTP, "steam": contrib.Steam}
INTS = ("digits", "interval", "initial_count", "counter_offset", "valid_window", "p.initial_count")


def show(text):
    out = []
    for c in text:
        if c == "\r":
            out.append("<CR>")
        elif (c < " " and c not in "\t\n") or c == "\x7f":
            out.append("<x%02x>" % ord(c))
        else:
            out.append(c)
    return "".join(out)


def err(e):
    return "error: %s: %s" % (type(e).__name__, e)


def read(name):
    with open(os.path.join(DATA, name), encoding="utf-8", newline="") as f:
        return f.read()


def lines(name):
    return read(name).split("\n")[:-1]


def fields(args):
    kw = {}
    for a in args:
        k, v = a.split("=", 1)
        kw[k] = int(v) if k in INTS else v
    return kw


def when(text):
    if re.fullmatch(r"-?[0-9]+", text):
        return int(text)
    return datetime.datetime.fromisoformat(text)


def make(kind, kw):
    args = {}
    for k, v in kw.items():
        if k in ("kind", "secret", "at", "otp", "counter", "for_time", "counter_offset", "valid_window") or k.startswith("p."):
            continue
        args[k] = getattr(hashlib, v) if k == "digest" else v
    return CLASSES[kind](kw["secret"], **args)


def describe(otp):
    extra = "initial_count=%d" % otp.initial_count if isinstance(otp, pyotp.HOTP) else "interval=%d" % otp.interval
    return "%s name=%r issuer=%r digits=%d digest=%s %s secret=%r" % (
        type(otp).__name__, otp.name, otp.issuer, otp.digits, otp.digest().name, extra, otp.secret)


def first_code(otp):
    try:
        if isinstance(otp, pyotp.HOTP):
            return "at(0) = " + otp.at(0)
        return "at(1709993107) = " + otp.at(1709993107)
    except Exception as e:
        return err(e)


def codes_job(kind, args):
    kw = fields(args)
    try:
        otp = make(kind, kw)
    except Exception as e:
        print(err(e))
        return
    for t in kw["at"].split(","):
        try:
            if kind == "hotp":
                code = otp.at(int(t))
            elif "counter_offset" in kw:
                code = otp.at(when(t), kw["counter_offset"])
            else:
                code = otp.at(when(t))
            print("at(%s) = %s" % (t, code))
        except Exception as e:
            print("at(%s): %s" % (t, err(e)))


def verify_hotp_job(args):
    kw = fields(args)
    otp = make("hotp", kw)
    for c in kw["counter"].split(","):
        try:
            print(show("verify(%r, %s) = %s" % (kw["otp"], c, otp.verify(kw["otp"], int(c)))))
        except Exception as e:
            print(show("verify(%r, %s): %s" % (kw["otp"], c, err(e))))


def verify_totp_job(args):
    kw = fields(args)
    otp = make("totp", kw)
    for t in kw["for_time"].split(","):
        try:
            if "valid_window" in kw:
                ok = otp.verify(kw["otp"], when(t), kw["valid_window"])
            else:
                ok = otp.verify(kw["otp"], when(t))
            print(show("verify(%r, %s) = %s" % (kw["otp"], t, ok)))
        except Exception as e:
            print(show("verify(%r, %s): %s" % (kw["otp"], t, err(e))))


def parse_back(uri):
    try:
        back = pyotp.parse_uri(uri)
        print("  parsed: " + describe(back))
        print("  " + first_code(back))
    except Exception as e:
        print("  parsed: " + err(e))


def provision_job(args):
    kw = fields(args)
    try:
        otp = make(kw["kind"], kw)
        p = dict((k[2:], v) for k, v in kw.items() if k.startswith("p."))
        uri = otp.provisioning_uri(**p)
    except Exception as e:
        print(err(e))
        return
    print(uri)
    parse_back(uri)


def secret_job(args):
    try:
        print(pyotp.HOTP(args[0]).byte_secret().hex())
    except Exception as e:
        print(err(e))


def random_job(args):
    f = pyotp.random_base32 if args[0] == "base32" else pyotp.random_hex
    try:
        s = f(length=int(args[1]))
        print("%d characters" % len(s))
    except Exception as e:
        print(err(e))


def uris_job(args):
    for line in lines(args[0]):
        print(show(line))
        try:
            otp = pyotp.parse_uri(line)
        except Exception as e:
            print("  " + err(e))
            continue
        print("  " + describe(otp))
        print("  " + first_code(otp))
        try:
            uri = otp.provisioning_uri()
            print("  uri: " + uri)
        except Exception as e:
            print("  uri: " + err(e))


# --- programs

def authenticator_job(args):
    t = when(args[1])
    stamp = t if isinstance(t, int) else int(t.timestamp())
    accounts = []
    for line in lines(args[0]):
        otp = pyotp.parse_uri(line)
        accounts.append(((otp.issuer or "").lower(), otp.name.lower(), otp))
    accounts.sort(key=lambda a: (a[0], a[1]))
    for _, _, otp in accounts:
        label = otp.name if otp.issuer is None else "%s (%s)" % (otp.issuer, otp.name)
        if isinstance(otp, pyotp.HOTP):
            print("%-40s %s  counter %d" % (label, otp.at(0), otp.initial_count))
            continue
        try:
            code = otp.at(t)
            left = otp.interval - stamp % otp.interval
            print("%-40s %s  %2ds left, next %s" % (label, code, left, otp.at(t, 1)))
        except Exception as e:
            print("%-40s %s" % (label, err(e)))


def user_otp(spec):
    secret, opts = spec
    kw = {}
    for o in opts.split():
        k, v = o.split("=", 1)
        kw[k] = getattr(hashlib, v) if k == "digest" else int(v)
    return pyotp.TOTP(secret, **kw)


def login_job(args):
    users = {}
    for line in lines(args[0]):
        name, secret, opts = line.split("\t")
        users[name] = user_otp((secret, opts))
    last_step = {}
    fails = {}
    locked_until = {}
    for line in lines(args[1]):
        stamp, name, typed = line.split("\t")
        t = datetime.datetime.fromisoformat(stamp)
        now = int(t.timestamp())
        head = show("%s %s %r:" % (stamp, name, typed))
        if name not in users:
            print(head + " no such user")
            continue
        if locked_until.get(name, 0) > now:
            print(head + " locked for %ds more" % (locked_until[name] - now))
            continue
        otp = users[name]
        code = typed.replace(" ", "").replace("-", "")
        step = otp.timecode(t)
        matched = None
        for i in (-1, 0, 1):
            if utils.strings_equal(code, otp.at(t, i)):
                matched = step + i
                break
        if matched is None:
            fails[name] = fails.get(name, 0) + 1
            if fails[name] >= 3:
                locked_until[name] = now + 300
                fails[name] = 0
                print(head + " wrong code; locked for 300s")
            else:
                print(head + " wrong code (%d of 3)" % fails[name])
        elif matched <= last_step.get(name, -1):
            print(head + " replayed code from step %d" % matched)
        else:
            last_step[name] = matched
            fails[name] = 0
            drift = matched - step
            print(head + " accepted at step %d%s" % (matched, "" if drift == 0 else " (drift %+d)" % drift))


def tokens_job(args):
    tokens = {}
    for line in lines(args[0]):
        serial, secret, counter = line.split("\t")
        tokens[serial] = [pyotp.HOTP(secret), int(counter), None]
    for line in lines(args[1]):
        serial, code = line.split("\t")
        head = "%s %s:" % (serial, code)
        if serial not in tokens:
            print(head + " unknown token")
            continue
        tok = tokens[serial]
        hotp, counter, pending = tok
        found = None
        for c in range(counter, counter + 10):
            if hotp.verify(code, c):
                found = c
                break
        if found is not None:
            tok[1] = found + 1
            tok[2] = None
            print(head + " accepted at %d, next %d" % (found, tok[1]))
            continue
        if pending is not None and hotp.verify(code, pending + 1):
            tok[1] = pending + 2
            tok[2] = None
            print(head + " resynchronised at %d, next %d" % (pending + 1, tok[1]))
            continue
        tok[2] = None
        for c in range(counter, counter + 100):
            if hotp.verify(code, c):
                tok[2] = c
                break
        if tok[2] is not None:
            print(head + " out of sync; press again")
        else:
            print(head + " rejected")


def enrol_job(args):
    t = int(args[1])
    for line in lines(args[0]):
        email, issuer, extra = line.split("\t")
        secret = base64.b32encode(hashlib.sha1(email.encode("utf-8")).digest()).decode("ascii")
        otp = pyotp.TOTP(secret, name=email, issuer=issuer or None)
        kw = dict(e.split("=", 1) for e in extra.split()) if extra else {}
        print(show("%s (%s):" % (email, issuer or "no issuer")))
        try:
            uri = otp.provisioning_uri(**kw)
        except Exception as e:
            print("  " + err(e))
            continue
        print("  " + uri)
        back = pyotp.parse_uri(uri)
        same = back.secret == otp.secret and back.name == otp.name and back.issuer == otp.issuer
        print("  round trip %s, code %s" % ("ok" if same else "differs: " + describe(back), back.at(t)))


JOBS = {
    "hotp": lambda a: codes_job("hotp", a), "totp": lambda a: codes_job("totp", a),
    "steam": lambda a: codes_job("steam", a), "verify_hotp": verify_hotp_job, "verify_totp": verify_totp_job,
    "provision": provision_job, "secret": secret_job, "random": random_job, "uris": uris_job,
    "authenticator": authenticator_job, "login": login_job, "tokens": tokens_job, "enrol": enrol_job,
}


def main():
    for line in lines("jobs.tsv"):
        job = line.split("\t")
        print("== " + show(" ".join(job)))
        JOBS[job[0]](job[1:])


main()
