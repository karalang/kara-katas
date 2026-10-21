# Writes data/: the zone files of a small company (Example Shop: its
# main zone, a partner zone, two reverse zones built with $GENERATE, and
# the next revision of the main zone), zone files for the reader's
# corners, files each reader and record error comes from, and jobs.tsv,
# the jobs mini_dnspython runs: loading zones, name arithmetic, building
# queries, answering them from a zone the way a small authoritative
# server does, decoding DNS messages off the wire (some well formed,
# some broken), reverse names and zone diffs. Everything is fixed, so
# the files never change.
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

FILES = {}

FILES["zones/example.com.zone"] = r'''; example.com: the zone of Example Shop
$TTL 1h
@   IN  SOA ns1.example.com. hostmaster.example.com. (
        2026102101 ; serial
        2h         ; refresh
        15m        ; retry
        2w         ; expire
        5m )       ; negative caching
    IN  NS   ns1
    IN  NS   ns2.example.net.
    IN  MX   10 mail
    IN  MX   20 mail2.example.net.
    IN  TXT  "v=spf1 mx include:_spf.example.net -all"
    IN  CAA  0 issue "letsencrypt.org"
    IN  CAA  0 iodef "mailto:security@example.com"
    IN  A    192.0.2.10
    IN  AAAA 2001:db8:0:0::10

ns1     IN A    192.0.2.53
        IN AAAA 2001:DB8::53
mail    300 IN A 192.0.2.25
mail    IN A    192.0.2.26
www     IN CNAME @
shop    IN CNAME www
api     600 A   192.0.2.30
api     A       192.0.2.31
api     A       192.0.2.30   ; the same address again
_dmarc  TXT     "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"
_sip._tcp SRV   10 60 5060 sip1
          SRV   20 0 5060 sip2.example.net.
sip1    A       192.0.2.40
_443._tcp.www TLSA 3 1 1 ( 0123456789abcdef0123456789abcdef
                           0123456789ABCDEF0123456789ABCDEF )
ns1     SSHFP   4 2 9b1e6c8a2f0d4e3b7a5c1d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a
db      HINFO   "x86_64" "Linux 6.1"
legacy  TXT     "a \"quoted\" word" two\032words "semi;colon" "tab\009x" ""
dev     NS      ns.dev
ns.dev  A       192.0.2.60
office  TYPE65280 \# 4 0a0b0c0d
printer A       \# 4 C0000263
WWW2    A       192.0.2.11
www2    A       192.0.2.12
Mixed.Case MX   5 MAIL
big     TXT     "record one of the big set, padded out to make the answer long"
big     TXT     "record two of the big set, padded out to make the answer long"
big     TXT     "record three of the big set, padded out to make the answer long"
big     TXT     "record four of the big set, padded out to make the answer long"
big     TXT     "record five of the big set, padded out to make the answer long"
big     TXT     "record six of the big set, padded out to make the answer long"
big     TXT     "record seven of the big set, padded out to make the answer long"
big     TXT     "record eight of the big set, padded out to make the answer long"
$ORIGIN corp.example.com.
vpn     A       198.51.100.1
intranet CNAME  vpn
@       TXT     "corp"
$ORIGIN example.com.
*.cdn   CNAME   cdn.example.net.
'''

# the next revision: a serial bump, a moved mail host, a new name, a
# removed one and a TTL change
FILES["zones/example.com.next.zone"] = r'''$TTL 1h
@   IN  SOA ns1.example.com. hostmaster.example.com. 2026102201 2h 15m 2w 5m
    IN  NS   ns1
    IN  NS   ns2.example.net.
    IN  MX   10 mail
    IN  MX   30 mail3
    IN  TXT  "v=spf1 mx include:_spf.example.net -all"
    IN  A    192.0.2.10
    IN  AAAA 2001:db8::10
ns1     IN A    192.0.2.53
        IN AAAA 2001:db8::53
mail    IN A    192.0.2.25
mail3   IN A    192.0.2.27
www     IN CNAME @
shop    IN CNAME www
api     300 A   192.0.2.30
api     300 A   192.0.2.31
status  A       192.0.2.80
_dmarc  TXT     "v=DMARC1; p=reject; rua=mailto:dmarc@example.com"
'''

