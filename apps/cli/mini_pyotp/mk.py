# Writes data/: an authenticator app's export of otpauth URIs, broken
# URIs, the users and login attempts of a site that checks TOTP codes,
# the hardware tokens and button presses of a service that checks HOTP
# codes, new users to enrol, and jobs.tsv, the jobs oracle.py and
# mini_pyotp.kara run. The codes users type are made with pyotp itself
# (vendor/pyotp), some of them wrong, late, replayed or typed oddly.
import datetime
import hashlib
import os
import shutil
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.dont_write_bytecode = True
os.environ["TZ"] = "UTC"

import pyotp  # noqa: E402
from tables import table  # noqa: E402

NFKD = dict(table())


def covered(s):
    return "".join(NFKD.get(c, c) for c in s) == unicodedata.normalize("NFKD", s)


def write(rel, text):
    for line in text.splitlines():
        assert covered(line), "no NFKD table for %r" % line
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


RFC = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"  # 12345678901234567890
RFC256 = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQGEZA===="
RFC512 = ("GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"
          "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQGEZDGNA=")
DEMO = "JBSWY3DPEHPK3PXP"
ACME = "HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ"

# An authenticator's plain-text export: one otpauth URI per line.
ACCOUNTS = [
    "otpauth://totp/GitHub:octo-dev?secret=NNQXEYJNN52HALLEMVWW6LLLMV4S2MRQGI2A&issuer=GitHub",
    "otpauth://totp/Amazon%20Web%20Services:admin@example-corp?secret=KRSXG5CTMVRXEZLUKNSXG2LUMUYTEMZU&issuer=Amazon%20Web%20Services",
    "otpauth://totp/Google%3Adev%40example.org?secret=MFRGGZDFMZTWQ2LKMFRGGZDFMZTWQ2LK&issuer=Google",
    "otpauth://totp/ACME%20Co:john.doe@email.com?secret=" + ACME + "&issuer=ACME%20Co&algorithm=SHA256&digits=8&period=60",
    "otpauth://hotp/YubiKey:slot2?secret=" + RFC + "&counter=42&issuer=YubiKey",
    "otpauth://totp/Steam:gamer_42?secret=JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP&issuer=Steam&encoder=steam",
    "otpauth://totp/Dropbox:sam%40example.net?secret=" + RFC512 .replace("=", "%3D") + "&algorithm=SHA512&digits=7",
    "otpauth://totp/home-server?secret=jbswy3dpehpk3pxp",
    "otpauth://totp/My%20Bank:sam?secret=GEZDGNBVGY3TQOJQ&issuer=My+Bank",
    "otpauth://totp/?secret=MFRGGZDFMZTWQ2LK&period=15",
    "otpauth://hotp/Legacy%20VPN:ops?secret=" + DEMO + "&counter=%207&digits=8",
    "otpauth://totp/Intranet:%C3%A9lodie?secret=" + DEMO + "&digits=%D9%A8&issuer=Intranet",
]

