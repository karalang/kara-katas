"""Writes data/: the jobs (data/jobs.txt) and, for each scripted session,
the bytes a PostgreSQL server sends back (data/<session>.bin). The server
side is built here message by message, in the order pg8000 reads it, with
the SCRAM replies computed for the client nonces pgstub.py hands out.

Jobs, one a line (a session runs from its `session` line to `end`):
  stmt <names|-> <sql>          native.to_statement, then make_vals(names)
  style <style> <names|-> <sql> dbapi.convert_paramstyle
  ident <value>                 converters.identifier
  literal <value>               converters.literal
  out <value>                   converters.make_param(PY_TYPES, value)
  in <oid> <text>               the input converter pg8000 uses for oid
Values are Python literals plus a few constructors (see oracle.py).

Run: python3 -s -P -B mk.py"""
import base64
import hashlib
import hmac
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

NONCES = ['%032x' % (0x5f3a91c2d8e64b07a1c39e2f4d6b8a10 + 7919 * k) for k in range(64)]
nonce_at = [0]


def msg(code, payload=b""):
    return code + struct.pack("!i", len(payload) + 4) + payload


def cstr(s):
    return s.encode("utf-8") + b"\x00"


def auth(code, extra=b""):
    return msg(b"R", struct.pack("!i", code) + extra)


def pstatus(k, v, enc="utf-8"):
    return msg(b"S", k.encode("ascii") + b"\x00" + v.encode(enc) + b"\x00")


def key(pid, secret):
    return msg(b"K", struct.pack("!ii", pid, secret))


def ready(st=b"I"):
    return msg(b"Z", st)


def rowdesc(cols):
    out = struct.pack("!H", len(cols))
    for name, oid in cols:
        size = {16: 1, 20: 8, 21: 2, 23: 4, 26: 4, 700: 4, 701: 8, 1082: 4, 1083: 8, 1114: 8, 1184: 8,
                1186: 16, 2950: 16}.get(oid, -1)
        out += cstr(name) + struct.pack("!ihihih", 16384 if oid != 705 else 0, len(out) % 7, oid, size, -1, 0)
    return msg(b"T", out)


def datarow(vals, enc="utf-8"):
    out = struct.pack("!H", len(vals))
    for v in vals:
        if v is None:
            out += struct.pack("!i", -1)
        else:
            b = v if isinstance(v, bytes) else v.encode(enc)
            out += struct.pack("!i", len(b)) + b
    return msg(b"D", out)


def complete(tag):
    return msg(b"C", cstr(tag))


def fields(code, pairs, enc="utf-8"):
    out = b""
    for k, v in pairs:
        out += k.encode("ascii") + v.encode(enc) + b"\x00"
    return msg(code, out + b"\x00")


def error(sqlstate, text, extra=()):
    return fields(b"E", [("S", "ERROR"), ("V", "ERROR"), ("C", sqlstate), ("M", text)] + list(extra))


def fatal(sqlstate, text, extra=()):
    return fields(b"E", [("S", "FATAL"), ("V", "FATAL"), ("C", sqlstate), ("M", text)] + list(extra))


def notice(text, sev="NOTICE", code="00000"):
    return fields(b"N", [("S", sev), ("V", sev), ("C", code), ("M", text)])


def notify(pid, chan, payload):
    return msg(b"A", struct.pack("!i", pid) + cstr(chan) + cstr(payload))


PARSE_OK = msg(b"1")
BIND_OK = msg(b"2")
CLOSE_OK = msg(b"3")
NO_DATA = msg(b"n")
EMPTY = msg(b"I")


def pdesc(oids):
    return msg(b"t", struct.pack("!H", len(oids)) + b"".join(struct.pack("!i", o) for o in oids))


def copy_out(binary, ncols):
    return msg(b"H", struct.pack("!bh", binary, ncols) + struct.pack("!h", binary) * ncols)


def copy_in(binary, ncols):
    return msg(b"G", struct.pack("!bh", binary, ncols) + struct.pack("!h", binary) * ncols)


def copy_data(b):
    return msg(b"d", b)


COPY_DONE = msg(b"c")


