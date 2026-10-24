# Runs data/jobs.txt on the vendored kafka-python and prints what each job
# shows. mini_kafka.kara must print the same bytes.
import ast
import logging
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kstub  # noqa: E402

kstub.install()

from kafka.errors import KafkaError, for_code  # noqa: E402
from kafka.partitioner.default import DefaultPartitioner, murmur2  # noqa: E402
from kafka.protocol import api_versions, fetch, find_coordinator, metadata, produce  # noqa: E402
from kafka.protocol.parser import KafkaProtocol  # noqa: E402
from kafka.record.default_records import DefaultRecordBatch, DefaultRecordBatchBuilder  # noqa: E402
from kafka.record.legacy_records import LegacyRecordBatchBuilder  # noqa: E402
from kafka.record.memory_records import MemoryRecords, MemoryRecordsBuilder  # noqa: E402

# The protocol logs a decode failure and the 0.8.2 quirk; the jobs print
# their own account instead.
logging.disable(logging.CRITICAL)

DATA = os.path.join(HERE, 'data')
APIS = {
    'ApiVersions': api_versions.ApiVersionsRequest,
    'Metadata': metadata.MetadataRequest,
    'Produce': produce.ProduceRequest,
    'Fetch': fetch.FetchRequest,
    'FindCoordinator': find_coordinator.FindCoordinatorRequest,
}


def read(name):
    with open(os.path.join(DATA, name), 'rb') as f:
        return f.read()


def fmt(e):
    if isinstance(e, KafkaError):
        return str(e)
    if isinstance(e, struct.error):
        return 'struct.error: %s' % e
    return '%s: %s' % (type(e).__name__, e)


def hexdump(b, ind):
    for i in range(0, len(b), 32):
        print(ind + b[i:i + 32].hex())


def untok(t):
    if t == '~':
        return None
    if t == '.':
        return b''
    out = bytearray()
    i = 0
    while i < len(t):
        if t[i] == '%':
            out.append(int(t[i + 1:i + 3], 16))
            i += 3
        else:
            out.append(ord(t[i]))
            i += 1
    return bytes(out)


def recsets():
    sets = {}
    cur = None
    for line in read('recsets.txt').decode().split('\n'):
        if line.startswith('set '):
            cur = sets.setdefault(line[4:], [])
        elif line:
            ts, k, v, h = line.split(' ')
            hs = []
            if h != '!':
                for kv in h.split(';'):
                    hk, hv = kv.split(':')
                    hs.append((untok(hk).decode(), untok(hv)))
            cur.append((None if ts == '~' else int(ts), untok(k), untok(v), hs))
    return sets


def show_records(buf, ind):
    mr = MemoryRecords(bytes(buf))
    print('%s%d bytes, %d valid' % (ind, mr.size_in_bytes(), mr.valid_bytes()))
    while mr.has_next():
        try:
            b = mr.next_batch()
        except Exception as e:
            print('%serror: %s' % (ind, fmt(e)))
            return
        try:
            if isinstance(b, DefaultRecordBatch):
                print(ind + str(b))
                print('%s  crc=%08x valid=%s size=%d codec=%d timestamp_type=%d control=%s '
                      'leader_epoch=%d last_offset=%d next_offset=%d has_producer_id=%s last_sequence=%d'
                      % (ind, b.crc, b.validate_crc(), b.size_in_bytes, b.compression_type,
                         b.timestamp_type, b.is_control_batch, b.leader_epoch, b.last_offset,
                         b.next_offset, b.has_producer_id(), b.last_sequence))
                for r in b:
                    print('%s  %r size=%d' % (ind, r, r.size_in_bytes))
            else:
                print('%sLegacyRecordBatch(magic=%d, base_offset=%d, size=%d, codec=%d, timestamp_type=%r) valid=%s'
                      % (ind, b.magic, b.base_offset, b.size_in_bytes, b.compression_type,
                         b.timestamp_type, b.validate_crc()))
                for r in b:
                    print('%s  %r valid=%s size=%d' % (ind, r, r.validate_crc(), r.size_in_bytes))
        except Exception as e:
            print('%s  error: %s' % (ind, fmt(e)))


def job_read(name):
    print('> read ' + name)
    show_records(read(name), '  ')


