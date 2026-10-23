#!/usr/bin/env python3
"""Writes the inputs of mini_thrift to data/: the IDL (app.thrift: the
Thrift tutorial's Calculator service plus a shop's record types), an event
log's rows, a user table for a schema migration, and the job script
data/jobs.tsv. data/files.txt lists the files written.

Run: python3 -s -P -B mk.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
written = []


def put(name, data):
    path = os.path.join(DATA, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(data, str):
        data = data.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    written.append(name)


class Lcg:
    def __init__(self, seed):
        self.s = seed

    def next(self, n):
        self.s = (self.s * 1103515245 + 12345) % 2147483648
        return (self.s >> 8) % n


IDL = r'''/*
 * The Thrift tutorial's Calculator (shared.thrift folded in), and the
 * records a shop's order service and its event log keep.
 */
namespace py app
namespace java com.example.app

typedef i32 MyInteger   // as in tutorial.thrift

const i32 INT32CONSTANT = 9853
const map<string,string> MAPCONSTANT = {'hello':'world', 'goodnight':'moon'}
const list<i16> RETRY_MS = [100, 250, 1000]

enum Operation {
  ADD = 1,
  SUBTRACT = 2,
  MULTIPLY = 3,
  DIVIDE = 4
}

enum Level { DEBUG, INFO, WARN = 5, ERROR }

struct Work {
  1: i32 num1 = 0,
  2: i32 num2,
  3: Operation op,
  4: optional string comment,
}

exception InvalidOperation {
  1: i32 whatOp,
  2: string why
}

struct SharedStruct {
  1: i32 key
  2: string value
}

struct Point {
  1: i32 x,
  2: i32 y
}

struct Item {
  1: string sku,
  2: i16 qty = 1,
  3: double price,
  4: list<string> tags,
  6: optional binary thumb
}

struct Order {
  1: i64 id,
  2: string customer,
  3: list<Item> items,
  4: map<string, i32> coupons,
  5: set<i16> flags,
  6: bool paid = false,
  7: byte priority,
  9: Point ship_to,
  12: map<MyInteger, list<string>> notes
}

# Fields listed out of id order: repr follows the IDL, the wire the ids.
struct Event {
  3: string kind,
  1: i64 ts,
  2: i32 user,
  4: double ms,
  5: map<string, string> attrs
}

struct EventV2 {
  1: i64 ts,
  2: i32 user,
  3: string kind,
  4: double ms,
  5: map<string, string> attrs,
  6: list<i32> extra = [7],
  7: bool flag = true,
  8: Level level = Level.INFO
}

struct Tree {
  1: string name,
  2: list<Tree> kids
}

struct Grid {
  1: map<Point, string> labels,
  2: map<list<i32>, i32> cells,
  3: set<double> levels,
  4: map<double, string> marks,
  5: map<bool, i32> votes,
  6: map<binary, i64> blobs,
  7: list<set<string>> groups,
  8: set<Point> spots
}

struct AllTypes {
  1: bool b,
  2: byte by,
  3: i16 s,
  4: i32 i,
  5: i64 l,
  6: double d,
  7: string str,
  8: binary bin,
  9: list<i32> li,
  10: set<string> ss,
  11: map<string, double> md,
  12: list<list<i16>> ll,
  13: list<bool> lb
}

struct UserV1 {
  1: i32 id,
  2: string name,
  3: string email
}

struct UserV2 {
  1: i32 id,
  2: string name,
  3: string email,
  4: list<string> roles = ["member"],
  5: bool active = true,
  6: double score = 0.0
}

struct Empty {}

service SharedService {
  SharedStruct getStruct(1: i32 key)
}

service Calculator extends SharedService {
   void ping(),
   i32 add(1:i32 num1, 2:i32 num2),
   i32 calculate(1:i32 logid, 2:Work w) throws (1:InvalidOperation ouch),
   oneway void zip()
}
'''

KINDS = ["view", "click", "search", "cart", "buy"]
PAGES = ["/", "/shoes", "/shoes/42", "/cart", "/search?q=boots", "/über-uns", "/checkout"]


def events():
    r = Lcg(4242)
    rows = ["ts\tkind\tuser\tms\tattrs"]
    ts = 1709546400000
    for i in range(60):
        ts += 500 + r.next(40000)
        kind = KINDS[r.next(len(KINDS))]
        user = 100 + r.next(9)
        ms = (r.next(90000) + 100) / 100.0
        attrs = []
        if r.next(3) > 0:
            attrs.append("page=" + PAGES[r.next(len(PAGES))])
        if kind == "search":
            attrs.append("q=" + ["boots", "red shoes", "café", "size 42"][r.next(4)])
        if kind == "buy":
            attrs.append("total=%d.%02d" % (10 + r.next(300), r.next(100)))
        rows.append("%d\t%s\t%d\t%s\t%s" % (ts, kind, user, repr(ms), ";".join(attrs)))
    return "\n".join(rows) + "\n"


USERS = [
    (1, "Ada Lovelace", "ada@example.com"),
    (2, "Grace Hopper", "grace@example.com"),
    (3, "Alan Turing", "alan@example.com"),
    (4, "Édith Piaf", "edith@example.fr"),
    (5, "Test Account", "qa@example.invalid"),
    (6, "Ken", "ken@example.com"),
    (7, "张伟", "zhang@example.cn"),
]


def users():
    rows = ["id\tname\temail"]
    for uid, name, email in USERS:
        rows.append("%d\t%s\t%s" % (uid, name, email))
    return "\n".join(rows) + "\n"


JOBS = []


def job(*parts):
    JOBS.append("\t".join(parts))


def be(n, w):
    return (n % (1 << (8 * w))).to_bytes(w, "big")


def bf(t, fid):
    """A binary-protocol field header."""
    return bytes([t]) + be(fid, 2)


def bs(s):
    b = s.encode("utf-8") if isinstance(s, str) else s
    return be(len(b), 4) + b


def x(*chunks):
    return "x:" + b"".join(chunks).hex()


def uv(n):
    out = bytearray()
    while True:
        if n < 0x80:
            out.append(n)
            return bytes(out)
        out.append((n & 0x7F) | 0x80)
        n >>= 7


def zz(n):
    return uv((n << 1) ^ (n >> 63))


def cs(s):
    b = s.encode("utf-8") if isinstance(s, str) else s
    return uv(len(b)) + b


STOP = b"\x00"
POINT = "Point(x=3, y=-4)"
ITEM = "Item(sku='BOOT-42', qty=2, price=89.95, tags=['leather', 'winter'])"
ORDER = ("Order(id=100234, customer='Ana Lima', items=[Item(sku='BOOT-42', qty=2, price=89.95, "
         "tags=['leather', 'winter']), Item(sku='SOCK-1', price=4.5, tags=[], thumb=b'\\x89PNG')], "
         "coupons={'WELCOME10': 10, 'FREESHIP': 0}, flags=[3, 1, 2], paid=True, priority=-2, "
         "ship_to=Point(x=12, y=7), notes={1: ['gift wrap'], -5: []})")
ALL = ("AllTypes(b=True, by=127, s=-32768, i=2147483647, l=-9223372036854775808, d=-0.0, "
       "str='naïve café ☕ \\t\"q\"\\\\', bin=b'\\x00\\xff\\x10', li=[0, -1, 1, 300], ss=['b', 'a'], "
       "md={'pi': 3.141592653589793, 'tiny': 5e-324, 'big': 1e+300}, ll=[[1, 2], [], [-3]], "
       "lb=[True, False, True])")


def jobs():
    # ---- the IDL as compiled
    for name in ("Point", "Item", "Order", "Event", "Work", "InvalidOperation", "Empty",
                 "calculate_args", "calculate_result", "ping_result", "add_result", "getStruct_args"):
        job("spec", name)
    job("const", "INT32CONSTANT")
    job("const", "MAPCONSTANT")
    job("const", "RETRY_MS")
    job("enum", "Operation")
    job("enum", "Level")
    # ---- encoding: one record, every protocol
    for proto in ("binary", "compact", "json", "sjson"):
        job("enc", proto, POINT)
        job("enc", proto, ITEM)
        job("enc", proto, ORDER)
        job("enc", proto, ALL)
        job("enc", proto, "Empty()")
        job("enc", proto, "Work()")
        job("enc", proto, "Tree(name='root', kids=[Tree(name='a', kids=[]), Tree(name='b', "
            "kids=[Tree(name='b1')])])")
    for proto in ("binary", "compact", "json"):
        job("rt", proto, ORDER)
        job("rt", proto, ALL)
        job("rt", proto, "AllTypes(d=nan)")
        job("rt", proto, "AllTypes(d=inf)")
        job("rt", proto, "AllTypes(d=-inf)")
        job("rt", proto, "AllTypes(d=0.1)")
        job("rt", proto, "AllTypes(d=1e+16, md={'x': 1.5e-07})")
    job("sizes", ORDER)
    job("sizes", ALL)
    job("rt", "binary", "Point(x=-1, y=2147483647)")
    job("rt", "compact", "Tree(name='r', kids=[Tree(name='s', kids=[Tree(name='t', kids=[])])])")
    job("rt", "json", "UserV2(id=9, name='Zoë', email='zoe@example.com')")
    binary_decoding()
    compact_decoding()
    json_decoding()
    encoding_errors()
    messages()
    dumps()
    files()
    rpc()
    programs()


def binary_decoding():
    p = bf(8, 1) + be(3, 4) + bf(8, 2) + be(-4, 4) + STOP
    d = lambda t, *c: job("dec", "binary", t, x(*c))  # noqa: E731
    d("Point", p)
    d("Point", p, b"\x01\x02")
    d("Point", p[:7])
    d("Point", b"")
    d("Point", bf(11, 9), bs("extra"), p)
    d("Point", bf(11, 1), bs("3"), bf(8, 2), be(5, 4), STOP)
    d("Point", bf(8, 0xFFFF), be(9, 4), STOP)
    d("Point", bf(8, 0xFFFE), be(9, 4), STOP)
    d("Point", bf(8, 0xFFFD), be(9, 4), STOP)
    d("Point", bf(8, 0xFFFC), be(9, 4), STOP)
    d("Point", bf(8, 0), be(9, 4), STOP)
    d("Point", bf(8, 1), be(1, 4), bf(8, 1), be(2, 4), STOP)
    d("Point", bf(5, 1), STOP)
    d("Point", bf(1, 1), STOP)
    d("Point", bf(16, 7), STOP)
    d("Point", bf(12, 7), bf(8, 1), be(1, 4), bf(2, 2), b"\x01", STOP, STOP)
    d("Point", bf(13, 7), bytes([11, 8]), be(1, 4), bs("k"), be(5, 4), STOP)
    d("Point", bf(15, 7), bytes([2]), be(3, 4), b"\x01\x00\x02", STOP)
    d("Point", bf(14, 7), bytes([4]), be(1, 4), be(0, 8), bf(8, 2), be(6, 4), STOP)
    d("UserV1", bf(8, 1), be(5, 4), bf(11, 2), bs("Édith"), bf(11, 3), bs("e@x.fr"), STOP)
    d("UserV1", bf(11, 2), be(-5, 4), STOP)
    d("UserV1", bf(11, 2), bs(b"caf\xe9"), STOP)
    d("UserV1", bf(11, 2), bs(b"\xe2\x98"), STOP)
    d("UserV1", bf(11, 2), bs(b"ok\xed\xa0\x80"), STOP)
    d("UserV1", bf(11, 2), be(1000, 4), b"abc")
    d("UserV1", bf(11, 2), bs(""), STOP)
    d("AllTypes", bf(2, 1), b"\x02", STOP)
    d("AllTypes", bf(2, 1), b"\x00", bf(3, 2), b"\xff", bf(6, 3), be(-2, 2), STOP)
    d("AllTypes", bf(15, 9), bytes([8]), be(-1, 4), STOP)
    d("AllTypes", bf(15, 9), bytes([11]), be(2, 4), be(1, 4), be(2, 4), STOP)
    d("Item", bf(15, 4), bytes([8]), be(2, 4), be(1, 4), b"A", be(1, 4), b"B", STOP)
    d("AllTypes", bf(14, 10), bytes([11]), be(3, 4), bs("b"), bs("a"), bs("b"), STOP)
    d("AllTypes", bf(14, 10), bytes([11]), be(0, 4), STOP)
    d("AllTypes", bf(13, 11), bytes([11, 4]), be(2, 4), bs("x"), be(1, 8), bs("x"), be(0x4000000000000000, 8), STOP)
    d("AllTypes", bf(15, 12), bytes([15]), be(2, 4), bytes([6]), be(1, 4), be(7, 2), bytes([6]), be(0, 4), STOP)
    d("AllTypes", bf(15, 13), bytes([2]), be(3, 4), b"\x01\x00\x07", STOP)
    d("AllTypes", bf(4, 6), be(0x7FF0000000000001, 8), STOP)
    d("AllTypes", bf(4, 6), be(0x0000000000000001, 8), STOP)
    d("AllTypes", bf(10, 5), be(-1, 8), bf(8, 4), be(-2147483648, 4), STOP)
    d("Grid", bf(13, 1), bytes([12, 11]), be(1, 4), bf(8, 1), be(1, 4), STOP, bs("a"), STOP)
    d("Grid", bf(13, 1), bytes([12, 11]), be(0, 4), STOP)
    d("Grid", bf(13, 2), bytes([15, 8]), be(1, 4), bytes([8]), be(1, 4), be(5, 4), be(9, 4), STOP)
    d("Grid", bf(14, 8), bytes([12]), be(1, 4), bf(8, 2), be(3, 4), STOP, STOP)
    d("Grid", bf(14, 3), bytes([4]), be(3, 4), be(0x8000000000000000, 8), be(0, 8),
      be(0x3FF8000000000000, 8), STOP)
    d("Grid", bf(13, 4), bytes([4, 11]), be(2, 4), be(0x7FF8000000000000, 8), bs("a"),
      be(0x7FF8000000000000, 8), bs("b"), STOP)
    d("Grid", bf(13, 5), bytes([2, 8]), be(3, 4), b"\x01", be(3, 4), b"\x00", be(2, 4), b"\x05", be(4, 4), STOP)
    d("Grid", bf(13, 6), bytes([11, 10]), be(2, 4), bs(b"\x00\x01"), be(7, 8), bs(b"zz"), be(-7, 8), STOP)
    d("Grid", bf(15, 7), bytes([14]), be(2, 4), bytes([11]), be(2, 4), bs("y"), bs("x"), bytes([11]), be(0, 4), STOP)
    d("Order", bf(13, 4), bytes([11, 8]), be(3, 4), bs("A"), be(1, 4), bs("B"), be(2, 4), bs("A"), be(3, 4), STOP)
    d("Order", bf(12, 9), bf(8, 1), be(1, 4), bf(11, 2), bs("y?"), STOP, bf(6, 2), be(3, 2), STOP)
    deep = b""
    for i in range(6):
        deep += bf(11, 1) + bs("n%d" % i) + bf(15, 2) + bytes([12]) + be(1, 4)
    deep += bf(11, 1) + bs("leaf") + STOP + (STOP * 6)
    d("Tree", deep)
    d("ping_result", STOP)
    d("ping_result", bf(8, 1), be(5, 4), STOP)
    d("Empty", bf(8, 1), be(5, 4), STOP)
    d("calculate_result", bf(8, 0), be(42, 4), STOP)
    d("calculate_result", bf(12, 1), bf(8, 1), be(4, 4), bf(11, 2), bs("no"), STOP, STOP)
    item = bf(11, 1) + bs("BOOT-42") + bf(15, 4) + bytes([11]) + be(2, 4) + bs("a") + bs("b") + STOP
    for s, c in ((4, -1), (7, -1), (-1, 1), (-1, 2), (0, 0)):
        job("lim", "binary", str(s), str(c), "Item", x(item))
    job("lim", "binary", "-1", "0", "Item", x(bf(15, 4), bytes([11]), be(0, 4), STOP))


def compact_decoding():
    d = lambda t, *c: job("dec", "compact", t, x(*c))  # noqa: E731
    p = bytes([0x15]) + zz(3) + bytes([0x15]) + zz(-4) + STOP
    d("Point", p)
    d("Point", p[:2])
    d("Point", bytes([0x05]) + zz(1) + zz(3) + bytes([0x05]) + zz(2) + zz(5) + STOP)
    d("Point", bytes([0x05]) + zz(-1) + zz(9) + STOP)
    d("Point", bytes([0x25]) + zz(8) + STOP)
    d("Point", bytes([0x15]) + uv(1 << 34) + STOP)
    d("Point", bytes([0x1D]) + STOP)
    d("Point", bytes([0x18]) + cs("3") + bytes([0x15]) + zz(5) + STOP)
    d("Point", bytes([0x1C, 0x11, 0x12, 0x15]) + zz(1) + STOP + bytes([0x15]) + zz(2) + STOP)
    d("Point", bytes([0x19, 0x31, 1, 2, 0]) + bytes([0x15]) + zz(6) + STOP)
    d("Point", bytes([0x1B, 0x02, 0x85]) + cs("k") + zz(1) + cs("j") + zz(2) + STOP)
    d("Point", bytes([0x15]) + b"\xff\xff")
    lf = lambda t, fid: bytes([t]) + zz(fid)  # noqa: E731
    d("AllTypes", bytes([0x11, 0x12]) + STOP)
    d("AllTypes", bytes([0x12]) + STOP)
    d("AllTypes", bytes([0x13, 0x80]) + STOP)
    d("AllTypes", bytes([0x11, 0x13, 0x80, 0x14]) + zz(-300) + STOP)
    d("AllTypes", lf(5, 4) + zz(-2147483648) + bytes([0x16]) + zz(-(1 << 63)) + STOP)
    d("AllTypes", lf(7, 6) + bytes.fromhex("182d4454fb210940") + STOP)
    d("AllTypes", lf(7, 6) + bytes.fromhex("182d4454fb21"))
    d("AllTypes", lf(8, 7) + cs("café") + bytes([0x18]) + cs(b"\x00\xff") + STOP)
    d("AllTypes", lf(8, 7) + cs(b"\xff") + STOP)
    d("AllTypes", lf(9, 9) + bytes([0xF5]) + uv(16) + b"".join(zz(i * i) for i in range(16)) + STOP)
    d("AllTypes", lf(9, 9) + bytes([0xD5]) + STOP)
    d("AllTypes", lf(9, 9) + bytes([0x2B]) + zz(-1) + zz(60) + STOP)
    d("AllTypes", lf(9, -5) + bytes([0x25]) + zz(1) + zz(2) + STOP)
    d("AllTypes", lf(10, 10) + bytes([0x38]) + cs("b") + cs("a") + cs("b") + STOP)
    d("AllTypes", lf(11, 11) + uv(2) + bytes([0x87]) + cs("a") + b"\x00" * 8 + cs("a")
      + bytes.fromhex("000000000000f03f") + STOP)
    d("AllTypes", lf(11, 11) + b"\x00" + STOP)
    d("AllTypes", lf(11, 11) + uv(1) + bytes([0x8D]) + cs("a") + STOP)
    d("AllTypes", lf(9, 13) + bytes([0x41, 1, 2, 0, 1]) + STOP)
    d("AllTypes", lf(9, 12) + bytes([0x29, 0x24]) + zz(1) + zz(2) + bytes([0x04]) + STOP)
    d("AllTypes", lf(9, 12) + bytes([0x29, 0x24]) + zz(1) + zz(2) + bytes([0x04]) + STOP + STOP)
    d("Order", lf(9, 3) + bytes([0x1C, 0x18]) + cs("A") + bytes([0x14]) + zz(3) + STOP
      + bytes([0x2A, 0x34]) + zz(2) + zz(1) + zz(2) + bytes([0x11]) + STOP)
    d("Order", bytes([0x59, 0x00]) + STOP)
    d("Order", bytes([0x61]) + bytes([0x33, 0xFE]) + STOP)
    d("Order", bytes([0x16]) + zz(5) + lf(11, 12) + uv(1) + bytes([0x59]) + zz(-5) + bytes([0x18]) + cs("x") + STOP)
    d("Tree", bytes([0x18]) + cs("t") + bytes([0x19, 0x1C, 0x18]) + cs("u") + STOP + STOP)
    d("Event", bytes([0x16]) + zz(1709546400123) + bytes([0x15]) + zz(101) + bytes([0x18]) + cs("view")
      + bytes([0x17]) + bytes.fromhex("0000000000405f40") + bytes([0x1B, 0x01, 0x88]) + cs("page") + cs("/") + STOP)
    item = bytes([0x18]) + cs("BOOT-42") + bytes([0x39, 0x28]) + cs("a") + cs("b") + STOP
    for s, c in ((4, -1), (-1, 1), (-1, 2)):
        job("lim", "compact", str(s), str(c), "Item", x(item))


def jt(s):
    return "t:" + s


def json_decoding():
    d = lambda t, s: job("dec", "json", t, jt(s))  # noqa: E731
    d("Point", '{"1":{"i32":3},"2":{"i32":-4}}')
    d("Point", '{"2":{"i32":-4},"1":{"i32":3}}')
    d("Point", '{"1": {"i32":3}}')
    d("Point", ' {"1":{"i32":3}}')
    d("Point", r'{\n"1":{"i32":3}}')
    d("Point", '{"1":{"i33":3}}')
    d("Point", '{"1":{"i32":"3"}}')
    d("Point", '{1:{"i32":3}}')
    d("Point", '{"1":{"i32":+3},"2":{"i32":007}}')
    d("Point", '{"1":{"i32":3.0}}')
    d("Point", '{"1":{"i32":1e3}}')
    d("Point", '{"1":{"i32":3}')
    d("Point", '{"1":{"i32":3}}tail')
    d("Point", '{"1":{"i32":99999999999}}')
    d("Point", '{"1":{"str":"x"},"2":{"i32":5}}')
    d("Point", '{"9":{"lst":["rec",1,{"1":{"tf":1}}]},"2":{"i32":5}}')
    d("Point", '{"-1":{"i32":5}}')
    d("Point", '{"1":{"i32":3}"2":{"i32":4}}')
    d("Point", '{"1":{"i32":3},"2"{"i32":4}}')
    d("Point", '')
    d("Point", '[]')
    for v in ('"2.5"', '"NaN"', '"-Infinity"', '"1_000.5"', '" 7 "', '"abc"', '1e400', '-', '"0x10"',
              '2.5e-3', '-0', '.5', '5.', '"inf"'):
        d("AllTypes", '{"6":{"dbl":%s}}' % v)
    for s in (r'a\\u00e9b', r'\\ud83d\\ude00!', r'x\\ud83d', r'\\ude00', r'\\ud83d\\u0041',
              r'\\ud83da', r'\\q', r'\\/\\b\\f\\n\\r\\t\\"\\\\', r'\\u00zz', r'\\u0x41', r'\\u+041',
              r'tab\there', 'café ☕', r'a\x80', r'\xc3', r'\xe2\x98\x95\xc3\xa9'):
        d("AllTypes", '{"7":{"str":"%s"}}' % s)
    d("AllTypes", '{"7":{"str":"open')
    d("AllTypes", '{"7":{"str":"open\\\\')
    for s in ("AP8Q", "AP8", "AP8Q====", "A", "A P8Q", "AP8Q!x", "AP8Qé", "", "AP==8Q", "_-8Q"):
        d("AllTypes", '{"8":{"str":"%s"}}' % s)
    d("AllTypes", '{"1":{"tf":2},"2":{"i8":-128},"3":{"i16":0}}')
    d("AllTypes", '{"1":{"tf":0}}')
    d("AllTypes", '{"9":{"lst":["i32",2,1,2]}}')
    d("AllTypes", '{"9":{"lst":["i32",3,1,2]}}')
    d("AllTypes", '{"9":{"lst":["i32",1,1,2]}}')
    d("AllTypes", '{"9":{"lst":["i32",-1]}}')
    d("AllTypes", '{"9":{"lst":["str",2,1,2]}}')
    d("AllTypes", '{"9":{"lst":["xyz",0]}}')
    d("AllTypes", '{"10":{"set":["str",3,"b","a","b"]}}')
    d("AllTypes", '{"11":{"map":["str","dbl",2,{"pi":3.14,"e":"2.718"}]}}')
    d("AllTypes", '{"11":{"map":["str","dbl",1,{pi:3.14}]}}')
    d("AllTypes", '{"12":{"lst":["lst",2,["i16",2,1,2],["i16",0]]}}')
    d("AllTypes", '{"13":{"lst":["tf",3,1,0,5]}}')
    d("Grid", '{"4":{"map":["dbl","str",2,{"0.5":"half","-1e3":"neg"}]}}')
    d("Grid", '{"4":{"map":["dbl","str",1,{0.5:"half"}]}}')
    d("Grid", '{"5":{"map":["tf","i32",2,{"1":10,"0":20}]}}')
    d("Grid", '{"6":{"map":["str","i64",1,{"AAE=":7}]}}')
    d("Grid", '{"3":{"set":["dbl",2,1.5,-0.25]}}')
    d("Grid", '{"1":{"map":["rec","str",1,{{"1":{"i32":1}}:"a"}]}}')
    d("Order", '{"9":{"rec":{"1":{"i32":4},"2":{"i32":5}}},"1":{"i64":7}}')
    d("Tree", '{"1":{"str":"a"},"2":{"lst":["rec",1,{"1":{"str":"b"},"2":{"lst":["rec",0]}}]}}')
    d("UserV2", '{"1":{"i32":1}}')
    job("dec", "sjson", "Point", jt('{"x":1}'))


def encoding_errors():
    cases = [
        "Point(x=2147483648)", "Point(x=-2147483649)", "Point(x='3')", "Point(x=1.5)", "Point(x=1e10)",
        "Point(x=True, y=False)", "Point(x=None, y=None)", "Point(x=[1])",
        "AllTypes(by=200)", "AllTypes(by=-129)", "AllTypes(by='a')", "AllTypes(s=40000)", "AllTypes(s=2.0)",
        "AllTypes(l=9223372036854775807)",
        "AllTypes(str=b'abc')", "AllTypes(str=b'')", "AllTypes(str=5)", "AllTypes(str=['ab', 'c'])",
        "AllTypes(str=['a', 1])", "AllTypes(str=1.5)", "AllTypes(str=True)",
        "AllTypes(bin='abc')", "AllTypes(bin=5)", "AllTypes(bin=b'')", "AllTypes(bin=[1, 2])",
        "AllTypes(b='yes')", "AllTypes(b=1)", "AllTypes(b=0)", "AllTypes(b='')", "AllTypes(b=[])",
        "AllTypes(d=3)", "AllTypes(d='x')", "AllTypes(d=True)", "AllTypes(d=[1, 2])", "AllTypes(d=b'1')",
        "AllTypes(li='abc')", "AllTypes(li=5)", "AllTypes(li={1: 2, 3: 4})", "AllTypes(li=[1, None])",
        "AllTypes(li=[1, 2.5])", "AllTypes(ss='ab')", "AllTypes(ss=['b', 'b', 'a'])", "AllTypes(md=[1])",
        "AllTypes(md=5)", "AllTypes(md={'a': None})", "AllTypes(md={1: 2.0})", "AllTypes(ll=[[1, 'x']])",
        "AllTypes(ll=[5])", "AllTypes(lb=[1, 0, 'x', None, True])",
        "Order(ship_to=5)", "Order(ship_to=Item(sku='x'))", "Order(items=[None])", "Order(items=[Point(x=1)])",
        "Order(ship_to={'x': 1})", "Order(notes={1: 'ab'})", "Grid(marks={0.5: 'half', -0.0: 'z'})",
        "Grid(votes={True: 1, False: 0})", "Grid(blobs={b'\\x00': 1})", "Grid(levels=[1.5, 1.5])",
        "5", "'text'", "Work(op=Operation.DIVIDE, comment='')",
    ]
    for c in cases:
        for proto in ("binary", "compact", "json"):
            job("enc", proto, c)
    for c in ("AllTypes(d='x')", "AllTypes(d='é')", "AllTypes(d=[1, 2])", "AllTypes(d=b'ab')",
              "AllTypes(d=True)", "AllTypes(d=nan)", "AllTypes(i=True, b=1)", "AllTypes(str=b'')",
              "Grid(marks={0.5: 'h'}, votes={True: 1})", "Grid(blobs={b'\\xff': 2})"):
        job("enc", "sjson", c)


def messages():
    for proto in ("binary", "binary-loose", "compact", "json", "sjson"):
        job("msgw", proto, "add", "1", "7")
        job("msgw", proto, "getStruct", "2", "-1")
        job("msgw", proto, "zip", "4", "2147483647")
    job("msgw", "compact", "big", "8", "1")
    job("msgw", "compact", "neg", "1", "-2147483648")
    job("msgw", "binary", "ünï", "3", "0")
    job("msgw", "json", "q\"uote", "1", "0")
    m = lambda proto, *c: job("msgr", proto, x(*c))  # noqa: E731
    m("binary", be(0x80010001, 4), bs("add"), be(7, 4))
    m("binary", be(0x800100FF, 4), bs("add"), be(-7, 4))
    m("binary", be(0x80020001, 4), bs("add"), be(7, 4))
    m("binary", be(3, 4), b"add", b"\x01", be(7, 4))
    m("binary-strict", be(3, 4), b"add", b"\x01", be(7, 4))
    m("binary", be(3, 4), b"ad")
    m("binary", be(0x80010001, 4), bs(b"\xff"), be(7, 4))
    m("compact", bytes([0x82, 0x21]) + uv(7) + cs("add"))
    m("compact", bytes([0x82, 0x21]) + uv(0xFFFFFFFF) + cs("add"))
    m("compact", bytes([0x82, 0x21]) + uv(0x80000000) + cs("add"))
    m("compact", bytes([0x80, 0x21]) + uv(7) + cs("add"))
    m("compact", bytes([0x82, 0x22]) + uv(7) + cs("add"))
    m("compact", bytes([0x82, 0xE1]) + uv(7) + cs("x"))
    job("msgr", "json", jt('[1,"add",1,7,{}]'))
    job("msgr", "json", jt('[2,"add",1,7,{}]'))
    job("msgr", "json", jt('[1,"add","1",7]'))
    job("msgr", "json", jt('[1,add,1,7]'))
    job("msgr", "sjson", jt('[1,"add",1,7]'))


ORDER_DUMP = ORDER.replace("flags=[3, 1, 2], ", "")


def dumps():
    job("rt", "compact", ORDER_DUMP)
    o_bin = ("0a0001000000000001878a0b000200000003416e610f00030c000000010b000100000001580600020002"
             "00040006400000000000000000000d00040b080000000100000001410000000100")
    job("dump", "binary", "x:" + o_bin, "struct")
    job("dump", "binary", "x:" + o_bin[:-6], "struct")
    job("dump", "compact", x(bytes([0x16]) + zz(5) + bytes([0x18]) + cs(b"\xffraw") + bytes([0x1A, 0x34])
                             + zz(1) + zz(2) + zz(-3) + bytes([0x11, 0x2C, 0x15]) + zz(7) + STOP + STOP),
        "struct")
    job("dump", "json", jt('{"1":{"i64":5},"3":{"lst":["rec",1,{"1":{"str":"X"},"3":{"dbl":2}}]},'
                           '"4":{"map":["str","i32",1,{"A":1}]},"6":{"tf":1}}'), "struct")
    job("dump", "binary", x(be(0x80010001, 4), bs("add"), be(0, 4), bf(8, 1), be(1, 4), bf(8, 2), be(2, 4), STOP),
        "message")
    job("dump", "compact", x(bytes([0x82, 0x41]) + uv(0) + cs("calculate") + bytes([0x0C]) + zz(1)
                             + bytes([0x25]) + zz(7) + STOP + STOP), "message")
    job("dump", "json", jt('[1,"add",1,0,{"1":{"i32":1},"2":{"i32":2}}]'), "message")
    job("dump", "binary", x(bf(5, 1), STOP), "struct")
    job("dump", "binary", x(bf(8, 1), be(1, 4), STOP, b"junk"), "struct")
    job("skip", "binary", "12", x(bf(8, 1), be(1, 4), STOP, b"\x99"))
    job("skip", "binary", "15", x(bytes([11]), be(2, 4), bs("a"), bs("bc")))
    job("skip", "compact", "13", x(uv(2) + bytes([0x55]) + zz(1) + zz(2) + zz(3) + zz(4)))
    job("skip", "compact", "12", x(bytes([0x11, 0x12, 0x15]) + zz(9) + STOP))
    job("skip", "json", "12", jt('{"1":{"i32":1}}'))
    job("skip", "json", "15", jt('["str",2,"a","b"],"rest"'))
    job("skip", "binary", "99", x(b"\x00"))
    job("skip", "binary", "2", x(b""))


def files():
    job("frames", "binary", "data/out/points.bin", "Point(x=1, y=2)", "Point(x=-3)", "Point()")
    job("file", "data/out/points.bin")
    job("readframes", "binary", "data/out/points.bin", "Point")
    job("frames", "compact", "data/out/points.c", "Point(x=1, y=2)", "Point(x=-3)", "Point()")
    job("file", "data/out/points.c")
    job("readframes", "compact", "data/out/points.c", "Point")
    job("patch", "data/out/points.c", "3", "09")
    job("readframes", "compact", "data/out/points.c", "Point")
    job("patch", "data/out/points.bin", "0", "80")
    job("readframes", "binary", "data/out/points.bin", "Point")
    job("frames", "json", "data/out/points.j", "Point(x=1, y=2)", "Tree(name='x')")
    job("file", "data/out/points.j")
    job("readframes", "json", "data/out/points.j", "Point")
    job("readframes", "json", "data/out/points.j", "Tree")
    job("truncate", "data/out/points.j", "20")
    job("readframes", "json", "data/out/points.j", "Point")
    job("frames", "binary", "data/out/bad.bin", "Point(x='1')")
    job("file", "data/out/bad.bin")
    job("readframes", "binary", "data/out/nothing.bin", "Point")


def rpc():
    work = lambda a, b, op: "Work(num1=%d, num2=%d, op=Operation.%s)" % (a, b, op)  # noqa: E731
    for proto, kind in (("binary", "framed"), ("compact", "framed"), ("json", "buffered"),
                        ("binary", "buffered"), ("compact", "plain")):
        job("call", proto, kind, "-", "ping")
        job("call", proto, kind, "-", "add", "1", "2")
    job("call", "binary", "framed", "-", "add", "2147483647", "1")
    job("call", "compact", "framed", "-", "add", "2147483647", "1")
    job("call", "json", "framed", "-", "add", "-2147483648", "-1")
    job("call", "binary", "framed", "-", "add", "'1'", "2")
    job("call", "binary", "framed", "-", "calculate", "1", work(1, 0, "DIVIDE"))
    job("call", "compact", "framed", "-", "calculate", "2", work(7, 2, "DIVIDE"))
    job("call", "binary", "framed", "-", "calculate", "2", work(7, 2, "DIVIDE"))
    job("call", "json", "buffered", "-", "calculate", "2", work(7, 2, "DIVIDE"))
    job("call", "json", "buffered", "-", "calculate", "8", work(8, 2, "DIVIDE"))
    job("call", "binary", "framed", "-", "calculate", "3", work(6, 7, "MULTIPLY"))
    job("call", "compact", "framed", "-", "calculate", "4", "Work(num1=1, num2=2, op=9)")
    job("call", "binary", "framed", "-", "calculate", "5", "Work(num2=5, op=Operation.SUBTRACT)")
    job("call", "binary", "framed", "-", "calculate", "6", "Work(num1=1, op=Operation.ADD)")
    job("call", "binary", "framed", "-", "calculate", "7", "None")
    job("call", "json", "framed", "-", "getStruct", "3")
    job("call", "compact", "buffered", "-", "getStruct", "8")
    job("call", "binary", "framed", "-", "getStruct", "99")
    job("call", "binary", "framed", "-", "getStruct", "2")
    job("call", "binary", "framed", "-", "zip")
    job("call", "json", "plain", "-", "zip")
    job("call", "binary", "framed", "Calculator", "add", "3", "4")
    job("call", "compact", "framed", "Calculator", "ping")
    job("call", "json", "buffered", "Calculator", "calculate", "9", work(9, 3, "SUBTRACT"))
    job("call", "binary", "framed", "Calculator", "getStruct", "9")
    job("call", "binary", "framed", "Calculator", "zip")
    job("call", "binary", "framed", "Shop", "add", "1", "1")
    fr = lambda *c: be(len(b"".join(c)), 4) + b"".join(c)  # noqa: E731
    msg = lambda name, t=1: be(0x80010000 | t, 4) + bs(name) + be(5, 4)  # noqa: E731
    args = bf(8, 1) + be(2, 4) + bf(8, 2) + be(3, 4) + STOP
    r = lambda mode, *c, kind="framed", proto="binary": job("raw", proto, kind, mode, x(*c))  # noqa: E731
    r("plain", fr(msg("nosuch"), args))
    r("plain", fr(msg("add"), args))
    r("plain", fr(msg("add", 2), args))
    r("plain", fr(msg("add"), bf(5, 1), STOP))
    r("plain", fr(msg("add"), bf(8, 1), be(2, 4), bf(11, 2), bs("3"), STOP))
    r("plain", fr(msg("add")))
    r("plain", b"")
    r("plain", be(100, 4), msg("add"))
    r("plain", be(-4, 4), msg("add"))
    r("mux", fr(msg("add"), args))
    r("mux", fr(msg("Shop:add"), args))
    r("mux", fr(msg("Calculator:add", 2), args))
    r("mux", fr(msg("Calculator:nosuch"), args))
    r("mux", fr(msg("Calculator:"), args))
    r("mux", fr(msg(":add"), args))
    r("mux", fr(msg("Calculator:add:x"), args))
    r("plain", be(3, 4), b"add", b"\x01", be(5, 4), args, kind="buffered")
    r("plain", msg("add"), args, kind="plain")
    r("plain", bytes([0x80, 0x21]) + uv(1) + cs("add") + STOP, kind="plain", proto="compact")
    r("plain", bytes([0x82, 0x21]) + uv(1) + cs("add") + bytes([0x15]) + zz(20) + bytes([0x15]) + zz(22) + STOP,
      kind="plain", proto="compact")
    job("raw", "json", "buffered", "plain", jt('[1,"add",1,0,{"1":{"i32":2},"2":{"i32":3}}]'))
    job("raw", "json", "buffered", "plain", jt('[2,"add",1,0,{}]'))
    job("raw", "json", "buffered", "plain", jt('[1,"add",1,0,{"1":{"i32":2},"2":{"i32":3}}'))
    job("raw", "json", "buffered", "mux", jt('[1,"Calculator:add",4,0,{"1":{"i32":2},"2":{"i32":3}}]'))


def programs():
    job("eventlog", "write", "compact", "data/out/events.bin")
    job("file", "data/out/events.bin")
    job("eventlog", "read", "compact", "data/out/events.bin", "Event")
    job("eventlog", "read", "compact", "data/out/events.bin", "EventV2")
    job("eventlog", "write", "binary", "data/out/events_b.bin")
    job("eventlog", "read", "binary", "data/out/events_b.bin", "Event")
    job("eventlog", "write", "json", "data/out/events.json")
    job("eventlog", "read", "json", "data/out/events.json", "Event")
    job("truncate", "data/out/events.bin", "500")
    job("eventlog", "read", "compact", "data/out/events.bin", "Event")
    job("patch", "data/out/events_b.bin", "4", "05")
    job("eventlog", "read", "binary", "data/out/events_b.bin", "Event")
    job("legacy", "binary", "data/out/users_v1.bin")
    job("file", "data/out/users_v1.bin")
    job("readframes", "binary", "data/out/users_v1.bin", "UserV1")
    job("migrate", "binary", "data/out/users_v1.bin", "compact", "data/out/users_v2.bin")
    job("readframes", "compact", "data/out/users_v2.bin", "UserV2")
    job("readframes", "compact", "data/out/users_v2.bin", "UserV1")
    job("export", "compact", "data/out/users_v2.bin", "UserV2", "data/out/users.jsonl")
    job("file", "data/out/users.jsonl")
    job("migrate", "compact", "data/out/users_v2.bin", "json", "data/out/users_v3.json")
    job("export", "json", "data/out/users_v3.json", "UserV2", "data/out/users3.jsonl")


def main():
    put("app.thrift", IDL)
    put("events.tsv", events())
    put("users.tsv", users())
    put("admins.txt", "ada@example.com\nken@example.com\n")
    jobs()
    put("jobs.tsv", "\n".join(JOBS) + "\n")
    with open(os.path.join(DATA, "files.txt"), "w") as f:
        f.write("\n".join(written) + "\n")


main()