def hello(params=(("server_version", "16.4"), ("client_encoding", "UTF8"), ("DateStyle", "ISO, MDY"),
                  ("integer_datetimes", "on"), ("TimeZone", "UTC")), pid=4242, secret=0x2b1d0f3c):
    out = auth(0)
    for k, v in params:
        out += pstatus(k, v)
    return out + key(pid, secret) + ready()


def simple(cols, rows, tag, st=b"I"):
    """The replies to a simple Query: a result set, then ReadyForQuery."""
    out = rowdesc(cols) if cols is not None else b""
    for r in rows:
        out += datarow(r)
    return out + complete(tag) + ready(st)


def extended(cols, rows, tag, nparams=0, st=b"I", pre=b""):
    """The replies to execute_unnamed: Parse+Sync, Describe+Sync, then
    Bind+Execute+Sync."""
    out = PARSE_OK + ready(st)
    out += pdesc([0] * nparams) + (rowdesc(cols) if cols is not None else NO_DATA) + ready(st)
    out += BIND_OK + pre
    for r in rows:
        out += datarow(r)
    return out + complete(tag) + ready(st)


# ---- SCRAM, server side (RFC 5802 / 7677), for the nonces pgstub hands out

def scram_hf(name):
    return hashlib.sha1 if name == "SCRAM-SHA-1" else hashlib.sha256


def scram_exchange(user, password, mech="SCRAM-SHA-256", iterations=128, salt=b"pg8000-salt-0001",
                   s_nonce="3rfcNHYJY1ZVvWVs7j", tamper=None):
    """AuthenticationSASLContinue and AuthenticationSASLFinal for the next
    client nonce. tamper picks a broken server: 'nonce' (a nonce that does
    not extend the client's), 'sig' (a wrong server signature), 'attrs'
    (server-first without the salt), 'final-e' (server-final with e=)."""
    c_nonce = NONCES[nonce_at[0]]
    nonce_at[0] += 1
    hf = scram_hf(mech)
    nonce = c_nonce + s_nonce
    if tamper == "nonce":
        nonce = "x" + nonce
    first_bare = f"n={user},r={c_nonce}"
    server_first = f"r={nonce},s={base64.b64encode(salt).decode()},i={iterations}"
    if tamper == "attrs":
        server_first = f"r={nonce},i={iterations}"
    salted = hashlib.pbkdf2_hmac(hf().name, password.encode(), salt, iterations)
    server_key = hmac.new(salted, b"Server Key", hf).digest()
    final_wo_proof = f"c={base64.b64encode(b'n,,').decode()},r={nonce}"
    auth_msg = ",".join((first_bare, server_first, final_wo_proof)).encode()
    sig = base64.b64encode(hmac.new(server_key, auth_msg, hf).digest()).decode()
    if tamper == "sig":
        sig = base64.b64encode(b"\x00" * len(base64.b64decode(sig))).decode()
    final = f"v={sig}"
    if tamper == "final-e":
        final = "e=invalid-proof"
    return auth(11, server_first.encode()), auth(12, final.encode())


def sasl_start(mechs):
    return auth(10, b"".join(m.encode() + b"\x00" for m in mechs) + b"\x00")


# ---- the sessions

SESSIONS = []


def session(name, opts, server, ops):
    SESSIONS.append((name, opts, server, ops))