BROKEN_URIS = [
    "https://totp/GitHub:octo?secret=" + DEMO,
    "otpauth://TOTP/GitHub:octo?secret=" + DEMO,
    "otpauth://totp/GitHub:octo?secret=" + DEMO + "&issuer=GitLab",
    "otpauth://totp/GitHub:octo?secret=" + DEMO + "&issuer=GitHub&issuer=GitLab",
    "otpauth://totp/x?secret=" + DEMO + "&digits=9",
    "otpauth://totp/x?secret=" + DEMO + "&digits=six",
    "otpauth://totp/x?secret=" + DEMO + "&algorithm=MD5",
    "otpauth://totp/x?secret=" + DEMO + "&algorithm=sha1",
    "otpauth://totp/x?issuer=Nobody",
    "otpauth://totp/x?secret=&issuer=Blank",
    "otpauth://totp/x?secret=" + DEMO + "&counter=3",
    "otpauth://hotp/x?secret=" + DEMO + "&period=60",
    "otpauth://totp/x?secret=" + DEMO + "&encoder=steam&counter=3",
    "otpauth://totp/x?secret=" + DEMO + "&encoder=steam&algorithm=SHA256&counter=1",
    "otpauth://totp/x?secret=" + DEMO + "&encoder=steam&digits=9",
    "otpauth://hotp/x?secret=" + DEMO + "&counter=-5",
    "otpauth://hotp/x?secret=" + DEMO + "&counter=1_000",
    "otpauth://totp/x?secret=" + DEMO + "&period=0",
    "otpauth://totp/x?secret=" + DEMO + "&period=-30",
    "otpauth://totp/x?secret=jbsw%20y3dp%20ehpk%203pxp",
    "otpauth://totp/x?secret=JBSWY3DPEHPK3PX1",
    "otpauth://totp/x?secret=JBSWY3DPE",
    "otpauth://totp/x?secret=JBSWY3DPEH",
    "otpauth://totp/x?secret=JBSWY3DPEHPK3PXP====",
    "otpauth://totp/x?secret=%C3%84BSWY3DPEHPK3PXP",
    "otpauth://totp/x?secret=" + DEMO + "&digits=10&encoder=steam",
    "otpauth://totp/a:b:c?secret=" + DEMO,
    "otpauth://totp/x?secret=" + DEMO + "&digits=6&digits=8",
    "otpauth://totp/x?secret=" + DEMO + "&period=+45",
    "otpauth://totp/Caf%E9:x?secret=" + DEMO,
    "otpauth:totp?secret=" + DEMO,
    "otpauth://totp/x?secret=" + DEMO + "&secret=MFRGGZDFMZTWQ2LK&image=x",
]

# A site's users: name, secret and the TOTP settings it enrolled them with.
USERS = [
    ("alice", "NNQXEYJNN52HALLEMVWW6LLLMV4S2MRQGI2A", {}),
    ("bob", DEMO, {"digits": 8}),
    ("carol", ACME, {"digest": "sha256", "interval": 60}),
    ("dave", RFC512, {"digest": "sha512", "digits": 8}),
    ("erin", "MFRGGZDFMZTWQ2LK", {}),
]


def iso(t):
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def user_totp(name):
    for n, s, o in USERS:
        if n == name:
            kw = dict(o)
            if "digest" in kw:
                kw["digest"] = getattr(hashlib, kw["digest"])
            return pyotp.TOTP(s, **kw)


def fullwidth(code):
    return "".join(chr(0xFF10 + int(c)) for c in code)


def attempts():
    t0 = 1709993100  # 2024-03-09 14:05:00 UTC
    rows = []

    def code(user, t, step=0):
        return user_totp(user).at(t, step)

    rows.append((t0 + 7, "alice", code("alice", t0 + 7)))
    rows.append((t0 + 9, "alice", code("alice", t0 + 7)))           # the same code again: replay
    rows.append((t0 + 40, "alice", code("alice", t0 + 40, -1)))      # last step's code, already used
    rows.append((t0 + 65, "alice", code("alice", t0 + 65, -1)))      # one step late
    rows.append((t0 + 70, "bob", code("bob", t0 + 70)[:4] + " " + code("bob", t0 + 70)[4:]))
    rows.append((t0 + 80, "bob", "12345678"))
    rows.append((t0 + 81, "bob", "87654321"))
    rows.append((t0 + 82, "bob", "11111111"))
    rows.append((t0 + 90, "bob", code("bob", t0 + 90)))              # locked out
    rows.append((t0 + 400, "bob", code("bob", t0 + 400)))            # the lock has run out
    rows.append((t0 + 100, "carol", fullwidth(code("carol", t0 + 100))))
    rows.append((t0 + 130, "carol", code("carol", t0 + 130, 1)))     # the next step's code, a step early
    rows.append((t0 + 140, "carol", code("carol", t0 + 140, 2)))     # two steps early
    rows.append((t0 + 200, "dave", code("dave", t0 + 200)))
    rows.append((t0 + 230, "dave", code("dave", t0 + 230)[:4] + "-" + code("dave", t0 + 230)[4:]))
    c = code("erin", t0 + 250)
    rows.append((t0 + 250, "erin", "".join("٠١٢٣٤٥٦٧٨٩"[int(d)] for d in c)))
    rows.append((t0 + 251, "erin", c[:5] + "¹²³⁴⁵⁶⁷⁸⁹⁰"[(int(c[5]) - 1) % 10]))
    rows.append((t0 + 252, "erin", "\u24ea\u2460\u2461\u2462\u2463\u2464\u2465\u2466\u2467\u2468"[int(c[0])] + c[1:]))
    rows.append((t0 + 260, "mallory", "000000"))
    rows.append((t0 + 300, "erin", code("erin", t0 + 300)))
    rows.sort(key=lambda r: r[0])
    return "".join("%s\t%s\t%s\n" % (iso(t), u, c) for t, u, c in rows)