FILES["zones/example.net.zone"] = r'''$ORIGIN example.net.
$TTL 86400
example.net. 3600 IN SOA ns2.example.net. admin.example.net. 7 3600 900 1209600 300
example.net. IN 3600 NS ns2
             NS ns3.example.org.
ns2 A 203.0.113.2
mail2 IN A 203.0.113.25
sip2 1d IN A 203.0.113.40
_spf TXT "v=spf1 ip4:192.0.2.0/24 ip4:203.0.113.0/24 -all"
cdn 60 CNAME edge.cdn.example.org.
$TTL 5m
ttl-test A 203.0.113.99
	A 203.0.113.98
other.example.org. A 203.0.113.1   ; outside the zone, so it is skipped
'''

FILES["zones/2.0.192.in-addr.arpa.zone"] = r'''$TTL 1d
@ SOA ns1.example.com. hostmaster.example.com. 1 1h 15m 1w 1h
@ NS ns1.example.com.
10 PTR example.com.
25 PTR mail.example.com.
26 PTR mail.example.com.
53 PTR ns1.example.com.
$GENERATE 100-104 $ PTR dhcp-$.example.com.
$GENERATE 200-206/3 ${0,3,d} 600 PTR h${-199,2,x}.lab.example.com.
$GENERATE 7-9 ${0,0,o} IN PTR oct-${8}.example.com.
'''

FILES["zones/db8.ip6.zone"] = r'''$TTL 1h
@ SOA ns1.example.com. hostmaster.example.com. 1 1h 15m 1w 1h
@ NS ns1.example.com.
0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0 PTR example.com.
3.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0 PTR ns1.example.com.
$GENERATE 10-12 ${0,7,n}.0.0.0.0.0.0.0.0.0.0.0.0 PTR v6-$.example.com.
$GENERATE 250-251 ${0,7,N}.0.0.0.0.0.0.0.0.0.0.0.1 PTR V6-${0,4,X}.example.com.
'''

# the reader's corners
FILES["cases/inherit.zone"] = r'''$TTL 300
@ SOA ns hostmaster 1 1 1 1 1
  NS ns
ns A 192.0.2.1
   A 192.0.2.2

   AAAA 2001:db8::1
; a comment line
host A 192.0.2.3 ; a trailing comment
	MX 10 host
'''

FILES["cases/merge.zone"] = r'''$TTL 300
@ SOA ns hostmaster 1 1 1 1 1
@ NS ns
@ MX 10 mx1
@ NS NS
@ 60 NS ns2
ns A 192.0.2.1
NS A 192.0.2.9
alias CNAME one
alias CNAME two
@ 100 SOA ns hostmaster 2 2 2 2 2
txt TXT "Hello"
txt TXT "hello"
txt TXT "Hello"
'''

FILES["cases/ttls.zone"] = r'''@ 1d SOA ns hostmaster 1 2h 30m 1w 10m
@ NS ns
ns A 192.0.2.1
a 1w2d3h4m5s A 192.0.2.2
b A 192.0.2.3
c 0 A 192.0.2.4
d 4294967295 A 192.0.2.5
$TTL 1H
e A 192.0.2.6
'''

FILES["cases/soa_ttl.zone"] = r'''@ SOA ns hostmaster 1 2 3 4 1800
@ NS ns
ns A 192.0.2.1
'''

FILES["cases/relative_origin.zone"] = r'''$TTL 300
@ SOA ns hostmaster 1 1 1 1 1
@ NS ns
ns A 192.0.2.1
$ORIGIN sub
lost A 192.0.2.2
$ORIGIN sub.example.com.
found A 192.0.2.3
'''

FILES["cases/escapes.zone"] = r'''$TTL 300
@ SOA ns hostmaster 1 1 1 1 1
@ NS ns
ns A 192.0.2.1
odd\.label A 192.0.2.2
sp\032ace TXT "x"
semi\;colon TXT "y"
\@sign TXT "z"
quote TXT "say \"hi\"" "back\\slash" "\255\000\127"
utf TXT "caf\195\169" "ünï"
hinfo HINFO "c\112u" os
caa CAA 128 tbs "\077x"
'''