def build_sessions():
    T_ID = [("id", 23)]

    # Trust auth, a simple query, the startup parameters.
    session("s01", "user='alice' database='shop' application_name='inventory' ssl=False",
            hello() + simple(T_ID + [("name", 25)], [["1", "widget"], ["2", None]], "SELECT 2")
            + simple(None, [], "CREATE TABLE"),
            ["run 'SELECT id, name FROM items'", "run 'CREATE TABLE t (x int)'", "show", "close"])

    # Cleartext and MD5 passwords.
    session("s02", "user='bob' password='hunter2' ssl=False",
            auth(3) + hello(params=(("server_version", "15.8"),)) + simple(T_ID, [["7"]], "SELECT 1"),
            ["run 'SELECT 7'", "close"])
    session("s03", "user='carol' password='s3cr3t' database='crm' ssl=False",
            auth(5, b"\x9a\x01\xfe\x33") + hello(pid=777, secret=-5), ["show", "close"])
    session("s04", "user='dave' ssl=False", auth(5, b"salt"), [])
    session("s05", "user='erin' ssl=False", auth(3), [])

    # SCRAM-SHA-256: the full exchange, then parameterised queries.
    sc, sf = scram_exchange("frank", "correct horse battery staple")
    session("s06", "user='frank' password='correct horse battery staple' ssl=False",
            sasl_start(["SCRAM-SHA-256"]) + sc + sf + hello()
            + extended([("total", 1700)], [["1234.50"]], "SELECT 1", nparams=2)
            + extended(None, [], "INSERT 0 1", nparams=4),
            ["run 'SELECT sum(price) FROM orders WHERE customer = :c AND placed > :since' "
             "c='frank' since=date(2024, 1, 1)",
             "run 'INSERT INTO log VALUES (:at, :who, :what, :n)' at=datetime(2024, 3, 9, 14, 30, 5, 120) "
             "who=None what=b'\\x00\\xffok' n=12",
             "close"])
    # SCRAM with both mechanisms offered (no TLS, so -PLUS is skipped).
    sc, sf = scram_exchange("grace", "pa55word", iterations=96, salt=b"\x01\x02\x03\x04salt")
    session("s07", "user='grace' password='pa55word' ssl=False",
            sasl_start(["SCRAM-SHA-256-PLUS", "SCRAM-SHA-256"]) + sc + sf + hello(), ["close"])
    # SCRAM-SHA-1 only.
    sc, sf = scram_exchange("heidi", "letmein", mech="SCRAM-SHA-1", iterations=64)
    session("s08", "user='heidi' password='letmein' ssl=False",
            sasl_start(["SCRAM-SHA-1"]) + sc + sf + hello(), ["close"])
    # SCRAM failures.
    session("s09", "user='ivan' password='x' ssl=False", sasl_start(["SCRAM-SHA-256-PLUS"]), [])
    sc, sf = scram_exchange("judy", "pw", tamper="sig")
    session("s10", "user='judy' password='pw' ssl=False", sasl_start(["SCRAM-SHA-256"]) + sc + sf, [])
    sc, sf = scram_exchange("ken", "pw", tamper="nonce")
    session("s11", "user='ken' password='pw' ssl=False", sasl_start(["SCRAM-SHA-256"]) + sc + sf, [])
    sc, sf = scram_exchange("lena", "pw", tamper="attrs")
    session("s12", "user='lena' password='pw' ssl=False", sasl_start(["SCRAM-SHA-256"]) + sc + sf, [])
    sc, sf = scram_exchange("mallory", "pw", tamper="final-e")
    session("s13", "user='mallory' password='pw' ssl=False", sasl_start(["SCRAM-SHA-256"]) + sc + sf, [])
    sc, sf = scram_exchange("nina", "tab\there")
    session("s14", "user='nina' password='tab\\there' ssl=False", sasl_start(["SCRAM-SHA-256"]) + sc, [])

    # The server refuses the login, or asks for what pg8000 cannot do.
    session("s15", "user='oscar' password='nope' ssl=False",
            auth(5, b"\x00\x01\x02\x03") + fatal("28P01", 'password authentication failed for user "oscar"',
                                                 [("F", "auth.c"), ("L", "323"), ("R", "auth_failed")]), [])
    session("s16", "user='peggy' ssl=False", auth(7), [])
    session("s17", "user='quinn' ssl=False", auth(99), [])
    session("s18", "user=None ssl=False", b"", [])
    session("s19", "user='rita' database=5 ssl=False", b"", [])

    # TLS negotiation over a server that answers N.
    session("s20", "user='sam' ssl=None", b"N" + hello(), ["close"])
    session("s21", "user='trent' ssl=True", b"N", [])

    # Every input converter on one result set.
    cols = [("i2", 21), ("i4", 23), ("i8", 20), ("oid", 26), ("f4", 700), ("f8", 701), ("num", 1700),
            ("ok", 16), ("txt", 25), ("vc", 1043), ("bin", 17), ("day", 1082), ("at", 1083),
            ("ts", 1114), ("tstz", 1184), ("span", 1186), ("doc", 3802), ("id", 2950), ("addr", 869),
            ("net", 650), ("tags", 1009), ("nums", 1007), ("r", 3904), ("pt", 600), ("rec", 2249),
            ("mac", 829), ("cash", 790), ("other", 3615)]
    row1 = ["-32768", "2147483647", "9223372036854775807", "4294967295", "1.5", "-1.25e-08", "12345.6789",
            "t", "plain", "café", "\\xdeadbeef", "2024-02-29", "23:59:59.999999", "2024-02-29 12:00:00",
            "2024-02-29 12:00:00+00", "1 day 02:03:04", '{"a": [1, 2.5, null], "b": "x\\"y"}',
            "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "192.168.10.7", "10.0.0.0/8", '{a,"b c",NULL,"d\\"e"}',
            "{{1,2},{3,4}}", "[1,10)", "(1.5,-2)", '(42,"x y",)', "08:00:2b:01:02:03", "$1,234.50",
            "'fat' & 'rat'"]
    row2 = [None] * len(cols)
    row3 = ["0", "-1", "-9223372036854775808", "0", "NaN", "Infinity", "NaN", "f", "", "",
            "\\x", "infinity", "00:00:00", "infinity", "-infinity", "00:00:00", "[]",
            "00000000-0000-0000-0000-000000000000", "::1", "2001:db8::/32", "{}", "{}", "empty", "(0,0)",
            "()", "ff:ff:ff:ff:ff:ff", "-$0.01", "'a'"]
    session("s22", "user='uma' ssl=False",
            hello() + simple(cols, [row1, row2, row3], "SELECT 3"),
            ["run 'SELECT * FROM every_type'", "close"])

    # Text encodings set by the server.
    s = hello(params=(("client_encoding", "LATIN1"),))
    s += extended([("name", 25)], [["Jos\xe9 M\xfcller".encode("latin-1")]], "SELECT 1", nparams=1)
    s += pstatus("client_encoding", "WIN1252") + simple([("q", 25)], [[b"\x93quoted\x94 \x80"]], "SELECT 1")
    session("s23", "user='victor' ssl=False", s,
            ["run 'SELECT name FROM people WHERE name = :n' n='Jos\\xe9'", "run 'SELECT q'", "show", "close"])

    # Errors, a failed transaction, notices and notifications.
    s = hello()
    s += error("42P01", 'relation "nope" does not exist', [("P", "15"), ("F", "parse_relation.c"), ("L", "1392"),
                                                           ("R", "parserOpenTable")]) + ready()
    s += simple(None, [], "BEGIN", st=b"T")
    s += error("22012", "division by zero") + ready(b"E")
    s += complete("SELECT 1") + ready(b"E")
    s += complete("ROLLBACK") + ready()
    s += notice("table \"t\" does not exist, skipping") + complete("DROP TABLE") + ready()
    s += notify(9001, "orders", "id=17") + notify(9001, "orders", "") + simple(T_ID, [["1"]], "SELECT 1")
    s += pstatus("application_name", "nightly") + EMPTY + ready()
    s += simple(None, [], "INSERT 0 3")[:-6] + complete("UPDATE 2") + ready()
    session("s24", "user='walter' ssl=False", s,
            ["run 'SELECT * FROM nope'", "run 'BEGIN'", "run 'SELECT 1/0'", "run 'SELECT 1'", "run 'ROLLBACK'",
             "run 'DROP TABLE IF EXISTS t'", "run 'SELECT 1'", "run ''",
             "run 'INSERT INTO t VALUES (1),(2),(3); UPDATE t SET x = x + 1 WHERE x < 3'", "show", "close"])

    # Prepared statements.
    s = hello()
    s += PARSE_OK + pdesc([23]) + rowdesc([("sku", 25), ("qty", 23)]) + ready()
    s += BIND_OK + datarow(["A-1", "4"]) + complete("SELECT 1") + ready()
    s += BIND_OK + complete("SELECT 0") + ready()
    s += PARSE_OK + pdesc([]) + NO_DATA + ready()
    s += CLOSE_OK + ready()
    s += PARSE_OK + pdesc([25, 1184]) + NO_DATA + ready()
    s += BIND_OK + complete("UPDATE 1") + ready()
    session("s25", "user='xena' ssl=False", s,
            ["prepare p 'SELECT sku, qty FROM stock WHERE qty > :q'", "exec p q=3", "exec p q=100",
             "prepare v 'VACUUM'", "closestmt p", "prepare u 'UPDATE stock SET seen = :at WHERE sku = :s'",
             "exec u s='A-1' at=datetime(2024, 5, 1, 8, 0, 0, 0, tz=-25200)", "exec u s='A-2'", "close"])

    # COPY out and in.
    s = hello()
    s += extended(None, [], "COPY 2", pre=copy_out(0, 2) + copy_data(b"1\tapple\n") + copy_data(b"2\tbanana\n") + COPY_DONE)
    s += extended(None, [], "COPY 1", pre=copy_out(0, 1) + copy_data("caf\xe9\n".encode()) + COPY_DONE)
    s += extended(None, [], "COPY 2", pre=copy_in(0, 2))
    s += extended(None, [], "COPY 3", pre=copy_in(0, 1))
    s += extended(None, [], "COPY 0")[:-(6 + 12)] + copy_in(1, 1)
    session("s26", "user='yuri' ssl=False", s,
            ["run 'COPY fruit TO STDOUT' stream=out_bytes()", "run 'COPY cafe TO STDOUT' stream=out_text()",
             "run 'COPY fruit FROM STDIN' stream=in_lines(['3\\tcherry\\n', b'4\\tdate\\n'])",
             "run 'COPY notes FROM STDIN' stream=in_bytes(b'a\\nb\\nc\\n')",
             "run 'COPY blob FROM STDIN (FORMAT binary)' stream=in_lines(['x'])", "close"])
    s = hello() + copy_out(0, 1) + copy_data(b"x\n")
    session("s27", "user='zed' ssl=False", s, ["run 'COPY t TO STDOUT'", "close"])

    # The extended protocol with every parameter type, the types= argument,
    # and placeholder errors.
    s = hello() + extended(None, [], "INSERT 0 1", nparams=14) + extended(None, [], "INSERT 0 1", nparams=2)
    s += extended([("n", 23)], [["2"]], "SELECT 1", nparams=1)
    session("s28", "user='amy' ssl=False", s,
            ["run 'INSERT INTO t VALUES (:a, :b, :c, :d, :e, :f, :g, :h, :i, :j, :k, :l, :m, :n)' "
             "a=True b=-7 c=2.5 d=Decimal('-0.50') e=\"it's\" f=time(9, 15) g=timedelta(2, 30, 5) "
             "h=UUID('12345678-1234-5678-1234-567812345678') i=IPv4Network('10.1.0.0/16') "
             "j=[1, None, [2, 3]] k=['a b', 'c\"d', '', 'NULL'] l={'k': [1, 2], 'z': None} m=(1, 'x y', None) "
             "n=Range(1, 10, '[]')",
             "run 'INSERT INTO t VALUES (:a, :b)' a=PGInterval(months=2, days=3) b=datetime(2024, 1, 1, 0, 30, 0, 0, tz=3600) "
             "types={'a': 1186, 'b': 1184}",
             "run 'SELECT :x::int + :x' x=1",
             "run 'SELECT :types' types=1 a=2", "run 'SELECT :missing' other=1", "close"])

    # Desynchronised and broken streams.
    session("s29", "user='bea' ssl=False", hello() + msg(b"W", b"\x00\x00\x00"), ["run 'SELECT 1'", "close"])
    session("s30", "user='cal' ssl=False", hello() + rowdesc(T_ID)[:9], ["run 'SELECT 1'", "close"])
    session("s31", "user='dina' ssl=False", hello() + simple(T_ID, [["1"]], "SELECT 1"),
            ["close", "run 'SELECT 1'", "close"])


