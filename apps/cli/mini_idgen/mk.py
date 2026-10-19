# Writes data/: the order, event, link and request files the reports read,
# and data/jobs.jsonl. Run from this directory; oracle.py and
# mini_idgen.kara read data/.
import json
import os
import random

rnd = random.Random(116)
jobs = []


def job(**kw):
    jobs.append(kw)


# ------------------------------------------------------------ UUID(...)

HEX = [
    "12345678-1234-5678-1234-567812345678",
    "{12345678-1234-5678-1234-567812345678}",
    "urn:uuid:12345678-1234-5678-1234-567812345678",
    "12345678123456781234567812345678",
    "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
    "00000000-0000-0000-0000-000000000000",
    "ffffffff-ffff-ffff-ffff-ffffffffffff",
    "FFFFFFFF-FFFF-4FFF-BFFF-FFFFFFFFFFFF",
    "a8098c1a-f86e-11da-bd1a-00112444be1e",
    "6fa459ea-ee8a-3ca4-894e-db77e160355e",
    "886313e1-3b8a-5372-9b90-0c9aee199e5d",
    "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
    "{{{12345678-1234-5678-1234-567812345678}}",
    "uuid:urn:12345678-1234-5678-1234-567812345678",
    "1234-5678-1234-5678-1234-5678-1234-5678",
    "0x345678-1234-5678-1234-567812345678",
    "12_45678-1234-5678-1234-567812345678",
    "+2345678-1234-5678-1234-567812345678",
    " 2345678-1234-5678-1234-56781234567 ",
    "１２345678-1234-5678-1234-567812345678",
    "12345678-1234-5678-1234-56781234567",
    "12345678-1234-5678-1234-5678123456789",
    "12345678-1234-5678-1234-56781234567g",
    "12_4567_-1234-5678-1234-567812345678",
    "0x_45678-1234-5678-1234-567812345678",
    "",
    "urn:uuid:",
    "xurn:uuid:12345678-1234-5678-1234-567812345678",
    "c232ab00-9414-11ec-b3c8-9e6bdeced846",
    "00000000-0000-8000-c000-000000000000",
    "00000000-0000-0000-e000-000000000000",
    "00000000-0000-f000-6000-000000000000",
]
for h in HEX:
    job(op="uuid", hex=h)
for h in HEX[:8]:
    for v in [1, 3, 4, 5]:
        job(op="uuid", hex=h, version=v)
job(op="uuid", hex=HEX[0], version=0)
job(op="uuid", hex=HEX[0], version=6)

BYTES = [
    list(range(16)),
    [0x12, 0x34, 0x56, 0x78] * 4,
    [255] * 16,
    [0] * 15 + [1],
    [ord(c) for c in "abcdefghijklmnop"],
    [39, 34, 92, 9, 10, 13, 127, 128, 32, 126, 0, 1, 2, 3, 4, 5],
    [39] * 16,
    [39, 34] * 8,
    list(range(15)),
    list(range(17)),
]
for b in BYTES:
    job(op="uuid", bytes=b)
    job(op="uuid", bytes_le=b)
job(op="uuid", bytes=BYTES[0], version=4)
job(op="uuid", bytes_le=BYTES[1], version=2)

FIELDS = [
    [0x12345678, 0x1234, 0x5678, 0x12, 0x34, 0x567812345678],
    [0, 0, 0, 0, 0, 0],
    [0xffffffff, 0xffff, 0xffff, 0xff, 0xff, 0xffffffffffff],
    [1 << 32, 0, 0, 0, 0, 0],
    [0, 1 << 16, 0, 0, 0, 0],
    [0, 0, -1, 0, 0, 0],
    [0, 0, 0, 256, 0, 0],
    [0, 0, 0, 0, 300, 0],
    [0, 0, 0, 0, 0, 1 << 48],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5, 6, 7],
]
for f in FIELDS:
    job(op="uuid", fields=f)
job(op="uuid", fields=FIELDS[0], version=1)

INTS = ["0", "1", str(1 << 127), str((1 << 128) - 1), str(1 << 128), "-1",
        str(0x12345678123456781234567812345678), "24197857161011715162171839636988778104"]
for i in INTS:
    job(op="uuid", int=i)
job(op="uuid", int=INTS[2], version=3)
job(op="uuid")
job(op="uuid", hex=HEX[0], int="5")
job(op="uuid", bytes=BYTES[0], fields=FIELDS[0])