FILES["cases/generic.zone"] = r'''$TTL 300
@ SOA ns hostmaster 1 1 1 1 1
@ NS ns
ns A 192.0.2.1
g1 TYPE65280 \# 0
g2 TYPE65281 \# 6 01 0203 040506
g3 TYPE1 192.0.2.7
g4 A \# 4 c0 00 02 08
g5 TYPE99 "spf by number"
g6 MX \# 8 000a 046d61696c 00
g7 class1 A 192.0.2.9
g8 IN TYPE13 "cpu" "os"
'''

FILES["cases/caa_quirks.zone"] = r'''$TTL 300
@ SOA ns hostmaster 1 1 1 1 1
@ NS ns
ns A 192.0.2.1
@ CAA 0 issuewild ";"
@ CAA 0 issue "ca.example.net; account=1234"
@ CAA 0 Issue "mixed case tag"
'''

FILES["cases/empty_quoted.zone"] = r'''$TTL 300
@ SOA ns hostmaster 1 1 1 1 1
@ NS ns
"" A 192.0.2.1
'''

FILES["cases/comments_kept.zone"] = r'''$TTL 300
@ SOA ns hostmaster 1 1 1 1 1 ; the apex
@ NS ns ;primary
ns A 192.0.2.1 ;   spaced out
ns A 192.0.2.2
'''