# ---- pure-function jobs

STMT = [
    ("a,b", "SELECT * FROM t WHERE a = :a AND b = :b"),
    ("a", "SELECT :a, :a, :a"),
    ("a,b", "SELECT :b, :a, :b"),
    ("x", "SELECT x::text, :x"),
    ("v", "UPDATE t SET v := :v"),
    ("-", "SELECT ':notaparam', \"col:name\""),
    ("q", "SELECT E'it\\'s :q', :q"),
    ("q", "SELECT 'it''s :q', :q"),
    ("z", "SELECT $$ :z $$, :z"),
    ("y", "SELECT 1 -- :y is a comment\n, :y"),
    ("a_1,B2", "SELECT :a_1+:B2"),
    ("a", "SELECT :a"),
    ("a", "SELECT :a)"),
    ("-", "SELECT :types"),
    ("-", "SELECT :stream"),
    ("a", "SELECT :a, :b"),
    ("-", "SELECT 1"),
    ("e", "SELECT e':e', :e"),
    ("w", "SELECT 'a':w"),
    ("-", "SELECT $1, ::int"),
    ("t", "SELECT '-' || :t"),
    ("t", "SELECT 2-:t"),
    ("p", "SELECT :p\n"),
    ("p", "SELECT x FROM y WHERE z = :p;"),
]