# ------------------------------------------------------- comparisons

for k in range(4):
    us = [HEX[rnd.randrange(len(HEX) // 2)] for _ in range(6)] + \
         ["%032x" % rnd.getrandbits(128) for _ in range(6)]
    job(op="sort", uuids=us)

# -------------------------------------------------- uuid1 (clock given)

# Each job is one run of uuid1 calls at the given times. The last
# timestamp carries over from job to job, as it does in one process.
T0 = 1729324800 * 10**9  # 2024-10-19 08:00:00 UTC
job(op="uuid1", calls=[[T0, 0x0242ac110002, 0x1234], [T0 + 100, 0x0242ac110002, 0x1234],
                       [T0 + 150, 0x0242ac110002, 0x1234], [T0 + 150, 0x0242ac110002, 0x1234],
                       [T0 - 5000, 0x0242ac110002, 0x1234], [T0 + 10**9, 0x0242ac110002, 0x1234]])
job(op="uuid1", calls=[[T0 + 2 * 10**9, 0, 0], [T0 + 3 * 10**9, (1 << 48) - 1, (1 << 14) - 1],
                       [T0 + 4 * 10**9, 0x1, 1 << 14], [T0 + 5 * 10**9, 0x2, (1 << 16) + 7]])
job(op="uuid1", calls=[[0, 0xdeadbeef, 99], [10**18, 0xdeadbeef, 99],
                       [2**62, 0xdeadbeef, 99], [9 * 10**18, 0xdeadbeef, 99]])
job(op="uuid1", calls=[[1, 0x00163e000001, 7]])

# ------------------------------------------------------ uuid3 and uuid5

NAMES = ["python.org", "www.example.com", "http://example.com/a?b=c", "", "a",
         "1.3.6.1.4.1.343", "cn=John Smith,o=Example,c=US", "naïve café", "日本語ドメイン.jp",
         "x" * 55, "y" * 56, "z" * 64, "w" * 119, "q" * 120, "\x00\x01\x02", "🙂 emoji"]
for fn in ["uuid3", "uuid5"]:
    for ns in ["@dns", "@url", "@oid", "@x500"]:
        for n in NAMES:
            job(op=fn, namespace=ns, name=n)
    for ns in ["12345678-1234-5678-1234-567812345678", "00000000-0000-0000-0000-000000000000"]:
        for n in NAMES[:5]:
            job(op=fn, namespace=ns, name=n)
    job(op=fn, namespace="@dns", name_bytes=[0, 255, 128, 10])

# --------------------------------------------------------------- uuid4

for k in range(8):
    job(op="uuid4", bytes=[rnd.randrange(256) for _ in range(16)])
job(op="uuid4", bytes=[0] * 16)
job(op="uuid4", bytes=[255] * 16)

# ------------------------------------------------------------- hashids

HASHIDS = [
    {},
    {"salt": "this is my salt"},
    {"salt": "this is my salt", "min_length": 8},
    {"salt": "arbitrary salt", "min_length": 16, "alphabet": "abcdefghijkl0123456"},
    {"salt": "acme-orders", "min_length": 6},
    {"salt": "acme-orders", "min_length": 40},
    {"salt": "", "min_length": 0, "alphabet": "0123456789abcdef"},
    {"salt": "short", "alphabet": "abcdefghijklmnopqrstuvwxyz"},
    {"salt": "caps", "alphabet": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"},
    {"salt": "seps only", "alphabet": "cfhistuCFHISTUabc"},
    {"salt": "dupes", "alphabet": "aabbccddeeffgghhiijjkkllmmnnoopp"},
    {"salt": "ünïcödé sält", "alphabet": "αβγδεζηθικλμνξοπρστυφχψω0123456789"},
    {"salt": "x", "min_length": -5},
    {"alphabet": "abcdefghijklmno"},
    {"alphabet": "abcdefghijklmnop"},
    {"alphabet": "cfhistu"},
    {"salt": "a very very very very very very very very very very long salt indeed"},
]
VALUES = [[1], [0], [12345], [1, 2, 3], [1, 23, 456], [683, 94108, 123, 5], [0, 0, 0],
          [2 ** 40], [2 ** 62], [7, -1], [], [99, 25, 1001, 7, 0, 3, 64, 81, 22, 5000]]
for h in HASHIDS:
    enc = []
    for v in VALUES:
        enc.append(v)
    job(op="hashids", config=h, encode=enc,
        decode=["", "a", "NkK9", "laHquq", "gB0NV05e", "jR", "xLmOP", "1d6216i30h53elk3", "QNrmM", "Ö"],
        encode_hex=["507f1f77bcf86cd799439011", "deadbeef", "", "0", "FFFFFFFFFFFFFFFFFFFFFFFF",
                    "xyz", "5_0", " 1"],
        roundtrip=True)

# ----------------------------------------------------------- shortuuid

SU = [None, "01", "0123456789abcdef", "abcdefghijklmnopqrstuvwxyz",
      "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz",
      "zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA9876543210-_",
      "aaaa", "ab", "αβγ", "", "AAAAAAAAAB"]
for a in SU:
    job(op="shortuuid", alphabet=a,
        encode=[[HEX[0], None], [HEX[5], None], [HEX[6], None], [HEX[4], 5], [HEX[4], 0], [HEX[5], 3]],
        decode=[["CXc85b4rqinB7s5J52TRYb", False], ["CXc85b4rqinB7s5J52TRYb", True], ["", False],
                ["2", False], ["0000", False], ["zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz", False],
                ["!", False], ["11111111111111111111111111111111111111111111111111111111111111111111111"
                               "11111111111111111111111111111111111111111111111111111111111", False]],
        names=[["example.com", None], ["http://example.com", None], ["HTTPS://Example.com/x", None],
               ["Https://", 4], ["", None]],
        lengths=[16, 8, 1, 0, 32])

# --------------------------------------------------------------- data

os.makedirs("data", exist_ok=True)

TENANTS = [("acme", "acme-orders"), ("globex", "globex 2024"), ("initech", "TPS reports")]
lines = ["tenant,order_id,customer_id,amount_cents"]
for k in range(30):
    t = TENANTS[rnd.randrange(3)][0]
    lines.append("%s,%d,%d,%d" % (t, 1000 + k * 37 + rnd.randrange(30), rnd.randrange(1, 500),
                                   rnd.randrange(100, 100000)))
lines.append("acme,notanumber,1,5")
lines.append("umbrella,5,1,5")
lines.append("globex,-4,1,5")
open("data/orders.csv", "w").write("\n".join(lines) + "\n")

open("data/tenants.txt", "w").write("".join("%s %s\n" % t for t in TENANTS))

# Event ids are version-1 UUIDs minted by three hosts; the report reads the
# time and host back out of them.
import uuid  # noqa: E402

HOSTS = [0x0242ac110002, 0x0242ac110003, 0x3c22fb7a10de]
ev = []
t = 1729324800 * 10**9 + 123456789
for k in range(24):
    t += rnd.randrange(1, 4 * 10**9)
    host = HOSTS[rnd.randrange(3)]
    seq = rnd.randrange(1 << 14)
    ts = t // 100 + 0x01b21dd213814000
    u = uuid.UUID(fields=(ts & 0xffffffff, (ts >> 32) & 0xffff, (ts >> 48) & 0x0fff,
                          (seq >> 8) & 0x3f, seq & 0xff, host), version=1)
    kind = rnd.choice(["order.created", "order.paid", "order.shipped", "user.login", "cart.updated"])
    ev.append((str(u), kind))
rnd.shuffle(ev)
ev.append(("not-a-uuid", "junk"))
ev.append((str(uuid.UUID(int=0x12345678123456781234567812345678, version=4)), "random.id"))
open("data/events.log", "w").write("".join("%s %s\n" % e for e in ev))

LINKS = ["https://example.com/docs/getting-started", "https://example.com/pricing",
         "http://blog.example.com/2024/10/launch", "https://example.com/docs/getting-started",
         "example.com/no-scheme", "HTTPS://EXAMPLE.COM/Upper", "ftp://files.example.com/a.zip",
         "https://example.com/search?q=uuid&lang=en", "https://例え.jp/パス"]
open("data/links.txt", "w").write("\n".join(LINKS) + "\n")

with open("data/jobs.jsonl", "w", encoding="utf-8") as fh:
    for j in jobs:
        fh.write(json.dumps(j, ensure_ascii=False) + "\n")
    for op in ["orders", "events", "links", "incoming"]:
        fh.write(json.dumps({"op": op}) + "\n")
print(len(jobs) + 4, "jobs")