# files the reader refuses
BROKEN = {
    "no_soa": "$TTL 300\n@ NS ns\nns A 192.0.2.1\n",
    "no_ns": "$TTL 300\n@ SOA ns hostmaster 1 1 1 1 1\nns A 192.0.2.1\n",
    "cname_then_a": "$TTL 300\n@ SOA ns hm 1 1 1 1 1\n@ NS ns\nwww CNAME ns\nwww A 192.0.2.1\n",
    "a_then_cname": "$TTL 300\n@ SOA ns hm 1 1 1 1 1\n@ NS ns\nwww A 192.0.2.1\nwww CNAME ns\n",
    "bad_ipv4": "$TTL 300\n@ SOA ns hm 1 1 1 1 1\n@ NS ns\nhost A 192.0.2.300\n",
    "ipv4_leading_zero": "$TTL 300\nhost A 192.0.02.1\n",
    "ipv4_short": "$TTL 300\nhost A 192.0.2\n",
    "bad_ipv6": "$TTL 300\nhost AAAA 2001:db8:::1\n",
    "ipv6_two_gaps": "$TTL 300\nhost AAAA 2001::db8::1\n",
    "ipv6_v4_bad": "$TTL 300\nhost AAAA ::ffff:192.0.2.300\n",
    "ipv6_long_chunk": "$TTL 300\nhost AAAA 2001:db8::12345\n",
    "ipv6_colon_end": "$TTL 300\nhost AAAA 2001:db8:1:\n",
    "unknown_type": "$TTL 300\nhost FOO bar\n",
    "type_too_big": "$TTL 300\nhost TYPE70000 x\n",
    "bad_ttl_unit": "$TTL 1x\n",
    "bad_ttl_trailing": "$TTL 1h30\n",
    "bad_ttl_record": "$TTL 300\nhost 5w5 A 192.0.2.1\n",
    "ttl_too_big": "host 4294967296 A 192.0.2.1\n",
    "unbalanced_open": "$TTL 300\n@ SOA ns hm ( 1 1 1 1 1\n",
    "unbalanced_close": "$TTL 300\nhost A 192.0.2.1 )\n",
    "newline_in_quote": "$TTL 300\nhost TXT \"open\nclose\"\n",
    "eof_in_quote": "$TTL 300\nhost TXT \"open",
    "escape_at_eol": "$TTL 300\nhost TXT abc\\\n",
    "include": "$TTL 300\n$INCLUDE other.zone\n",
    "unknown_directive": "$TTL 300\n$FOO bar\n",
    "label_too_long_rdata": "$TTL 300\nhost CNAME " + "x" * 64 + "\n",
    "label_too_long_owner": "$TTL 300\n" + "y" * 64 + " A 192.0.2.1\n",
    "name_too_long_owner": "$TTL 300\n" + ".".join(["a" * 60] * 5) + " A 192.0.2.1\n",
    "name_too_long_rdata": "$TTL 300\nhost CNAME " + ".".join(["b" * 60] * 5) + "\n",
    "empty_label": "$TTL 300\na..b A 192.0.2.1\n",
    "bad_escape": "$TTL 300\na\\1b A 192.0.2.1\n",
    "escape_too_big_owner": "$TTL 300\n\\300x A 192.0.2.1\n",
    "escape_too_big_rdata": "$TTL 300\nhost CNAME \\300x\n",
    "escape_too_big_txt": "$TTL 300\nhost TXT \"\\300\"\n",
    "class_mismatch": "$TTL 300\nhost CH A 192.0.2.1\n",
    "class_by_number": "$TTL 300\nhost CLASS2 A 192.0.2.1\n",
    "non_origin_soa": "$TTL 300\n@ SOA ns hm 1 1 1 1 1\nsub SOA ns hm 1 1 1 1 1\n",
    "missing_ttl": "host A 192.0.2.1\n",
    "mx_too_big": "$TTL 300\nhost MX 70000 mail\n",
    "mx_not_int": "$TTL 300\nhost MX ten mail\n",
    "caa_flags": "$TTL 300\nhost CAA 300 issue \"x\"\n",
    "caa_tag": "$TTL 300\nhost CAA 0 is-sue \"x\"\n",
    "txt_too_long": "$TTL 300\nhost TXT \"" + "z" * 256 + "\"\n",
    "txt_none": "$TTL 300\nhost TXT\n",
    "hinfo_too_long": "$TTL 300\nhost HINFO \"" + "c" * 256 + "\" os\n",
    "hinfo_short": "$TTL 300\nhost HINFO cpu\n",
    "extra_token": "$TTL 300\nhost A 192.0.2.1 extra\n",
    "generic_length": "$TTL 300\nhost TYPE65280 \\# 4 0a0b0c\n",
    "generic_odd": "$TTL 300\nhost TYPE65280 \\# 2 abc\n",
    "generic_no_hash": "$TTL 300\nhost TYPE65280 0a0b\n",
    "generic_known_bad": "$TTL 300\nhost A \\# 5 0102030405\n",
    "sshfp_hex": "$TTL 300\nhost SSHFP 4 2 zz\n",
    "sshfp_empty": "$TTL 300\nhost SSHFP 4 2\n",
    "tlsa_odd": "$TTL 300\nhost TLSA 3 1 1 abc\n",
    "soa_serial": "$TTL 300\n@ SOA ns hm 1h 1 1 1 1\n",
    "soa_short": "$TTL 300\n@ SOA ns hm 1 1 1\n",
    "srv_port": "$TTL 300\nhost SRV 1 2 65536 target\n",
    "name_only": "$TTL 300\nwww\n@ NS ns\n",
    "owner_then_eof": "$TTL 300\nwww",
    "gen_range": "$TTL 300\n$GENERATE 10-5 $ A 192.0.2.$\n",
    "gen_parse": "$TTL 300\n$GENERATE 1-x $ A 192.0.2.$\n",
    "gen_nostop": "$TTL 300\n$GENERATE 7 $ A 192.0.2.$\n",
    "gen_negative": "$TTL 300\n$GENERATE -1-4 $ A 192.0.2.$\n",
    "gen_base": "$TTL 300\n$GENERATE 1-2 ${0,2,z} A 192.0.2.$\n",
    "gen_no_ttl": "$GENERATE 1-2 h$ A 192.0.2.$\n",
    "gen_type": "$TTL 300\n$GENERATE 1-2 h$ BOGUS x\n",
    "gen_no_rhs": "$TTL 300\n$GENERATE 1-2 h$ A\n",
    "gen_bad_rdata": "$TTL 300\n$GENERATE 250-256 h$ A 192.0.2.$\n",
    "gen_class": "$TTL 300\n$GENERATE 1-2 h$ CH A 192.0.2.$\n",
}
for name, text in BROKEN.items():
    FILES["broken/" + name + ".zone"] = text


def label(s):
    if isinstance(s, str):
        s = s.encode()
    return bytes([len(s)]) + s


def wname(*labels):
    return b"".join(label(x) for x in labels) + b"\x00"


def header(id, flags, qd, an, ns, ar):
    return struct.pack("!HHHHHH", id, flags, qd, an, ns, ar)