# Hardware HOTP tokens: serial, secret and the counter the server expects.
TOKENS = [
    ("YK-0001", RFC, 0),
    ("YK-0002", DEMO, 100),
    ("YK-0003", "MFRGGZDFMZTWQ2LK", 5),
]


def presses():
    tok = dict((s, pyotp.HOTP(k)) for s, k, _ in TOKENS)
    rows = [
        ("YK-0001", tok["YK-0001"].at(0)),
        ("YK-0001", tok["YK-0001"].at(1)),
        ("YK-0001", tok["YK-0001"].at(1)),     # a replayed press
        ("YK-0001", tok["YK-0001"].at(5)),     # pressed a few times away from the server
        ("YK-0002", tok["YK-0002"].at(150)),   # far ahead: needs a second code
        ("YK-0002", tok["YK-0002"].at(151)),   # the next one: resynchronised
        ("YK-0002", tok["YK-0002"].at(152)),
        ("YK-0003", tok["YK-0003"].at(40)),    # far ahead
        ("YK-0003", tok["YK-0003"].at(42)),    # not the next one
        ("YK-0003", tok["YK-0003"].at(4)),     # behind the server
        ("YK-0003", "123456"),
        ("YK-9999", "000000"),
        ("YK-0003", tok["YK-0003"].at(200)),   # beyond any window
        ("YK-0003", tok["YK-0003"].at(201)),
    ]
    return "".join("%s\t%s\n" % r for r in rows)


# New users to enrol: email, the issuer to show, and extra URI parameters.
ENROL = [
    ("new.hire@example.org", "Example Corp", ""),
    ("ops+oncall@example.org", "Example Corp: Ops", ""),
    ("jürgen@example.de", "Beispiel GmbH", ""),
    ("pat", "", "image=https://example.org/logo.png"),
    ("lee", "Shop", "image=http://example.org/logo.png"),
    ("kim", "Shop", "image=https://example.org"),
    ("sam/admin", "Shop & Co", "color=green"),
]


