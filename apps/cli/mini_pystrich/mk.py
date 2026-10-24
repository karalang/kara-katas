"""Write data/: payloads for pyStrich's Data Matrix and Aztec encoders, a
product table and a list of tickets for the two programs, and
data/jobs.txt, the jobs that run them.

A job is one line:
    dm <payload> [options]   DataMatrixEncoder on the payload file
    az <payload> [options]   AztecEncoder on the payload file
    !labels <csv>            GS1 Data Matrix labels for a product table
    !tickets <txt>           Aztec tickets, one record a line
    !capacity                symbol sizes for generated payloads

Options are key=value words: shape=square|rectangular|auto, bytes (force
byte mode), enc=str|auto|ascii|iso-8859-1|utf-8|compat, ecc=N, kind=,
layers=N, qz=N, and art (print the symbol).

Run: python3 -s -P -B mk.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
FILES = []
JOBS = []


def put(rel, text):
    path = os.path.join(D, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text.encode("utf-8"))
    FILES.append(rel)
    return rel


def pay(name, text):
    return put("payloads/%s.txt" % name, text)


def job(line):
    JOBS.append(line)


def section(title):
    JOBS.append("# " + title)


# ------------------------------------------------------------ payloads

hudora = pay("hudora", "HuDoRa")
hello = pay("hello", "Hello, World!")
empty = pay("empty", "")
one = pay("one", "a")
nul = pay("nul", "\x00")
digits = pay("digits", "1234567890")
odd_digits = pay("odd_digits", "12345")
upper = pay("upper", "ABCDEFGHIJKLMNOP")
lower = pay("lower", "the quick brown fox jumps over the lazy dog")
x12 = pay("x12", "ABC*123>XYZ\rDEF GHI")
url = pay("url", "https://example.com/orders?id=1042&ref=mail")
latin1 = pay("latin1", "Rausschmeißer")
cafe = pay("cafe", "café crème brûlée")
greek = pay("greek", "Ελληνικά")
emoji = pay("emoji", "\U0001f4e6 parcel 42")
control = pay("control", "\x01\x02tab\there\x1bESC")
mixed_case = pay("mixed_case", "ORDER no. 42 for Mr Smith: 3 x Widget-XL")
serial = pay("serial", "SN" + "".join(str(i % 10) for i in range(48)))
fnc1_compat = pay("fnc1_compat", "ç0112345678901231")
compat_high = pay("compat_high", "Grüße")
euro = pay("euro", "price €5")
long_text = pay("long_text", (
    "data matrix symbols carry up to fifteen hundred bytes in a square "
    "the size of a stamp, and the encoder picks the cheapest of four "
    "encodation schemes for every stretch of the text: ascii for digits "
    "in pairs, c forty for capitals, text for lower case and x twelve for "
    "the edi character set, switching with latches when that saves space."
))
long_digits = pay("long_digits", "".join(str((i * 7) % 10) for i in range(1000)))
too_long = pay("too_long", "x" * 3117)
huge = pay("huge", "abcdefghij" * 200)
exact_c40 = pay("exact_c40", "ABCDEF")
exact_unlatch = pay("exact_unlatch", "ABCABCABC")
binary = pay("binary", "".join(chr(c) for c in [0, 128, 255, 7, 200, 13, 10, 65]))
bytes_run = pay("bytes_run", "ä" * 40 + "end")
crlf = pay("crlf", "line one\r\nline two. next, then: done")
punct = pay("punct", "a!b\"c#d$e%f&g'h(i)j*k+l")
ticket = pay("ticket", "M1DOE/JANE            EABC123 OSLBGODY 0612 123Y012A0042 100")
para = pay("para", (
    "Aztec codes are read from the centre outwards, so they need no quiet "
    "zone; the bullseye finder sits in the middle, the mode message rings "
    "it, and the data spirals out in layers of dominoes. Full-range symbols "
    "add a reference grid every sixteen modules so a reader can follow the "
    "layers even when the print is warped."
))
big_az = pay("big_az", "".join(chr(65 + (i * 7) % 26) for i in range(1200)))
huge_az = pay("huge_az", "".join(str((i * 3) % 10) for i in range(3000)))

# ------------------------------------------------------------ tables

put("tables/products.csv", "\n".join([
    "sku,gtin,expiry,batch,serial",
    "ASP-100,09506000134352,261231,L4512,",
    "VIT-C,09506000134369,270630,B77,SN0001",
    "BAND-S,09506000134376,,X1,SN0002",
    "GLOVE-M,09506000134383,280101,GL-2026-10,",
    "BAD-CHK,09506000134391,261231,L1,",
    "SHORT,0950600013435,261231,L2,",
    "NO-BATCH,09506000134352,261231,,SN9",
    "TAB,09506000134352,261231,L\t3,",
    "",
]))

put("payloads/tickets.txt", "\n".join([
    "rail|OSL-BGO|2026-11-02 07:25|car 4 seat 51|NOK 899",
    "rail|BGO-OSL|2026-11-04 16:00|car 2 seat 12|NOK 899",
    "flight|M1DOE/JANE EABC123 OSLCDGAF 1075 306Y024C0037 100",
    "event|CONCERT HALL|ROW K SEAT 14|2026-12-24 19:30|ID 7730041",
    "transit|zone 1-2|valid 24h|nr 000412",
    "",
]))

# ------------------------------------------------------------ jobs

section("Data Matrix: the docstring example and the encodation modes")
job("dm %s art" % hudora)
job("dm %s" % hello)
job("dm %s qz=1 art" % one)
job("dm %s" % nul)
for p in [digits, odd_digits, upper, lower, x12, url, mixed_case, serial,
          control, punct, crlf]:
    job("dm %s" % p)

section("Data Matrix: character sets")
for p in [latin1, cafe, greek, emoji]:
    job("dm %s" % p)
job("dm %s enc=ascii" % latin1)
job("dm %s enc=iso-8859-1" % latin1)
job("dm %s enc=utf-8" % latin1)
job("dm %s enc=iso-8859-1" % greek)
job("dm %s enc=compat" % compat_high)
job("dm %s enc=compat" % euro)
job("dm %s enc=latin2" % hello)
job("dm %s" % fnc1_compat)
job("dm %s enc=auto" % fnc1_compat)
job("dm %s" % binary)

section("Data Matrix: shapes, byte mode, padding and size limits")
for p in [hello, lower, url]:
    job("dm %s shape=rectangular" % p)
    job("dm %s shape=auto" % p)
job("dm %s shape=rectangular qz=1 art" % digits)
job("dm %s shape=rectangular" % long_text)
job("dm %s shape=oval" % hello)
job("dm %s bytes" % upper)
job("dm %s bytes" % lower)
job("dm %s bytes" % latin1)
job("dm %s" % empty)
job("dm %s" % exact_c40)
job("dm %s" % exact_unlatch)
job("dm %s shape=auto" % exact_unlatch)
job("dm %s" % long_text)
job("dm %s" % long_digits)
job("dm %s" % huge)
job("dm %s" % too_long)
job("dm %s qz=0" % hudora)
job("dm %s qz=-1" % hudora)

section("Aztec: modes, shifts and byte runs")
job("az %s art" % hello)
job("az %s qz=1 art" % one)
for p in [hudora, digits, upper, lower, url, mixed_case, control, punct,
          crlf, nul, binary, bytes_run, ticket]:
    job("az %s" % p)

section("Aztec: character sets")
for p in [latin1, cafe, greek, emoji]:
    job("az %s" % p)
job("az %s enc=ascii" % latin1)
job("az %s enc=utf-8" % latin1)

section("Aztec: error correction, symbol kinds and layers")
for e in [5, 50, 95]:
    job("az %s ecc=%d" % (hello, e))
job("az %s ecc=4" % hello)
job("az %s ecc=96" % hello)
job("az %s kind=full" % hello)
job("az %s kind=full qz=0 art" % one)
job("az %s kind=compact layers=4" % hello)
job("az %s kind=full layers=6" % hello)
job("az %s kind=compact layers=1" % lower)
job("az %s layers=2" % hello)
job("az %s kind=compact layers=5" % hello)
job("az %s kind=full layers=33" % hello)
job("az %s kind=compact" % para)
job("az %s" % para)
job("az %s qz=0 art" % para)
job("az %s" % big_az)
job("az %s" % huge_az)
job("az %s" % huge)
job("az %s" % too_long)
job("az %s" % empty)

section("programs: GS1 labels, tickets, symbol sizes")
job("!labels tables/products.csv")
job("!tickets payloads/tickets.txt")
job("!capacity")

put("jobs.txt", "\n".join(JOBS) + "\n")
with open(os.path.join(D, "files.txt"), "w") as f:
    f.write("\n".join(FILES) + "\n")
print("%d files, %d jobs" % (len(FILES), sum(1 for j in JOBS if not j.startswith("#"))))