def rr(name, rtype, rclass, ttl, rdata):
    return name + struct.pack("!HHIH", rtype, rclass, ttl, len(rdata)) + rdata


def ptr(off):
    return struct.pack("!H", 0xC000 | off)


EX = wname("www", "example", "com")
Q_A = EX + struct.pack("!HH", 1, 1)

WIRES = {}
# a recursive resolver's answer for www.example.com, names compressed
WIRES["answer"] = (header(0x1234, 0x8180, 1, 2, 0, 0) + Q_A
                   + rr(ptr(12), 5, 1, 300, wname("web", "example", "net"))
                   + rr(ptr(12 + len(Q_A) + 12), 1, 1, 60, bytes([192, 0, 2, 10])))
# the same rrset twice with different TTLs, the second name in capitals
WIRES["merge_ttl"] = (header(7, 0x8400, 1, 3, 0, 0) + Q_A
                      + rr(ptr(12), 1, 1, 300, bytes([192, 0, 2, 1]))
                      + rr(wname("WWW", "EXAMPLE", "COM"), 1, 1, 60, bytes([192, 0, 2, 2]))
                      + rr(ptr(12), 1, 1, 0x80000000, bytes([192, 0, 2, 3])))
# two CNAMEs for one name: the second replaces the first
WIRES["two_cnames"] = (header(8, 0x8180, 1, 2, 0, 0) + Q_A
                       + rr(ptr(12), 5, 1, 300, wname("a", "example", "net"))
                       + rr(ptr(12), 5, 1, 300, wname("b", "example", "net")))
# an NXDOMAIN with the SOA in the authority section
WIRES["nxdomain"] = (header(9, 0x8183, 1, 0, 1, 0)
                     + wname("nope", "example", "com") + struct.pack("!HH", 1, 1)
                     + rr(ptr(12 + 5), 6, 1, 300,
                          wname("ns1", "example", "com") + wname("hostmaster", "example", "com")
                          + struct.pack("!IIIII", 2026102101, 7200, 900, 1209600, 300)))
# every record type the port knows, uncompressed
ALLTYPES = [
    (1, bytes([198, 51, 100, 7])),
    (28, bytes.fromhex("20010db8000000000000ff0000420001")),
    (28, bytes.fromhex("00000000000000000000ffffc0000201")),
    (28, bytes.fromhex("00000000000000000000000000000001")),
    (28, bytes.fromhex("fe800000000000000000000000000000")),
    (2, wname("ns", "example", "org")),
    (12, wname("host", "example", "org")),
    (15, struct.pack("!H", 5) + wname("mx", "example", "org")),
    (16, label("first") + label("") + label(b"bin\x00\xff\"")),
    (99, label("v=spf1 -all")),
    (33, struct.pack("!HHH", 1, 2, 443) + wname("svc", "example", "org")),
    (257, b"\x00" + label("issue") + b"ca.example.net"),
    (13, label("ARM") + label("Plan 9")),
    (44, b"\x01\x01" + bytes(range(20))),
    (52, b"\x03\x01\x01" + bytes(range(70))),
    (39, wname("other", "example")),
    (65280, b"\xde\xad\xbe\xef"),
    (65280, b""),
]
body = b""
for t, data in ALLTYPES:
    body += rr(wname("t", "example", "org"), t, 1, 3600, data)
WIRES["alltypes"] = header(10, 0x8500, 0, len(ALLTYPES), 0, 0) + body
# odd header values: opcode NOTIFY, an unknown opcode, an rcode with no name
WIRES["notify"] = header(11, 0x2400, 1, 0, 0, 0) + wname("example", "com") + struct.pack("!HH", 6, 1)
WIRES["opcode3"] = header(12, 0x1800, 0, 0, 0, 0)
WIRES["rcode12"] = header(13, 0x87bc, 0, 0, 0, 0)
WIRES["two_questions"] = (header(14, 0x0100, 2, 0, 0, 0) + Q_A
                          + wname("example", "com") + struct.pack("!HH", 15, 1))
