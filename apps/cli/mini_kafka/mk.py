# Writes data/: record sets as a broker stores and serves them (v2 batches,
# v0/v1 message sets, gzip-compressed ones, and broken copies of each),
# response streams for the wire sessions, the record lists the build jobs
# append, and jobs.txt. The well-formed inputs come from the vendored
# kafka-python itself; the broken ones are patched byte by byte.
import gzip
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kstub  # noqa: E402

kstub.install()

import kafka.record.default_records as dr  # noqa: E402
import kafka.record.legacy_records as lr  # noqa: E402
from kafka.record.memory_records import MemoryRecordsBuilder  # noqa: E402
from kafka.record.util import calc_crc32c, encode_varint  # noqa: E402
from kafka.protocol.api import ResponseHeader  # noqa: E402
from kafka.protocol import metadata, produce, fetch, api_versions, find_coordinator  # noqa: E402,F401
from kafka.protocol.types import Int32  # noqa: E402


def gzip0(data):
    # kafka-python stamps the current time into the gzip header; inputs
    # must not change from one run of mk.py to the next.
    return gzip.compress(data, compresslevel=9, mtime=0)


dr.gzip_encode = gzip0
lr.gzip_encode = gzip0

DATA = os.path.join(HERE, 'data')
os.makedirs(DATA, exist_ok=True)
files = []


def put(name, data):
    with open(os.path.join(DATA, name), 'wb') as f:
        f.write(bytes(data))
    files.append(name)


T0 = 1761300000000

ORDERS = [
    (T0, b'user-17', b'{"order":1042,"sku":"A-17","qty":2}',
     [('content-type', b'application/json'), ('trace-id', b'4bf92f3577b34da6')]),
    (T0 + 12, b'user-3', b'{"order":1043,"sku":"B-02","qty":1}',
     [('content-type', b'application/json')]),
    (T0 + 12, None, b'heartbeat', []),
    (T0 + 250, b'user-17', None, [('reason', b'gdpr-erasure')]),
    (T0 + 251, b'caf\xc3\xa9-9', b'prix: 4,50 \xe2\x82\xac', [('lang', b'fr'), ('empty', None)]),
    (T0 + 4000, b'bin', b"\x00\x01\x02'\"\\\n\t\r\x7f\x80\xff", []),
    (T0 - 2000, b'late', b'arrived out of order', [('retry', b'')]),
]


def v2_batch(records, base_offset=0, codec=0, txn=False, pid=-1, epoch=-1, seq=-1, offset=0):
    b = MemoryRecordsBuilder(2, codec, 1 << 20, offset=offset, transactional=txn,
                             producer_id=pid, producer_epoch=epoch, base_sequence=seq)
    for ts, k, v, h in records:
        b.append(ts, k, v, h)
    b.close()
    buf = bytearray(b.buffer())
    struct.pack_into('>q', buf, 0, base_offset)
    return buf


def fix_crc(buf):
    struct.pack_into('>I', buf, 17, calc_crc32c(bytes(buf[21:])))
    return buf


def fix_len(buf):
    struct.pack_into('>i', buf, 8, len(buf) - 12)
    return buf


def set_attrs(buf, attrs):
    struct.pack_into('>h', buf, 21, attrs)
    return fix_crc(buf)


def raw_record(ts_delta, off_delta, key, value, headers, hcount=None, length_adj=0):
    body = bytearray(b'\x00')
    encode_varint(ts_delta, body.append)
    encode_varint(off_delta, body.append)
    for x in (key, value):
        if x is None:
            encode_varint(-1, body.append)
        else:
            encode_varint(len(x), body.append)
            body.extend(x)
    encode_varint(len(headers) if hcount is None else hcount, body.append)
    for hk, hv in headers:
        if isinstance(hk, int):
            encode_varint(hk, body.append)
        else:
            encode_varint(len(hk), body.append)
            body.extend(hk)
        if hv is None:
            encode_varint(-1, body.append)
        else:
            encode_varint(len(hv), body.append)
            body.extend(hv)
    out = bytearray()
    encode_varint(len(body) + length_adj, out.append)
    return out + body