STYLE = [
    ("qmark", "a,b", "SELECT * FROM t WHERE a = ? AND b = ?"),
    ("qmark", "a", "SELECT '?' , ?"),
    ("numeric", "a,b", "SELECT :1, :2, :1"),
    ("numeric", "-", "SELECT x::int, a:=1"),
    ("named", "a,b", "SELECT :a, :b, :a"),
    ("named", "a", "SELECT :a, :b"),
    ("format", "a,b", "SELECT %s, %s"),
    ("format", "a", "SELECT '%s', %s, 100%%"),
    ("format", "a", "SELECT %d"),
    ("pyformat", "a,b", "SELECT %(a)s, %(b)s, %(a)s"),
    ("pyformat", "a", "SELECT %(a)s, %s"),
    ("pyformat", "a", "SELECT %s, %(a)s"),
    ("pyformat", "a", "SELECT %(a)x, %(a)s"),
    ("pyformat", "a", "SELECT 50%% off, %(a)s"),
    ("qmark", "a", "SELECT \"?\", E'\\'?', $$?$$, ?"),
    ("qmark", "a", "SELECT 1 -- ?\n, ?"),
    ("bogus", "a", "SELECT ?, :a"),
    ("named", "a", "SELECT :a::text"),
]

VALUES = [
    "None", "True", "False", "0", "-17", "2.5", "1e+300", "-0.0", "float('inf')", "float('nan')",
    "'plain'", "\"it's\"", "''", "b''", "b'\\x00\\x01\\xfe'", "bytearray(b'ab')",
    "Decimal('12.50')", "Decimal('-0.001')", "Decimal('NaN')",
    "date(2024, 2, 29)", "date(1, 1, 1)", "time(23, 59, 59, 999999)", "time(7, 5)",
    "datetime(2024, 2, 29, 23, 30, 0, 0)", "datetime(2024, 2, 29, 23, 30, 0, 250000, tz=-3600)",
    "datetime(2024, 3, 1, 0, 15, 0, 0, tz=19800)", "datetime(1999, 12, 31, 23, 59, 59, 999999, tz=0)",
    "timedelta(0, 0, 0)", "timedelta(-1, 86399, 999999)", "timedelta(400, 3600, 1)",
    "PGInterval(years=1, months=2)", "PGInterval(weeks=3, hours=-4, seconds=1.5)",
    "UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')",
    "IPv4Address('127.0.0.1')", "IPv4Network('192.168.0.0/24')", "IPv6Address('2001:db8::1')",
    "IPv6Network('fe80::/10')", "IPv6Address('0:0:0:0:0:0:0:0')", "IPv6Address('1:0:0:2:0:0:0:3')",
    "[]", "[1, 2, 3]", "[[1, 2], [3, None]]", "['x', 'y z', 'a,b', 'q\"', 'back\\\\slash', '{', 'NULL', '']",
    "[True, 2.5, Decimal('1.0'), date(2024, 1, 2)]", "[b'\\x01', {'k': 'v'}, (1, 2)]",
    "[' lead', 'tab\\there', 'nl\\n']",
    "(1, 'a', None)", "(None, None)", "((1, 2), [3, 4])", "('x y', b'\\xff')",
    "{}", "{'a': 1, 'b': [True, None, 2.5], 'c': {'d': 'e'}}", "{'u': 'caf\\xe9', 'q': 'say \"hi\"'}",
    "{'n': float('inf')}",
    "Range(1, 5, '[)')", "Range(None, date(2024, 1, 1), '(]')", "Range(Decimal('1.5'), None, '[)')",
    "Range(is_empty=True)", "Range(datetime(2024, 1, 1, 0, 0, 0, 0), datetime(2024, 1, 2, 0, 0, 0, 0), '[)')",
]