WIRES["chaos"] = (header(15, 0x0100, 1, 0, 0, 0) + wname("version", "bind") + struct.pack("!HH", 16, 3))
WIRES["escaped_name"] = (header(16, 0x8000, 1, 0, 0, 0)
                         + wname(b"a.b", b"sp ace", b"\x00\x7f\xc3\xa9", b"semi;@$")
                         + struct.pack("!HH", 1, 1))
# broken messages
WIRES["short"] = header(17, 0, 0, 0, 0, 0)[:11]
WIRES["empty"] = b""
WIRES["trailing"] = header(18, 0x0100, 1, 0, 0, 0) + Q_A + b"\x00"
WIRES["forward_pointer"] = header(19, 0x0100, 1, 0, 0, 0) + ptr(40) + struct.pack("!HH", 1, 1)
WIRES["self_pointer"] = header(20, 0x0100, 1, 0, 0, 0) + ptr(12) + struct.pack("!HH", 1, 1)
WIRES["pointer_loop"] = (header(21, 0x0100, 1, 1, 0, 0) + Q_A
                         + label("x") + ptr(12 + len(Q_A)) + struct.pack("!HHIH", 1, 1, 0, 0))
WIRES["label_type"] = header(22, 0x0100, 1, 0, 0, 0) + b"\x41abc\x00" + struct.pack("!HH", 1, 1)
WIRES["truncated_name"] = header(23, 0x0100, 1, 0, 0, 0) + b"\x03ww"
WIRES["truncated_question"] = header(24, 0x0100, 1, 0, 0, 0) + EX + b"\x00"
WIRES["rdlen_too_big"] = (header(25, 0x8180, 1, 1, 0, 0) + Q_A
                          + ptr(12) + struct.pack("!HHIH", 1, 1, 60, 10) + bytes([192, 0, 2, 1]))
WIRES["a_short"] = (header(26, 0x8180, 1, 1, 0, 0) + Q_A + rr(ptr(12), 1, 1, 60, bytes([192, 0, 2])))
WIRES["aaaa_short"] = (header(27, 0x8180, 1, 1, 0, 0) + Q_A + rr(ptr(12), 28, 1, 60, bytes(4)))
WIRES["mx_leftover"] = (header(28, 0x8180, 1, 1, 0, 0) + Q_A
                        + rr(ptr(12), 15, 1, 60, struct.pack("!H", 1) + ptr(12) + b"\x00\x00"))
WIRES["txt_overrun"] = (header(29, 0x8180, 1, 1, 0, 0) + Q_A + rr(ptr(12), 16, 1, 60, b"\x09abc"))
WIRES["txt_empty"] = (header(38, 0x8180, 1, 1, 0, 0) + Q_A + rr(ptr(12), 16, 1, 60, b""))
WIRES["caa_bad_tag"] = (header(39, 0x8180, 1, 1, 0, 0) + Q_A + rr(ptr(12), 257, 1, 60, b"\x00\x02a-b"))
WIRES["opt_in_answer"] = (header(30, 0x8180, 1, 1, 0, 0) + Q_A + rr(b"\x00", 41, 4096, 0, b""))
WIRES["tsig_in_answer"] = (header(31, 0x8180, 1, 1, 0, 0) + Q_A + rr(ptr(12), 250, 255, 0, b""))
long_name = b""
for i in range(5):
    long_name += label(chr(ord("a") + i) * 60)
WIRES["name_too_long"] = (header(32, 0x8180, 1, 1, 0, 0) + Q_A
                          + rr(long_name + ptr(12), 1, 1, 60, bytes([192, 0, 2, 1])))
WIRES["soa_short"] = (header(33, 0x8180, 1, 1, 0, 0) + Q_A
                      + rr(ptr(12), 6, 1, 60, b"\x00\x00" + struct.pack("!III", 1, 2, 3)))
WIRES["caa_short"] = (header(34, 0x8180, 1, 1, 0, 0) + Q_A + rr(ptr(12), 257, 1, 60, b"\x00\x05iss"))
WIRES["srv_short"] = (header(35, 0x8180, 1, 1, 0, 0) + Q_A + rr(ptr(12), 33, 1, 60, b"\x00\x01\x00"))
WIRES["rr_header_short"] = (header(36, 0x8180, 1, 1, 0, 0) + Q_A + ptr(12) + b"\x00\x01\x00")
WIRES["count_too_big"] = (header(37, 0x8180, 1, 2, 0, 0) + Q_A + rr(ptr(12), 1, 1, 60, bytes([192, 0, 2, 1])))