def raw_batch(payload, count, base_offset=0, attrs=0, last_delta=None, first_ts=T0, max_ts=T0):
    hdr = bytearray(61)
    if last_delta is None:
        last_delta = count - 1
    dr.DefaultRecordBase.HEADER_STRUCT.pack_into(
        hdr, 0, base_offset, 0, 0, 2, 0, attrs, last_delta, first_ts, max_ts, -1, -1, -1, count)
    buf = hdr + bytearray(payload)
    return fix_crc(fix_len(buf))


def legacy_set(magic, records, codec=0, offset=0, absolute_inner=False):
    b = MemoryRecordsBuilder(magic, codec, 1 << 20, offset=offset)
    for ts, k, v in records:
        b.append(ts, k, v, [])
    b.close()
    return bytearray(b.buffer())


def legacy_msg(magic, offset, ts, key, value, attrs=0):
    lb = lr.LegacyRecordBatchBuilder(magic, 0, 1 << 20)
    size = lb.size_in_bytes(offset, ts, key, value)
    lb._buffer.extend(bytearray(size))
    lb._encode_msg(0, offset, ts, key, value, attributes=attrs)
    return bytearray(lb._buffer)


def legacy_crc(buf, start=0):
    # The CRC of the message at start covers magic onwards.
    length = struct.unpack_from('>i', buf, start + 8)[0]
    crc = zlib.crc32(bytes(buf[start + 16:start + 12 + length])) & 0xffffffff
    struct.pack_into('>I', buf, start + 12, crc)
    return buf


def gz_member(data, flags=0, extra=b'', name=b'', comment=b''):
    co = zlib.compressobj(9, zlib.DEFLATED, -15)
    deflated = co.compress(data) + co.flush()
    hdr = bytearray(b'\x1f\x8b\x08') + bytes([flags]) + b'\x00\x00\x00\x00\x02\xff'
    if flags & 4:
        hdr += struct.pack('<H', len(extra)) + extra
    if flags & 8:
        hdr += name + b'\x00'
    if flags & 16:
        hdr += comment + b'\x00'
    if flags & 2:
        hdr += struct.pack('<H', zlib.crc32(bytes(hdr)) & 0xffff)
    return hdr + deflated + struct.pack('<II', zlib.crc32(data) & 0xffffffff, len(data) & 0xffffffff)


# ---------------------------------------------------------------- v2 sets

orders = v2_batch(ORDERS, base_offset=0)
put('v2_orders.bin', orders)

put('v2_idempotent.bin', v2_batch(ORDERS[:3], base_offset=5000, pid=4001, epoch=3, seq=2147483646))
put('v2_txn.bin', v2_batch(ORDERS[1:4], base_offset=77, txn=True, pid=9, epoch=0, seq=0))

multi = (v2_batch(ORDERS[:2], base_offset=100)
         + v2_batch(ORDERS[2:5], base_offset=102)
         + v2_batch(ORDERS[5:], base_offset=105))
put('v2_multi.bin', multi)

lat = v2_batch(ORDERS[:4], base_offset=40)
struct.pack_into('>q', lat, 35, T0 + 99000)
put('v2_logappend.bin', set_attrs(lat, 8))

EVENTS = [(T0 + i * 7, b'sensor-%d' % (i % 3),
           b'{"sensor":%d,"reading":%d,"unit":"celsius","status":"ok"}' % (i % 3, 200 + i), [])
          for i in range(24)]
gz = v2_batch(EVENTS, base_offset=300, codec=1)
assert struct.unpack_from('>h', gz, 21)[0] == 1
put('v2_gzip.bin', gz)

# The same records split over two gzip members whose headers carry the
# optional fields, with zero padding after the last.
plain = v2_batch(EVENTS[:10], base_offset=900)
body = bytes(plain[61:])
cut = len(body) // 2
members = (gz_member(body[:cut], flags=4 | 8, extra=b'KF\x02\x00ab', name=b'events.json')
           + gz_member(body[cut:], flags=16 | 2, comment=b'second half') + b'\x00\x00\x00')
put('v2_gzip_members.bin', set_attrs(fix_len(plain[:61] + members), 1))


def gz_variant(name, mutate):
    g = bytearray(gz)
    payload = bytearray(g[61:])
    payload = mutate(payload)
    put(name, set_attrs(fix_len(g[:61] + payload), 1))


def badmagic(p):
    p[0] = 0x78
    p[1] = 0x9c
    return p


def badcrc(p):
    p[-8] ^= 1
    return p


def badisize(p):
    p[-4] ^= 4
    return p