IDENTS = ["'users'", "'Users'", "'user id'", "'_hidden'", "'1st'", "'a$b'", "'quote\"d'", "'caf\\xe9'",
          "'ok_2'", "''", "5", "'nul\\x00'", "'select'"]

LITERALS = [
    "None", "True", "False", "42", "-1.5", "Decimal('3.14')", "b'\\xde\\xad'", "\"O'Reilly\"",
    "'plain'", "datetime(2024, 6, 1, 12, 0, 0, 0)", "datetime(2024, 6, 1, 12, 0, 0, 0, tz=7200)",
    "date(2024, 6, 1)", "time(12, 0, 0, 5)", "timedelta(1, 2, 3)", "['a', \"b'c\", None]", "[[1], [2]]",
    "UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')", "IPv4Address('10.0.0.1')", "{'k': \"it's\"}",
    "(1, 'two')", "Range(1, 2, '[)')", "PGInterval(days=1)",
]

INPUTS = [
    (23, "42"), (23, " -7 "), (23, "1_000"), (23, "4.5"), (23, ""), (20, "+12"), (21, "0x10"),
    (701, "3.14159"), (701, "1e-7"), (701, "-Infinity"), (701, "NaN"), (701, "1e400"), (701, "abc"),
    (700, "0.1"), (701, "100000000000000000"), (701, "0.0001"), (701, "0.00001"),
    (1700, "0.10"), (1700, "-123456789012345678901234567890.5"), (1700, "NaN"), (1700, "Infinity"),
    (1700, "1.2.3"), (16, "t"), (16, "f"), (16, "true"),
    (17, "\\x00ff10"), (17, "\\x"), (17, "\\x0g"), (17, "\\x0"), (17, "\\x00 ff"),
    (1082, "2024-02-29"), (1082, "2023-02-29"), (1082, "infinity"), (1082, "0044-03-15 BC"),
    (1082, "12345-01-01"), (1082, "2024-1-5"),
    (1083, "08:30:00"), (1083, "08:30:00.5"), (1083, "08:30:00.1234567"), (1083, "24:00:00"),
    (1083, "8:5:3"), (1083, "08:30:60"),
    (1114, "2024-02-29 13:45:30"), (1114, "2024-02-29 13:45:30.000001"), (1114, "infinity"),
    (1114, "-infinity"), (1114, "0044-03-15 12:00:00 BC"), (1114, "10000-01-01 00:00:00"),
    (1184, "2024-02-29 13:45:30+00"), (1184, "2024-02-29 13:45:30.5-08"), (1184, "2024-02-29 13:45:30+05:30"),
    (1184, "2024-02-29 13:45:30.25-03:30"), (1184, "1900-01-01 00:00:00+00:53:28"), (1184, "-infinity"),
    (1186, "1 day 02:03:04"), (1186, "1 year 2 mons 3 days 04:05:06.5"), (1186, "-1 days +02:00:00"),
    (1186, "00:00:00.000001"), (1186, "@ 1 day 2 hours ago"), (1186, "@ 3 mins 4.5 secs"),
    (1186, "P1Y2M3DT4H5M6.5S"), (1186, "P3DT12H"), (1186, "1-2"), (1186, "3 4:05:06"),
    (1186, "-1-2 +3 -4:05:06.25"), (1186, "2 weeks"), (1186, "1 millennium 2 centuries 3 decades"),
    (114, '{"a": 1, "b": [true, false, null], "c": 1.5e3}'), (3802, '"text"'), (3802, "[1, -2.0, 3e0]"),
    (114, '{"esc": "\\u00e9\\n\\"", "neg": -0, "big": 1234567890123456789}'), (114, "{bad}"), (114, ""),
    (114, "[1, 2"), (114, '{"a" 1}'), (114, "1 2"), (114, "nan"), (114, "-Infinity"),
    (2950, "A0EEBC99-9C0B-4EF8-BB6D-6BB9BD380A11"), (2950, "{a0eebc999c0b4ef8bb6d6bb9bd380a11}"),
    (2950, "not-a-uuid"),
    (869, "10.1.2.3"), (869, "10.1.2.3/8"), (869, "::ffff:1.2.3.4"), (869, "fe80::1/64"), (869, "2001:DB8:0:0:1::1"),
    (869, "1:2:3:4:5:6:7:8"), (869, "300.1.1.1"), (869, "1::2::3"), (650, "192.168.0.0/16"), (650, "::/0"),
    (1009, '{one,two,"three four"}'), (1009, '{"a\\\\b","c\\"d",NULL,"NULL"}'), (1009, "{{a,b},{c,d}}"),
    (1007, "{1,-2,3}"), (1007, "{NULL,1}"), (1016, "{}"), (1231, "{1.5,NaN}"), (1000, "{t,f,NULL}"),
    (1182, "{2024-01-01,infinity}"), (199, '{"{\\"a\\": 1}","[2]"}'), (1022, "{1.5,Infinity}"),
    (1115, '{"2024-01-01 00:00:00"}'), (2951, "{a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11}"),
    (1041, "{10.0.0.1,10.0.0.0/8}"), (1001, '{"\\\\x00ff"}'),
    (3904, "[1,10)"), (3904, "empty"), (3904, "(,5]"), (3926, "[-5,)"), (3912, "[2024-01-01,2024-02-01)"),
    (3906, "(1.5,2.25]"), (3908, '["2024-01-01 00:00:00","2024-01-02 12:00:00")'),
    (3910, '["2024-01-01 00:00:00+00",)'), (4451, "{[1,3),[5,7)}"), (4451, "{}"), (4535, "{[2024-01-01,2024-01-05)}"),
    (3905, '{"[1,2)","[3,4)"}'),
    (600, "(1.5,-2)"), (600, "(0,1e-5)"), (2249, '(1,"a b",)'), (2249, '("x\\"y",,"")'), (2249, "()"),
    (22, "1 2 3"), (22, ""), (790, "$1,000.00"), (829, "08:00:2b:01:02:03"), (19, "pg_catalog"),
    (1043, "varchar"), (1042, "char  "), (25, "tab\there"), (705, "unknown"), (3615, "'fat' & 'rat'"),
]


def main():
    os.makedirs(DATA, exist_ok=True)
    build_sessions()
    jobs = []
    for names, sql in STMT:
        jobs.append(f"stmt {names} {sql!r}")
    for style, names, sql in STYLE:
        jobs.append(f"style {style} {names} {sql!r}")
    for v in IDENTS:
        jobs.append(f"ident {v}")
    for v in LITERALS:
        jobs.append(f"literal {v}")
    for v in VALUES:
        jobs.append(f"out {v}")
    for oid, text in INPUTS:
        jobs.append(f"in {oid} {text!r}")
    files = []
    for name, opts, server, ops in SESSIONS:
        jobs.append(f"session {name} {opts}")
        for op in ops:
            jobs.append(f"op {op}")
        jobs.append("end")
        with open(os.path.join(DATA, name + ".bin"), "wb") as f:
            f.write(server)
        files.append(name + ".bin")
    with open(os.path.join(DATA, "jobs.txt"), "w") as f:
        f.write("\n".join(jobs) + "\n")
    with open(os.path.join(DATA, "files.txt"), "w") as f:
        f.write("\n".join(files) + "\n")
    print(f"{len(jobs)} job lines, {len(SESSIONS)} sessions, {nonce_at[0]} nonces")


main()