ZONE = "zones/example.com.zone"


def jobs():
    j = []
    for name in sorted(n for n in FILES if n.startswith("zones/")):
        origin = name[len("zones/"):-len(".zone")]
        if origin == "example.com.next":
            origin = "example.com"
        if origin == "db8.ip6":
            origin = "0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa"
        j.append(["zone", name, origin, "rel"])
    j.append(["zone", ZONE, "example.com", "abs"])
    j.append(["zone", ZONE, "example.com.", "origin"])
    j.append(["zone", "zones/example.net.zone", "example.net", "abs"])
    j.append(["zone", ZONE, "example.com", "comments"])
    for name in sorted(n for n in FILES if n.startswith("cases/")):
        j.append(["zone", name, "example.com", "rel"])
    j.append(["zone", "cases/comments_kept.zone", "example.com", "comments"])
    j.append(["zone", "cases/escapes.zone", "example.com", "abs"])
    j.append(["zone", "cases/merge.zone", "Example.COM", "abs"])
    for name in sorted(n for n in FILES if n.startswith("broken/")):
        j.append(["zone", name, "example.com", "rel"])
    j.append(["zone", "broken/no_soa.zone", "example.com", "nocheck"])
    j.append(["zone", "broken/no_ns.zone", "example.com", "nocheck"])
    j.append(["zone", ZONE, "com", "rel"])
    j.append(["zone", ZONE, "example.org", "nocheck"])

    # names
    for text, origin in [
        ("www.example.com", "."), ("www.example.com.", "-"), ("www.example.com", "-"),
        ("@", "example.com"), ("@", "-"), (".", "-"), ("", "example.com"),
        ("WWW.Example.COM.", "-"), ("a\\.b.example.com.", "-"), ("a\\032b\\099.c", "example.org"),
        ("\\@.\\$.\\;.\\(\\).\\\"q\\\".", "-"), ("*.example.com.", "-"), ("ex\\ample.com.", "-"),
        ("tab\\009here.", "-"), ("high\\200\\255.", "-"), ("a..b", "-"), (".a", "-"), ("a\\1", "-"),
        ("a\\12x.", "-"), ("x" * 63 + ".", "-"), ("x" * 64 + ".", "-"),
        (".".join(["a" * 63] * 3) + "." + "b" * 61 + ".", "-"),
        (".".join(["a" * 63] * 3) + "." + "b" * 62 + ".", "-"),
        ("\\300.", "-"), ("relative.name", "rel.origin"), ("a.b.c.d.e.f.g", "-"),
    ]:
        j.append(["name", text, origin])
    for a, b in [
        ("www.example.com.", "example.com."), ("example.com.", "www.example.com."),
        ("www.example.com.", "WWW.EXAMPLE.COM."), ("a.example.com.", "b.example.com."),
        ("mail.example.com.", "www.example.net."), ("www", "www.example.com."),
        ("www.example.com.", "www"), ("a.b", "b"), ("x.a.b", "y.a.b"), (".", "com."),
        ("@", "@"), ("@", "a"), ("Z.example.com.", "a.example.com."), ("\\200.com.", "z.com."),
        ("a.example.com.", "a-b.example.com."), ("ab.example.com.", "a.example.com."),
        ("example.com.", "."), ("com.", "net."),
    ]:
        j.append(["cmp", a, b])
    for text, depth in [("www.example.com.", "0"), ("www.example.com.", "1"), ("www.example.com.", "2"),
                        ("www.example.com.", "4"), ("www.example.com.", "5"), ("a.b", "2"), ("a.b", "-1")]:
        j.append(["split", text, depth])
    for a, b in [("www", "example.com."), ("www.", "example.com."), ("www.", "@"), ("@", "@"),
                 ("a.b", "c.d"), ("x" * 63, ".".join(["y" * 63] * 3) + ".")]:
        j.append(["concat", a, b])
    for text in ("www.example.com.", "com.", ".", "@", "a"):
        j.append(["parent", text])

    # TTLs and addresses
    for text in ("3600", "1h", "1H30M", "2w1d", "1w2d3h4m5s", "0", "", "h", "1h30", "1y", "4294967295",
                 "4294967296", "60s60s", "007"):
        j.append(["ttl", text])
    for text in ("2001:db8::1", "2001:DB8:0:0:0:0:0:1", "::", "::1", "1::", "::ffff:192.0.2.1",
                 "::192.0.2.1", "::ffff:0:192.0.2.1", "1:0:0:2:0:0:0:3", "0:0:1:0:0:1:0:0",
                 "1:2:3:4:5:6:7:8", "fe80::1:0:0:0", "2001:db8::0:1", "0::0", "1:2:3:4:5:6:7::",
                 "::1:2:3:4:5:6:7", "0:0:0:0:0:ffff:c000:201", "0:0:0:0:0:0:c000:201",
                 "1:2:3:4:5:6:7:8:9", "1:2:3", "12345::", "g::1", ":1::2", "1::2:", "::ffff:1.2.3"):
        j.append(["ip6", text])
    for text in ("192.0.2.1", "2001:db8::53", "::ffff:198.51.100.7", "::1", "10.0.0.256", "nonsense", "1.2.3"):
        j.append(["rev", text])
    for text in ("1.2.0.192.in-addr.arpa.", "3.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
                 "4.3.in-addr.arpa.", "www.example.com.", "300.2.0.192.in-addr.arpa."):
        j.append(["unrev", text])

    # queries
    for qname, qtype, qid in [("www.example.com", "A", "4660"), ("example.com.", "MX", "1"),
                              ("Example.COM", "TYPE65280", "65535"), ("_sip._tcp.example.com", "SRV", "0"),
                              ("example.com", "ANY", "42"), ("b\\.c.example.com", "AAAA", "77"),
                              ("example.com", "NOPE", "1")]:
        j.append(["query", qname, qtype, qid])

    # answering queries from the zone
    for qname, qtype in [
        ("example.com", "SOA"), ("example.com", "NS"), ("example.com", "MX"), ("WWW.Example.com", "A"),
        ("shop.example.com", "AAAA"), ("shop.example.com", "CNAME"), ("api.example.com", "A"),
        ("mail.example.com", "MX"), ("nothere.example.com", "A"), ("ns1.example.com", "TXT"),
        ("_sip._tcp.example.com", "SRV"), ("host.dev.example.com", "A"), ("dev.example.com", "NS"),
        ("example.com", "ANY"), ("intranet.corp.example.com", "A"), ("www.example.org", "A"),
        ("legacy.example.com", "TXT"), ("_443._tcp.www.example.com", "TLSA"), ("office.example.com", "TYPE65280"),
        ("mixed.case.example.com", "MX"), ("example.com", "CAA"), ("big.example.com", "TXT"),
        ("www2.example.com", "A"),
    ]:
        j.append(["serve", ZONE, "example.com", qname, qtype, "100"])
    j.append(["serve", ZONE, "example.com", "big.example.com", "TXT", "101", "udp"])
    j.append(["serve", ZONE, "example.com", "example.com", "ANY", "102", "udp"])
    j.append(["serve", "zones/2.0.192.in-addr.arpa.zone", "2.0.192.in-addr.arpa", "103.2.0.192.in-addr.arpa", "PTR", "103"])
    j.append(["serve", "zones/example.net.zone", "example.net", "cdn.example.net", "A", "104"])
    for name in ("two_questions", "chaos", "answer", "trailing", "short"):
        j.append(["servewire", ZONE, "example.com", WIRES[name].hex()])

    # decoding messages
    for name in WIRES:
        j.append(["wire", name, WIRES[name].hex()])

    # what changed between two revisions of a zone
    j.append(["diff", ZONE, "zones/example.com.next.zone", "example.com"])
    j.append(["diff", "zones/example.com.next.zone", ZONE, "example.com"])
    j.append(["diff", "cases/merge.zone", "cases/inherit.zone", "example.com"])
    return j


if os.path.isdir(DATA):
    shutil.rmtree(DATA)
for name, text in FILES.items():
    path = os.path.join(DATA, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8", newline="\n") as f:
    for job in jobs():
        f.write("\t".join(job) + "\n")