gz_variant('v2_gzip_badmagic.bin', badmagic)
gz_variant('v2_gzip_badcrc.bin', badcrc)
gz_variant('v2_gzip_badsize.bin', badisize)
gz_variant('v2_gzip_cut.bin', lambda p: p[:len(p) // 2])
gz_variant('v2_gzip_junk.bin', lambda p: p + b'\x00\x00K')
gz_variant('v2_gzip_hdrcut.bin', lambda p: p[:7])

ctrl = raw_batch(raw_record(0, 0, struct.pack('>hh', 0, 1), b'\x00\x00\x00\x00\x00\x05', [])
                 + raw_record(3, 1, struct.pack('>hh', 0, 0), b'\x00\x00\x00\x00\x00\x05', []),
                 2, base_offset=80, attrs=32 | 16, first_ts=T0 + 500, max_ts=T0 + 503)
put('v2_control.bin', ctrl)

c = bytearray(orders)
c[120] ^= 0x20
put('v2_badcrc.bin', c)

c = bytearray(orders)
struct.pack_into('>i', c, 57, 6)
put('v2_extra.bin', fix_crc(c))

c = bytearray(orders)
struct.pack_into('>i', c, 57, 8)
put('v2_short_count.bin', fix_crc(c))

recs = (raw_record(0, 0, b'a', b'one', [(b'k', b'v')])
        + raw_record(1, 1, b'b', b'two', [(b'k', b'v')], length_adj=1))
put('v2_badlen.bin', raw_batch(recs, 2))
put('v2_neg_headers.bin', raw_batch(raw_record(0, 0, b'a', b'x', [], hcount=-1), 1))
put('v2_neg_hkey.bin', raw_batch(raw_record(0, 0, b'a', b'x', [(-2, b'v')]), 1))
big = raw_record(0, 0, b'a', b'x', [])
big = big[:1] + b'\x00' + b'\xff' * 10 + big[3:]
put('v2_varint.bin', raw_batch(big, 1))

for codec, name in ((2, 'snappy'), (3, 'lz4'), (4, 'zstd'), (6, 'codec6')):
    put('v2_%s.bin' % name, set_attrs(bytearray(orders), codec))

c = bytearray(orders[:40])
struct.pack_into('>i', c, 8, 28)
put('v2_cut_header.bin', c)
put('tiny.bin', struct.pack('>qi', 7, 8) + b'\x00' * 8)

# ---------------------------------------------------------------- v0 / v1

LEG = [(T0, b'k1', b'first'), (T0 + 5, None, b'second'), (T0 + 9, b'k3', None),
       (T0 + 9, b'', b''), (T0 + 30, b'k5', b'caf\xc3\xa9 \x00\xff')]
put('v0_plain.bin', legacy_set(0, [(None, k, v) for _, k, v in LEG], offset=10))
put('v1_plain.bin', legacy_set(1, LEG, offset=20))

LOGS = [(T0 + i, b'host-%d' % (i % 2), b'GET /api/v1/items/%d 200 12ms' % (i * 13)) for i in range(12)]
put('v1_gzip.bin', legacy_set(1, LOGS, codec=1))
v1g = legacy_set(1, LOGS[:6], codec=1)
struct.pack_into('>q', v1g, 0, 555)
put('v1_gzip_offsets.bin', v1g)
v1lat = bytearray(v1g)
v1lat[17] |= 8
struct.pack_into('>q', v1lat, 18, T0 + 77777)
put('v1_gzip_logappend.bin', legacy_crc(v1lat))
put('v0_gzip.bin', legacy_set(0, [(None, k, v) for _, k, v in LOGS[:5]], codec=1, offset=60))

c = legacy_set(1, LEG[:3], offset=20)
c[40] ^= 1
put('v1_badcrc.bin', c)

put('v1_nullwrap.bin', legacy_msg(1, 9, T0, None, None, attrs=1))

inner = legacy_msg(1, 0, T0, b'k', b'v', attrs=1) + legacy_msg(1, 1, T0, b'k', b'w')
put('v1_double.bin', legacy_msg(1, 1, T0, None, gzip0(bytes(inner)), attrs=1))

inner = legacy_msg(1, 0, T0, b'k', b'v') + legacy_msg(1, 1, T0, b'k', b'w')[:20]
put('v1_inner_cut.bin', legacy_msg(1, 1, T0, None, gzip0(bytes(inner)), attrs=1))

put('v1_snappy.bin', legacy_msg(1, 3, T0, None, b'\x82SNAPPY\x00', attrs=2))
put('v0_lz4.bin', legacy_msg(0, 3, None, None, b'\x04"M\x18', attrs=3))

mixed = (legacy_msg(0, 0, None, b'a', b'v0 message')
         + legacy_msg(1, 1, T0, b'b', b'v1 message')
         + v2_batch(ORDERS[:2], base_offset=2)
         + legacy_set(1, LOGS[:3], codec=1))
nxt = v2_batch(ORDERS[2:6], base_offset=7)
put('mixed.bin', mixed + nxt[:45])
put('trailing.bin', v2_batch(ORDERS[:1], base_offset=0) + b'\x00\x00\x00\x00\x00')

# ------------------------------------------------------- response streams


def frame(corr, resp):
    # Struct.encode holds its instance through a weak reference, so the
    # header must stay bound while it encodes.
    header = ResponseHeader(corr)
    msg = header.encode() + resp.encode()
    return Int32.encode(len(msg)) + msg


MR = metadata.MetadataResponse
meta1 = MR[1](
    [(1, 'kafka-1.internal', 9092, 'us-east-1a'), (2, 'kafka-2.internal', 9092, None),
     (3, 'kafka-3.internal', 9093, 'us-east-1c')],
    2,
    [(0, 'orders', False, [(0, 0, 1, [1, 2, 3], [1, 2, 3]), (0, 1, 2, [2, 3, 1], [2, 3]),
                           (9, 2, -1, [3, 1, 2], [])]),
     (3, 'payments', False, []),
     (0, '__consumer_offsets', True, [(0, 0, 3, [3], [3])])])
meta0 = MR[0](
    [(1, 'localhost', 9092)],
    [(5, 'new-topic', [])])
meta5 = MR[5](
    0,
    [(1, 'kafka-1.internal', 9092, None)],
    'Xj2QnW8yTs-k5G3b9uV7Lw',
    1,
    [(0, 'audit', False, [(0, 0, 1, [1, 2], [1], [2])])])
api0 = api_versions.ApiVersionsResponse[0](0, [(0, 0, 8), (1, 0, 11), (3, 0, 12), (18, 0, 3)])
api3_ok = api_versions.ApiVersionsResponse[3](0, [(0, 0, 9, {}), (3, 0, 12, {}), (18, 0, 3, {})], 0, {})
api_err = api_versions.ApiVersionsResponse[0](35, [(18, 0, 2)])
prod3 = produce.ProduceResponse[3]([('orders', [(0, 0, 1042, -1), (1, 6, -1, -1)])], 15)
prod8 = produce.ProduceResponse[8](
    [('orders', [(0, 10, -1, -1, 0), (1, 0, 57, 1761300000123, 12)])], 0)
fc0 = find_coordinator.FindCoordinatorResponse[0](0, 2, 'kafka-2.internal', 9092)
fc1 = find_coordinator.FindCoordinatorResponse[1](0, 15, 'The coordinator is not available.', -1, '', -1)
fetch4 = fetch.FetchResponse[4](
    0,
    [('orders', [(0, 0, 7, 7, [], bytes(orders)),
                 (1, 0, 300, 300, [(9, 77)], bytes(gz) + bytes(nxt[:30])),
                 (2, 1, -1, -1, None, b'')])])
fetch0 = fetch.FetchResponse[0]([('logs', [(0, 0, 3, bytes(legacy_set(1, LOGS[:3])))])])

put('resp_meta.bin', frame(1, meta1) + frame(2, api0))
put('resp_mixed.bin', frame(1, meta0) + frame(2, meta5) + frame(3, fc0))
put('resp_api3.bin', frame(1, api3_ok) + frame(2, api_err))
put('resp_produce.bin', frame(4, prod3) + frame(5, prod8))
put('resp_fetch.bin', frame(1, fetch4) + frame(2, fetch0))
put('resp_wrong_corr.bin', frame(9, meta0) + frame(2, api0))
put('resp_unsolicited.bin', frame(1, api0) + frame(2, api0))
short_meta = frame(1, meta1)
short_meta = Int32.encode(40) + short_meta[4:44]
put('resp_short.bin', short_meta + frame(2, api0))
put('resp_fc_quirk.bin', frame(0, fc0))
put('resp_fc1.bin', frame(1, fc1))
bad_utf8 = bytearray(frame(1, meta0))
bad_utf8[22] = 0xff
put('resp_badutf8.bin', bad_utf8)
put('resp_varint.bin', Int32.encode(11) + struct.pack('>ih', 1, 0) + b'\x80\x80\x80\x80\x80')
put('resp_cut.bin', Int32.encode(9) + struct.pack('>ih', 1, 0) + b'\x80\x80\x80')

# ---------------------------------------------------------- build inputs


def tok(b):
    if b is None:
        return '~'
    if b == b'':
        return '.'
    out = []
    for x in b:
        c = chr(x)
        if c.isascii() and (c.isalnum() or c in '_-'):
            out.append(c)
        else:
            out.append('%%%02X' % x)
    return ''.join(out)


def rec_line(ts, k, v, h):
    hs = '!' if not h else ';'.join(tok(hk.encode()) + ':' + tok(hv) for hk, hv in h)
    return '%s %s %s %s' % ('~' if ts is None else ts, tok(k), tok(v), hs)


SETS = {
    'orders': ORDERS,
    'events': EVENTS[:8],
    'legacy': [(ts, k, v, []) for ts, k, v in LEG],
    'v0': [(None, k, v, []) for _, k, v in LEG],
    'big': [(T0 + i, b'k%d' % i, bytes([65 + i % 26]) * (40 + 13 * i), [('n', b'%d' % i)]) for i in range(9)],
    'bigleg': [(T0 + i, b'k%d' % i, bytes([65 + i % 26]) * (40 + 13 * i), []) for i in range(9)],
    'far': [(T0, b'a', b'now', []), (0, b'b', b'epoch', []), (T0 + 40000000000, b'c', b'later', []),
            (-1, b'd', b'neg', [])],
    'hdr': [(T0, b'a', b'x', [('h', b'1')])],
}
lines = []
for name, recs in SETS.items():
    lines.append('set ' + name)
    for r in recs:
        lines.append(rec_line(*r))
    lines.append('')
with open(os.path.join(DATA, 'recsets.txt'), 'w') as f:
    f.write('\n'.join(lines))
files.append('recsets.txt')

# ------------------------------------------------------------------- jobs

jobs = []
for name in files:
    if name.endswith('.bin') and not name.startswith('resp_'):
        jobs.append('read ' + name)

# build <set> <magic> <codec> <batch_size> <offset> <txn> <pid> <epoch> <seq>
jobs += [
    'build orders 2 0 16384 0 0 -1 -1 -1',
    'build orders 2 0 200 0 0 -1 -1 -1',
    'build events 2 0 16384 1000 0 4001 3 2147483645',
    'build events 2 0 16384 0 1 77 1 0',
    'build big 2 0 300 0 0 -1 -1 -1',
    'build far 2 0 16384 0 0 -1 -1 -1',
    'build legacy 1 0 16384 0 0 -1 -1 -1',
    'build legacy 1 0 120 5 0 -1 -1 -1',
    'build v0 0 0 16384 0 0 -1 -1 -1',
    'build bigleg 0 0 300 0 0 -1 -1 -1',
    'build hdr 1 0 16384 0 0 -1 -1 -1',
    'build events 2 2 16384 0 0 -1 -1 -1',
    'build events 2 3 16384 0 0 -1 -1 -1',
    'build legacy 1 2 16384 0 0 -1 -1 -1',
    'build events 2 0 16384 0 1 -1 -1 -1',
    'build events 2 0 16384 0 0 5 -1 -1',
    'build events 2 0 16384 0 0 5 1 -1',
    'build legacy 1 0 16384 0 0 5 1 1',
    'build legacy 3 0 16384 0 0 -1 -1 -1',
    'build legacy 1 7 16384 0 0 -1 -1 -1',
]

keys = ['~', '.', 'a', 'ab', 'abc', 'abcd', 'abcde', '21', 'user-17', 'user-3', 'caf%C3%A9-9',
        'order-1042', 'order-1043', '%00', '%FF%FF%FF%FF', '%80%81%82', 'the-quick-brown-fox',
        'sensor-0', 'sensor-1', 'sensor-2', 'tenant_42%2Finvoices']
jobs.append('partition 12 ' + ' '.join(keys[1:]))
jobs.append('partition 1 a b c')
jobs.append('partition 7 ' + ' '.join(keys[1:12]))
jobs.append('errors 0 1 2 3 5 6 7 15 25 35 41 47 58 72 74 87 102 127 128 -1 -7')

jobs += [
    'session ~ ~',
    '  send Metadata 1 ([\'orders\', \'payments\'],)',
    '  send ApiVersions 0 ()',
    '  flush',
    '  recv resp_meta.bin 7',
    'end',
    'session inventory-svc ~',
    '  send Metadata 0 ([\'new-topic\'],)',
    '  send Metadata 5 ([\'audit\'], True)',
    '  send FindCoordinator 0 (\'billing-workers\',)',
    '  flush',
    '  recv resp_mixed.bin 0',
    'end',
    'session cli-7 ~',
    '  send ApiVersions 3 (\'kafka-python\', \'2.2.15\', {})',
    '  send ApiVersions 3 (\'mini-kafka\', None, {1: b\'ab\'})',
    '  flush',
    '  recv resp_api3.bin 1',
    'end',
    'session producer-1 ~',
    '  send Produce 0 (0, 1000, [(\'orders\', [(0, b\'@v2_orders.bin\')])])',
    '  corr 4',
    '  send Produce 3 (None, -1, 30000, [(\'orders\', [(0, b\'@v2_idempotent.bin\'), (1, b\'@v1_plain.bin\')])])',
    '  corr 5',
    '  send Produce 8 (\'txn-1\', 1, 30000, [(\'orders\', [(0, b\'@v2_txn.bin\')])])',
    '  flush',
    '  recv resp_produce.bin 13',
    'end',
    'session consumer-1 ~',
    '  send Fetch 4 (-1, 500, 1, 52428800, 1, [(\'orders\', [(0, 0, 1048576), (1, 300, 1048576), (2, 0, 1048576)])])',
    '  send Fetch 0 (-1, 100, 1, [(\'logs\', [(0, 0, 65536)])])',
    '  flush',
    '  recv resp_fetch.bin 64',
    '  consume',
    'end',
    'session c2 ~',
    '  send Metadata 0 ([],)',
    '  send ApiVersions 0 ()',
    '  recv resp_wrong_corr.bin 0',
    '  recv resp_wrong_corr.bin 0',
    'end',
    'session c3 ~',
    '  send ApiVersions 0 ()',
    '  recv resp_unsolicited.bin 5',
    'end',
    'session c4 ~',
    '  send Metadata 1 (None,)',
    '  send ApiVersions 0 ()',
    '  recv resp_short.bin 0',
    '  send ApiVersions 0 ()',
    '  recv resp_meta.bin 0',
    'end',
    'session c5 ~',
    '  corr 6',
    '  send FindCoordinator 0 (\'g\',)',
    '  recv resp_fc_quirk.bin 0',
    'end',
    'session c6 0.10.0',
    '  corr 6',
    '  send FindCoordinator 0 (\'g\',)',
    '  recv resp_fc_quirk.bin 0',
    'end',
    'session c7 ~',
    '  send Metadata 0 ([\'x\'],)',
    '  recv resp_badutf8.bin 0',
    'end',
    'session c9 ~',
    '  send ApiVersions 3 (\'a\', \'b\', {})',
    '  recv resp_varint.bin 0',
    'end',
    'session c11 ~',
    '  send ApiVersions 3 (\'a\', \'b\', {})',
    '  recv resp_cut.bin 0',
    'end',
    'session billing ~',
    '  send FindCoordinator 1 (\'billing-workers\', 0)',
    '  flush',
    '  recv resp_fc1.bin 3',
    'end',
    'session c8 ~',
    '  send Metadata 1 ([\'a\'], 5)',
    '  send Metadata 1 ([(\'a\', 1)],)',
    '  send FindCoordinator 1 (\'g\', 0)',
    '  send ApiVersions 3 (\'a\', \'b\', {0: b\'x\'})',
    '  flush',
    'end',
]
with open(os.path.join(DATA, 'jobs.txt'), 'w') as f:
    f.write('\n'.join(jobs) + '\n')
with open(os.path.join(DATA, 'files.txt'), 'w') as f:
    f.write('\n'.join(files) + '\n')
print('%d files, %d job lines' % (len(files), len(jobs)))