def jobs():
    j = []
    j.append(["hotp", "secret=" + RFC, "at=0,1,2,3,4,5,6,7,8,9"])
    j.append(["hotp", "secret=" + RFC, "at=-1,0,4294967295,4294967296,18446744073709551615,18446744073709551616"])
    j.append(["hotp", "secret=" + RFC, "initial_count=10", "at=0,-10,-11"])
    for d in ["sha1", "sha224", "sha256", "sha384", "sha512"]:
        j.append(["hotp", "secret=" + RFC, "digest=" + d, "digits=8", "at=0,1,2"])
    for n in ["0", "1", "5", "9", "10", "11"]:
        j.append(["hotp", "secret=" + RFC, "digits=" + n, "at=0,1"])
    j.append(["hotp", "secret=" + RFC, "digest=md5", "at=0"])
    j.append(["hotp", "secret=" + RFC, "interval=30", "at=0"])
    j.append(["hotp", "secret=", "at=0,1"])
    for s in ["jbswy3dpehpk3pxp", "JBSW Y3DP EHPK 3PXP", "JBSWY3DPEHPK3PX0", "JBSWY3DPEHPK3PX8", "JBSWY3DPE",
              "JBSWY3DPEH", "JBSWY3DPEHP", "JBSWY3DPEHPK", "JBSWY3DPEHPK3", "JBSWY3DPEHPK3P", "JBSWY3DPEHPK3PX",
              "JBSWY3DPEHPK3PXP====", "JBSWY3DPEHPK3PXP========", "JBSWY3DP=HPK3PXP", "MFRGGZDFMZTWQ2LK=",
              "ÄBSWY3DPEHPK3PXP", "jbswy3dpehpk3pxpjbswy3dp", "AAAAAAAA", "77777777", "MZXW6===", "MZXW6YQ="]:
        j.append(["secret", s])
    t = "59,1111111109,1111111111,1234567890,2000000000,20000000000"
    j.append(["totp", "secret=" + RFC, "digits=8", "at=" + t])
    j.append(["totp", "secret=" + RFC256, "digest=sha256", "digits=8", "at=" + t])
    j.append(["totp", "secret=" + RFC512, "digest=sha512", "digits=8", "at=" + t])
    j.append(["totp", "secret=" + DEMO, "at=0,1,29,30,-1,-29,-30,-31,-59,-60"])
    j.append(["totp", "secret=" + DEMO, "at=253402300799,253402300800,-62135510400,-62135596800,-62135596801"])
    j.append(["totp", "secret=" + DEMO, "at=2024-03-09T14:05:07Z,2024-03-09T14:05:07.999+05:30,2024-03-09 14:05:07,"
              "2024-03-09T14:05:29.999999,1969-12-31T23:59:59Z,1969-12-31T23:59:30-00:30"])
    j.append(["totp", "secret=" + DEMO, "at=0001-01-01T00:30:00+01:00,9999-12-31T23:59:59-01:00,0001-01-01T00:00:00"])
    j.append(["totp", "secret=" + DEMO, "counter_offset=-1", "at=0,29,30,1709993107"])
    j.append(["totp", "secret=" + DEMO, "counter_offset=5", "at=1709993107"])
    j.append(["totp", "secret=" + DEMO, "interval=60", "at=59,60,-1,-60,-61"])
    j.append(["totp", "secret=" + DEMO, "interval=7", "at=1709993107"])
    j.append(["totp", "secret=" + DEMO, "interval=0", "at=10"])
    j.append(["totp", "secret=" + DEMO, "interval=-30", "at=0,-31,1709993107"])
    j.append(["totp", "secret=" + DEMO, "initial_count=3", "at=0"])
    j.append(["totp", "secret=" + DEMO, "digits=11", "at=0"])
    j.append(["steam", "secret=" + DEMO, "at=0,30,1709993107,2000000000"])
    j.append(["steam", "secret=JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP", "digits=9", "interval=10", "at=1709993107"])
    j.append(["steam", "secret=" + DEMO, "digest=sha256", "at=0"])
    # verify
    h = pyotp.HOTP(RFC)
    j.append(["verify_hotp", "secret=" + RFC, "otp=" + h.at(9), "counter=9,10,8"])
    j.append(["verify_hotp", "secret=" + RFC, "otp=" + fullwidth(h.at(3)), "counter=3"])
    j.append(["verify_hotp", "secret=" + RFC, "otp=" + h.at(3) + " ", "counter=3"])
    j.append(["verify_hotp", "secret=" + RFC, "otp=0" + h.at(3), "counter=3"])
    j.append(["verify_hotp", "secret=" + RFC, "otp=x", "counter=-1"])
    tt = pyotp.TOTP(DEMO)
    c = tt.at(1709993107)
    for w in ["0", "1", "2", "-1"]:
        j.append(["verify_totp", "secret=" + DEMO, "otp=" + c, "valid_window=" + w, "for_time=1709993107,1709993137,1709993167,1709993077,1709993047"])
    j.append(["verify_totp", "secret=" + DEMO, "otp=" + c, "for_time=2024-03-09T14:05:20Z,2024-03-09T19:35:20+05:30,2024-03-09T14:05:40Z"])
    j.append(["verify_totp", "secret=" + DEMO, "otp=" + tt.at(1709993107, -1), "valid_window=1", "for_time=1709993107"])
    j.append(["verify_totp", "secret=" + DEMO, "otp=" + "０" * 6, "valid_window=1", "for_time=1709993107"])
    # provisioning URIs
    j.append(["provision", "kind=totp", "secret=" + DEMO])
    j.append(["provision", "kind=totp", "secret=" + DEMO, "name=alice@example.org", "issuer=Example Corp"])
    j.append(["provision", "kind=totp", "secret=" + DEMO, "digest=sha256", "digits=8", "interval=60", "p.name=bob", "p.issuer_name=Acme"])
    j.append(["provision", "kind=totp", "secret=" + DEMO, "digest=sha384", "name=x"])
    j.append(["provision", "kind=totp", "secret=" + DEMO, "digest=sha224", "digits=7", "interval=30", "name=x", "issuer=a:b"])
    j.append(["provision", "kind=hotp", "secret=wrn3pqx5uqxqvnqr", "name=mark@percival"])
    j.append(["provision", "kind=hotp", "secret=wrn3pqx5uqxqvnqr", "name=mark@percival", "initial_count=12"])
    j.append(["provision", "kind=hotp", "secret=wrn3pqx5uqxqvnqr", "name=mark@percival", "initial_count=12", "p.initial_count=0"])
    j.append(["provision", "kind=hotp", "secret=wrn3pqx5uqxqvnqr", "initial_count=12", "p.initial_count=3", "p.name=other"])
    j.append(["provision", "kind=totp", "secret=" + DEMO, "name=", "issuer=", "p.image=https://example.org/i.png"])
    j.append(["provision", "kind=totp", "secret=" + DEMO, "name=a b+c&d=e?f#g", "issuer=x y/z", "p.label=Ünïcode ✓"])
    j.append(["provision", "kind=totp", "secret=" + DEMO, "p.image=ftp://example.org/i.png"])
    j.append(["provision", "kind=totp", "secret=" + DEMO, "p.image=https://example.org"])
    j.append(["provision", "kind=totp", "secret=" + DEMO, "p.image=https:///i.png?x=1#f"])
    j.append(["provision", "kind=steam", "secret=" + DEMO, "name=gamer", "issuer=Steam"])
    j.append(["random", "base32", "16"])
    j.append(["random", "base32", "31"])
    j.append(["random", "hex", "39"])
    j.append(["random", "hex", "0"])
    j.append(["uris", "accounts.txt"])
    j.append(["uris", "broken-uris.txt"])
    j.append(["authenticator", "accounts.txt", "1709993107"])
    j.append(["authenticator", "accounts.txt", "2024-03-09T14:05:59Z"])
    j.append(["login", "users.tsv", "attempts.log"])
    j.append(["tokens", "tokens.tsv", "presses.log"])
    j.append(["enrol", "enrol.tsv", "1709993107"])
    return j


def main():
    shutil.rmtree(DATA, ignore_errors=True)
    write("accounts.txt", "".join(u + "\n" for u in ACCOUNTS))
    write("broken-uris.txt", "".join(u + "\n" for u in BROKEN_URIS))
    write("users.tsv", "".join("%s\t%s\t%s\n" % (n, s, " ".join("%s=%s" % kv for kv in o.items())) for n, s, o in USERS))
    write("attempts.log", attempts())
    write("tokens.tsv", "".join("%s\t%s\t%d\n" % t for t in TOKENS))
    write("presses.log", presses())
    write("enrol.tsv", "".join("%s\t%s\t%s\n" % e for e in ENROL))
    write("jobs.tsv", "".join("\t".join(job) + "\n" for job in jobs()))


main()