def job_build(args, sets):
    name = args[0]
    magic, codec, bs, off, txn, pid, epoch, seq = [int(x) for x in args[1:]]
    print('> build %s magic=%d codec=%d batch_size=%d offset=%d transactional=%s producer_id=%d '
          'producer_epoch=%d base_sequence=%d' % (name, magic, codec, bs, off, bool(txn), pid, epoch, seq))
    try:
        b = MemoryRecordsBuilder(magic, codec, bs, offset=off, transactional=bool(txn),
                                 producer_id=pid, producer_epoch=epoch, base_sequence=seq)
    except AssertionError as e:
        print('  error: ' + fmt(e))
        return
    for ts, k, v, h in sets[name]:
        try:
            md = b.append(ts, k, v, h)
        except Exception as e:
            print('  error: ' + fmt(e))
            continue
        if magic == 2:
            est = DefaultRecordBatchBuilder.estimate_size_in_bytes(k, v, h)
        else:
            est = LegacyRecordBatchBuilder.estimate_size_in_bytes(magic, codec, k, v)
        print('  %r estimate=%d' % (md, est))
    print('  size=%d full=%s next_offset=%d' % (b.size_in_bytes(), b.is_full(), b.next_offset()))
    try:
        b.close()
    except Exception as e:
        print('  error: ' + fmt(e))
        return
    buf = b.buffer()
    print('  built %d bytes, crc32 %08x' % (len(buf), zlib.crc32(buf)))
    hexdump(buf[:64], '  ')
    show_records(buf, '  ')


def job_partition(args):
    n = int(args[0])
    parts = list(range(n))
    print('> partition %d' % n)
    part = DefaultPartitioner()
    for t in args[1:]:
        k = untok(t)
        print('  %r murmur2=%d partition=%d' % (k, murmur2(k), part(k, parts, parts)))


def job_errors(args):
    print('> errors')
    for c in args:
        cls = for_code(int(c))
        print('  %s -> %s errno=%s message=%s retriable=%s invalid_metadata=%s: %s'
              % (c, cls.__name__, cls.errno, cls.message, cls.retriable, cls.invalid_metadata,
                 cls('details')))


def files_in(v):
    if isinstance(v, bytes) and v.startswith(b'@'):
        return read(v[1:].decode())
    if isinstance(v, tuple):
        return tuple(files_in(x) for x in v)
    if isinstance(v, list):
        return [files_in(x) for x in v]
    return v


def session(head, lines):
    cid = None if head[1] == '~' else head[1]
    av = None if head[2] == '~' else tuple(int(x) for x in head[2].split('.'))
    print('> session client_id=%s api_version=%s' % (head[1], head[2]))
    proto = KafkaProtocol(client_id=cid, api_version=av)
    explicit = None
    keep = []
    last = None
    for line in lines:
        parts = line.split(' ', 3)
        op = parts[0]
        if op == 'corr':
            explicit = int(parts[1])
        elif op == 'send':
            api, ver, lit = parts[1], int(parts[2]), parts[3]
            args = files_in(ast.literal_eval(lit))
            corr, explicit = explicit, None
            try:
                req = APIS[api][ver](*args)
                keep.append(req)
                got = proto.send_request(req, correlation_id=corr)
                print('  send %s correlation_id=%d expect_response=%s'
                      % (type(req).__name__, got, req.expect_response()))
            except Exception as e:
                print('  send %s v%d error: %s' % (api, ver, fmt(e)))
        elif op == 'flush':
            data = proto.send_bytes()
            print('  flush %d bytes, crc32 %08x' % (len(data), zlib.crc32(data)))
            hexdump(data, '    ')
        elif op == 'recv':
            data = read(parts[1])
            size = int(parts[2])
            chunks = [data] if size == 0 else [data[i:i + size] for i in range(0, len(data), size)]
            print('  recv %s: %d bytes in %d chunks' % (parts[1], len(data), len(chunks)))
            for c in chunks:
                try:
                    for corr, r in proto.receive_bytes(c):
                        print('    correlation_id=%d %r' % (corr, r))
                        last = r
                except Exception as e:
                    print('    error: ' + fmt(e))
        elif op == 'consume':
            print('  consume ' + type(last).__name__)
            for t in last.topics:
                for p in t[1]:
                    print('    %s-%d %s highwater=%d' % (t[0], p[0], for_code(p[1]).__name__, p[2]))
                    if p[-1] is None:
                        print('      no records')
                    else:
                        show_records(p[-1], '      ')


def main():
    sets = recsets()
    lines = read('jobs.txt').decode().split('\n')
    i = 0
    while i < len(lines):
        words = lines[i].split(' ')
        i += 1
        if words[0] == 'read':
            job_read(words[1])
        elif words[0] == 'build':
            job_build(words[1:], sets)
        elif words[0] == 'partition':
            job_partition(words[1:])
        elif words[0] == 'errors':
            job_errors(words[1:])
        elif words[0] == 'session':
            body = []
            while lines[i] != 'end':
                body.append(lines[i].strip())
                i += 1
            i += 1
            session(words, body)


main()
