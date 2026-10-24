# Runs data/jobs.txt and the dump and import programs on the vendored bson
# and prints the results. Run as: python3 -I -B oracle.py > expected.out
import datetime
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'vendor'))
import bson  # noqa: E402
from bson import json_util  # noqa: E402
from bson.binary import UuidRepresentation  # noqa: E402
from bson.codec_options import CodecOptions, DatetimeConversion  # noqa: E402
from bson.decimal128 import Decimal128  # noqa: E402
from bson.objectid import ObjectId  # noqa: E402

D = os.path.join(HERE, 'data')
MODES = [('canonical', json_util.CANONICAL_JSON_OPTIONS),
         ('relaxed', json_util.RELAXED_JSON_OPTIONS),
         ('legacy', json_util.LEGACY_JSON_OPTIONS)]


def err(e):
    return '%s: %s' % (type(e).__name__, e)


def show_dumps(obj, modes=MODES):
    for name, opts in modes:
        try:
            print('  %s: %s' % (name, json_util.dumps(obj, json_options=opts)))
        except Exception as e:
            print('  %s: %s' % (name, err(e)))


def show_repr(d):
    try:
        print('  repr: %r' % (d,))
    except Exception as e:
        print('  repr: ' + err(e))


def show_doc(d, modes=MODES):
    show_repr(d)
    show_dumps(d, modes)


def run_json(arg, check_keys=False):
    try:
        d = json_util.loads(arg)
    except Exception as e:
        print('  loads: ' + err(e))
        return
    show_repr(d)
    try:
        b = bson.encode(d, check_keys=check_keys)
    except Exception as e:
        print('  encode: ' + err(e))
        return
    print('  bson: ' + b.hex())
    if check_keys:
        return
    try:
        back = bson.decode(b)
    except Exception as e:
        print('  decode: ' + err(e))
        return
    show_dumps(back)


def run_hex(arg, opts=None):
    data = bytes.fromhex(arg)
    try:
        d = bson.decode(data, codec_options=opts) if opts else bson.decode(data)
    except Exception as e:
        print('  decode: ' + err(e))
    else:
        show_doc(d, MODES if opts is None else MODES[1:2])
    if opts is None:
        print('  valid: %s' % bson.is_valid(data))


OPTS = {
    'datetime=auto': CodecOptions(datetime_conversion=DatetimeConversion.DATETIME_AUTO),
    'datetime=clamp': CodecOptions(datetime_conversion=DatetimeConversion.DATETIME_CLAMP),
    'datetime=ms': CodecOptions(datetime_conversion=DatetimeConversion.DATETIME_MS),
    'uuid=standard': CodecOptions(uuid_representation=UuidRepresentation.STANDARD),
    'uuid=pythonLegacy': CodecOptions(uuid_representation=UuidRepresentation.PYTHON_LEGACY),
    'uuid=javaLegacy': CodecOptions(uuid_representation=UuidRepresentation.JAVA_LEGACY),
    'uuid=csharpLegacy': CodecOptions(uuid_representation=UuidRepresentation.CSHARP_LEGACY),
}


def run_all(arg):
    data = bytes.fromhex(arg)
    try:
        docs = bson.decode_all(data)
        print('  decode_all: %d' % len(docs))
        for d in docs:
            print('    ' + json_util.dumps(d, json_options=json_util.CANONICAL_JSON_OPTIONS))
    except Exception as e:
        print('  decode_all: ' + err(e))
    n = 0
    try:
        for d in bson.decode_iter(data):
            n += 1
            print('  iter %d: %s' % (n, json_util.dumps(d)))
        print('  decode_iter: %d' % n)
    except Exception as e:
        print('  decode_iter after %d: %s' % (n, err(e)))
    print('  valid: %s' % bson.is_valid(data))


def run_oid(arg):
    print('  is_valid: %s' % ObjectId.is_valid(arg))
    try:
        o = ObjectId(arg)
    except Exception as e:
        print('  ' + err(e))
        return
    print('  str: %s' % o)
    print('  repr: %r' % (o,))
    print('  binary: %s' % o.binary.hex())
    print('  generated: %s' % o.generation_time.isoformat())


def run_oidtime(arg):
    dt = json_util.loads('{"$date": "%s"}' % arg)
    try:
        o = ObjectId.from_datetime(dt)
    except Exception as e:
        print('  ' + err(e))
        return
    print('  oid: %s' % o)
    print('  generated: %s' % o.generation_time.isoformat())
    print('  before: %s' % (o < ObjectId('5f2b3c4d5e6f708192a3b4c5')))


def run_dec(arg):
    try:
        d = Decimal128(arg)
    except Exception as e:
        print('  ' + err(e))
        return
    print('  bid: %s' % d.bid.hex())
    print('  str: %s' % d)
    print('  repr: %r' % (d,))
    print('  to_decimal: %s' % d.to_decimal())


def run_bid(arg):
    d = Decimal128.from_bid(bytes.fromhex(arg))
    try:
        print('  str: %s' % d)
    except Exception as e:
        print('  str: ' + err(e))
    try:
        print('  to_decimal: %s' % d.to_decimal())
    except Exception as e:
        print('  to_decimal: ' + err(e))


def dump(path):
    # bsondump: one relaxed Extended JSON line per document
    with open(os.path.join(D, path), 'rb') as f:
        data = f.read()
    print('== bsondump %s (%d bytes)' % (path, len(data)))
    n = 0
    try:
        for d in bson.decode_iter(data):
            n += 1
            print(json_util.dumps(d))
    except Exception as e:
        print('error: ' + err(e))
    print('%d objects found' % n)


def import_jsonl(path):
    # mongoimport: each line of Extended JSON becomes a BSON document; the
    # documents that load are written out and read back
    with open(os.path.join(D, path), encoding='utf-8') as f:
        lines = f.read().split('\n')
    print('== import %s' % path)
    out = b''
    good = 0
    bad = 0
    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            out += bson.encode(json_util.loads(line))
            good += 1
        except Exception as e:
            bad += 1
            print('line %d: %s' % (i, err(e)))
    name = 'mini_bson_import.bson'
    with open(name, 'wb') as f:
        f.write(out)
    with open(name, 'rb') as f:
        back = bson.decode_all(f.read())
    os.remove(name)
    print('imported %d, failed %d, %d bytes' % (good, bad, len(out)))
    for d in back:
        print(json_util.dumps(d, json_options=json_util.CANONICAL_JSON_OPTIONS))


def main():
    with open(os.path.join(D, 'jobs.txt'), encoding='utf-8') as f:
        jobs = [ln for ln in f.read().split('\n') if ln]
    for ln in jobs:
        kind, arg = ln.split('\t', 1)
        print('== %s %s' % (kind, arg))
        if kind == 'json':
            run_json(arg)
        elif kind == 'keys':
            run_json(arg, check_keys=True)
        elif kind == 'hex':
            run_hex(arg)
        elif kind == 'opts':
            name, h = arg.split(' ')
            run_hex(h, OPTS[name])
        elif kind == 'all':
            run_all(arg)
        elif kind == 'oid':
            run_oid(arg)
        elif kind == 'oidtime':
            run_oidtime(arg)
        elif kind == 'dec':
            run_dec(arg)
        elif kind == 'bid':
            run_bid(arg)
    with open(os.path.join(D, 'files.txt'), encoding='utf-8') as f:
        for path in f.read().split('\n'):
            if path.endswith('.bson'):
                dump(path)
            elif path.endswith('.jsonl'):
                import_jsonl(path)


if __name__ == '__main__':
    main()
