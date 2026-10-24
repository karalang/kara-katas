"""Writes the inputs of mini_pika: data/urls.txt, the broker URLs the
URLParameters job parses, and data/sessions.txt, sixteen AMQP 0-9-1
sessions as a client saw them: its settings, the messages it publishes,
and the bytes the broker sent, as timed segments.

The broker side is encoded here with struct, independently of pika, so
the capture can hold what a broker may send but pika never encodes: every
field-table type, flag words with a continuation bit, bodies split
anywhere, and some damaged frames."""
import random
import struct

rng = random.Random(20261024)

# ------------------------------------------------------------ encoding


def ss(s):
    b = s.encode('utf-8') if isinstance(s, str) else s
    assert len(b) < 256
    return struct.pack('B', len(b)) + b


def ls(s):
    b = s.encode('utf-8') if isinstance(s, str) else s
    return struct.pack('>I', len(b)) + b


def fv(tag, v):
    t = tag.encode()
    if tag == 't':
        return t + struct.pack('B', 1 if v else 0)
    if tag in ('b', 'B'):
        return t + struct.pack('B', v)
    if tag in ('U', 's'):
        return t + struct.pack('>h', v)
    if tag == 'u':
        return t + struct.pack('>H', v)
    if tag == 'I':
        return t + struct.pack('>i', v)
    if tag == 'i':
        return t + struct.pack('>I', v)
    if tag == 'L':
        return t + struct.pack('>q', v)
    if tag in ('l', 'T'):
        return t + struct.pack('>Q', v)
    if tag == 'f':
        return t + struct.pack('>f', v)
    if tag == 'd':
        return t + struct.pack('>d', v)
    if tag == 'D':
        return t + struct.pack('>Bi', v[0], v[1])
    if tag in ('S', 'x'):
        return t + ls(v)
    if tag == 'A':
        body = b''.join(fv(a, b) for a, b in v)
        return t + struct.pack('>I', len(body)) + body
    if tag == 'F':
        return t + table(v)
    if tag == 'V':
        return t
    if tag == 'Z':
        return t + struct.pack('>I', v)
    raise ValueError(tag)


def table(items):
    body = b''.join(ss(k) + fv(t, v) for k, (t, v) in items)
    return struct.pack('>I', len(body)) + body


def frame(kind, ch, payload, end=0xCE):
    return struct.pack('>BHI', kind, ch, len(payload)) + payload + bytes([end])


def method(ch, cls, mid, args=b''):
    return frame(1, ch, struct.pack('>HH', cls, mid) + args)


def heartbeat():
    return frame(8, 0, b'')


def bits(*flags):
    n = 0
    for i, f in enumerate(flags):
        if f:
            n |= 1 << i
    return struct.pack('B', n)


PROP_ORDER = ['content_type', 'content_encoding', 'headers', 'delivery_mode',
              'priority', 'correlation_id', 'reply_to', 'expiration',
              'message_id', 'timestamp', 'type', 'user_id', 'app_id',
              'cluster_id']


def header(ch, size, props, extra_word=False, cls=60):
    flags = 0
    body = b''
    for i, name in enumerate(PROP_ORDER):
        if name not in props:
            continue
        flags |= 1 << (15 - i)
        v = props[name]
        if name == 'headers':
            body += table(v)
        elif name in ('delivery_mode', 'priority'):
            body += struct.pack('B', v)
        elif name == 'timestamp':
            body += struct.pack('>Q', v)
        else:
            body += ss(v)
    if extra_word:
        words = struct.pack('>HH', flags | 1, 0)
    else:
        words = struct.pack('>H', flags)
    return frame(2, ch, struct.pack('>HHQ', cls, 0, size) + words + body)


def bodies(ch, data, sizes):
    out = b''
    pos = 0
    for n in sizes:
        out += frame(3, ch, data[pos:pos + n])
        pos += n
    assert pos == len(data), (pos, len(data))
    return out


def split_body(data, max_len):
    sizes = []
    left = len(data)
    while left > 0:
        sizes.append(min(max_len, left))
        left -= sizes[-1]
    return sizes


# ------------------------------------------------------------ methods

def conn_start(props, mechanisms=b'PLAIN AMQPLAIN', locales=b'en_US',
               major=0, minor=9):
    return method(0, 10, 10, struct.pack('BB', major, minor) + table(props) +
                  ls(mechanisms) + ls(locales))


def conn_tune(channel_max, frame_max, hb):
    return method(0, 10, 30, struct.pack('>HIH', channel_max, frame_max, hb))


def conn_open_ok():
    return method(0, 10, 41, ss(''))


def conn_close(code, text, cls=0, mid=0):
    return method(0, 10, 50, struct.pack('>H', code) + ss(text) +
                  struct.pack('>HH', cls, mid))


def conn_close_ok():
    return method(0, 10, 51)


def conn_blocked(reason):
    return method(0, 10, 60, ss(reason))


def conn_unblocked():
    return method(0, 10, 61)


def chan_open_ok(ch):
    return method(ch, 20, 11, ls(b''))


def chan_flow(ch, active):
    return method(ch, 20, 20, bits(active))


def chan_close(ch, code, text, cls, mid):
    return method(ch, 20, 40, struct.pack('>H', code) + ss(text) +
                  struct.pack('>HH', cls, mid))


def chan_close_ok(ch):
    return method(ch, 20, 41)


def qos_ok(ch):
    return method(ch, 60, 11)


def declare_ok(ch, queue, messages, consumers):
    return method(ch, 50, 11, ss(queue) + struct.pack('>II', messages,
                                                       consumers))


def select_ok(ch):
    return method(ch, 85, 11)


def consume_ok(ch, tag):
    return method(ch, 60, 21, ss(tag))


def cancel(ch, tag, nowait=False):
    return method(ch, 60, 30, ss(tag) + bits(nowait))


def cancel_ok(ch, tag):
    return method(ch, 60, 31, ss(tag))


def deliver(ch, tag, dtag, redelivered, exchange, rkey):
    return method(ch, 60, 60, ss(tag) + struct.pack('>Q', dtag) +
                  bits(redelivered) + ss(exchange) + ss(rkey))


def basic_return(ch, code, text, exchange, rkey):
    return method(ch, 60, 50, struct.pack('>H', code) + ss(text) +
                  ss(exchange) + ss(rkey))


def ack(ch, dtag, multiple=False):
    return method(ch, 60, 80, struct.pack('>Q', dtag) + bits(multiple))


def nack(ch, dtag, multiple=False, requeue=False):
    return method(ch, 60, 120, struct.pack('>Q', dtag) +
                  bits(multiple, requeue))


# ------------------------------------------------------------ sessions

CAPS = [('publisher_confirms', ('t', True)),
        ('exchange_exchange_bindings', ('t', True)),
        ('basic.nack', ('t', True)),
        ('consumer_cancel_notify', ('t', True)),
        ('connection.blocked', ('t', True)),
        ('consumer_priorities', ('t', True)),
        ('authentication_failure_close', ('t', True)),
        ('per_consumer_qos', ('t', True)),
        ('direct_reply_to', ('t', True))]


def server_props(caps=CAPS, version='4.0.5', node='rabbit@mq-01'):
    return [('capabilities', ('F', caps)),
            ('cluster_name', ('S', node)),
            ('copyright', ('S', 'Copyright (c) 2007-2026 the broker authors')),
            ('information', ('S', 'See the broker documentation')),
            ('platform', ('S', 'Erlang/OTP 27.1.2')),
            ('product', ('S', 'RabbitMQ')),
            ('version', ('S', version))]


def text_body(n, words, seed):
    r = random.Random(seed)
    out = []
    size = 0
    while size < n:
        w = r.choice(words)
        out.append(w)
        size += len(w) + 1
    return (' '.join(out))[:n].encode()


class Session:
    def __init__(self, name, url):
        self.name = name
        self.lines = ['session ' + name, 'url ' + url]
        self.now = 0

    def add(self, line):
        self.lines.append(line)

    def recv(self, t, data, cuts=None):
        """The broker's bytes arrive at time t, in one segment or cut at
        the given sizes (the rest in a last segment)."""
        pos = 0
        for i, n in enumerate(cuts or []):
            self.lines.append('recv %d %s' % (t + i, data[pos:pos + n].hex()))
            pos += n
        if pos < len(data):
            self.lines.append('recv %d %s' % (t + len(cuts or []),
                                              data[pos:].hex()))

    def recv_random(self, t, data, lo, hi):
        pos = 0
        k = 0
        while pos < len(data):
            n = rng.randint(lo, hi)
            self.lines.append('recv %d %s' % (t + k, data[pos:pos + n].hex()))
            pos += n
            k += 1

    def end(self, t):
        self.lines.append('end %d' % t)
        return '\n'.join(self.lines)


def client(s, platform='replay', name=None):
    if name:
        s.add('client {platform:"%s",connection_name:"%s"}' % (platform, name))
    else:
        s.add('client {platform:"%s"}' % platform)


def handshake(s, t, ch_max=2047, frame_max=131072, hb=60, caps=CAPS,
              start=None):
    s.recv(t, start or conn_start(server_props(caps)))
    s.recv(t + 15, conn_tune(ch_max, frame_max, hb))
    s.recv(t + 30, conn_open_ok())


def setup(s, t, queue, tag, messages=0):
    """Replies to the client's channel setup: Channel.Open, Basic.Qos,
    Queue.Declare, Confirm.Select and Basic.Consume, each sent only once
    the one before it is answered."""
    s.recv(t, chan_open_ok(1))
    s.recv(t + 5, qos_ok(1))
    s.recv(t + 10, declare_ok(1, queue, messages, 0))
    s.recv(t + 20, select_ok(1))
    s.recv(t + 25, consume_ok(1, tag))


WORDS = ['order', 'invoice', 'shipment', 'pallet', 'carton', 'sku', 'qty',
         'warehouse', 'dock', 'route', 'manifest', 'parcel', 'customer',
         'refund', 'ledger', 'batch', 'priority', 'express', 'ground']


def session_orders():
    s = Session('orders', 'amqp://svc-orders:not-a-real-password@'
                'mq.internal:5672/shop?heartbeat=30&frame_max=8192'
                '&blocked_connection_timeout=10')
    client(s, name='orders-api')
    s.add('queue orders.created prefetch 20 tag orders-worker-1')
    s.add('close_after 5')
    # what the client publishes once its queue is declared
    s.add('pub orders order.created 0')
    s.add('prop content_type application/json')
    s.add('prop delivery_mode 2')
    s.add('prop headers {retries:0,source:"checkout",trace:x0af3c9}')
    s.add('body text {"order": 41017, "total": "129.95", "lines": 3}')
    s.add('pub orders order.created 0')
    s.add('prop content_type application/json')
    s.add('prop message_id ord-41018')
    s.add('prop timestamp 1792841400')
    s.add('body text {"order": 41018, "total": "18.00", "lines": 1}')
    s.add('pub orders order.misrouted 1')
    s.add('prop content_type text/plain')
    s.add('body text nobody is bound to this key')
    s.add('pub orders order.created 0')
    s.add('prop headers {amount:d129.950,when:@1792841460,tags:["vip","eu"],'
          'flags:{gift:T,wrap:F},big:9000000000,neg:-3000000000,none:~}')
    s.add('body text {"order": 41019}')
    s.add('pub orders order.bulk 0')
    s.add('prop content_type application/octet-stream')
    s.add('prop priority 3')
    s.add('body fill 20000 manifest')
    s.add('pub - orders.created 0')
    s.add('body text direct to the queue')

    handshake(s, 15)
    setup(s, 50, 'orders.created', 'orders-worker-1', messages=3)
    t = 80
    hdr1 = [('x-first-seen', ('T', 1792841100)),
            ('x-retries', ('b', 2)),
            ('x-shard', ('B', 0xF6)),
            ('x-score', ('f', 97.75)),
            ('x-ratio', ('d', -12.5)),
            ('x-amount', ('D', (2, 12995))),
            ('x-tiny', ('D', (9, 5))),
            ('x-zero', ('D', (3, 0))),
            ('x-short', ('U', -2)),
            ('x-ushort', ('u', 65000)),
            ('x-sshort', ('s', -300)),
            ('x-long', ('I', -70000)),
            ('x-ulong', ('i', 4000000000)),
            ('x-llong', ('L', -9000000000000)),
            ('x-ullong', ('l', 18000000000000000000)),
            ('x-blob', ('x', b'\x00\x01\xfe\'"\\')),
            ('x-latin1', ('S', b'caf\xe9')),
            ('x-utf8', ('S', 'café → tea')),
            ('x-nothing', ('V', None)),
            ('x-tags', ('A', [('S', 'a'), ('I', 7), ('t', False), ('V', None)])),
            ('x-nested', ('F', [('k', ('S', "it's")), ('q', ('S', 'say "hi"'))])),
            ('x-retries', ('b', 3))]
    m1 = (deliver(1, 'orders-worker-1', 1, False, 'orders', 'order.created') +
          header(1, 46, {'content_type': 'application/json',
                         'headers': hdr1, 'delivery_mode': 2}) +
          bodies(1, b'{"order": 41001, "total": "64.00", "lines": 2}', [46]))
    s.recv(t, m1, cuts=[11, 40, 300])
    props2 = {'content_type': 'text/plain', 'content_encoding': 'gzip',
              'headers': [('x-death', ('A', [('F', [
                  ('count', ('l', 1)), ('reason', ('S', 'expired')),
                  ('queue', ('S', 'orders.retry')),
                  ('time', ('T', 1792841000)), ('exchange', ('S', '')),
                  ('routing-keys', ('A', [('S', 'orders.retry')]))])]))],
              'delivery_mode': 1, 'priority': 9,
              'correlation_id': 'c-77', 'reply_to': 'amq.rabbitmq.reply-to',
              'expiration': '60000', 'message_id': 'm-41002',
              'timestamp': 1792841200, 'type': 'order.created',
              'user_id': 'svc-orders', 'app_id': 'checkout',
              'cluster_id': 'eu-1'}
    body2 = text_body(150, WORDS, 2)
    m2 = (deliver(1, 'orders-worker-1', 2, True, 'orders', 'order.created') +
          header(1, len(body2), props2, extra_word=True) +
          bodies(1, body2, [100, 50]))
    s.recv(t + 5, m2 + ack(1, 2, multiple=True))
    ret = (basic_return(1, 312, 'NO_ROUTE', 'orders', 'order.misrouted') +
           header(1, 27, {'content_type': 'text/plain'}) +
           bodies(1, b'nobody is bound to this key', [27]))
    s.recv(t + 12, ret + ack(1, 3) + nack(1, 4) + ack(1, 6, multiple=True))
    # heartbeats both ways, and a resource alarm
    s.recv(15000, heartbeat())
    s.recv(16000, conn_blocked('low on memory'))
    s.recv(21000, conn_unblocked())
    s.recv(30000, heartbeat())
    # three more deliveries: a poison message, a 20,000-byte one that the
    # broker splits at its frame_max of 8192, and an empty one
    t = 40000
    m3 = (deliver(1, 'orders-worker-1', 3, False, 'orders', 'order.created') +
          header(1, 19, {'content_type': 'text/plain'}) +
          bodies(1, b'poison: bad payload', [19]))
    body4 = text_body(20000, WORDS, 4)
    m4 = (deliver(1, 'orders-worker-1', 4, False, 'orders', 'order.bulk') +
          header(1, len(body4), {'content_type': 'application/octet-stream',
                                 'priority': 3}) +
          bodies(1, body4, split_body(body4, 8184)))
    m5 = (deliver(1, 'orders-worker-1', 5, False, '', 'orders.created') +
          header(1, 0, {}))
    s.recv_random(t, m3 + m4 + m5, 900, 4000)
    # one more delivery in flight while the client is closing
    m6 = (deliver(1, 'orders-worker-1', 6, False, 'orders', 'order.created') +
          header(1, 4, {}) + bodies(1, b'late', [4]))
    s.recv(40100, m6 + cancel_ok(1, 'orders-worker-1'))
    s.recv(40110, chan_close_ok(1))
    s.recv(40120, conn_close_ok())
    return s.end(40200)


def session_ledger():
    s = Session('ledger', 'amqp://ledger-svc:unused@mq.internal/%2Fledger'
                '?heartbeat=0&channel_max=16')
    client(s, name='ledger')
    s.add('credentials external')
    s.add('queue ledger.entries prefetch 1 tag ledger-1')
    start = conn_start(server_props(), mechanisms=b'PLAIN EXTERNAL AMQPLAIN')
    handshake(s, 10, start=start)
    s.recv(50, chan_open_ok(1))
    s.recv(55, qos_ok(1))
    s.recv(60, chan_close(1, 406, "PRECONDITION_FAILED - inequivalent arg "
                          "'durable' for queue 'ledger.entries' in vhost "
                          "'/ledger': received 'true' but current is 'false'",
                          50, 10))
    s.recv(70, conn_close_ok())
    return s.end(100)


def session_bad_password():
    s = Session('bad_password', 'amqp://reporting:wrong-on-purpose@mq.internal/')
    client(s)
    s.add('queue reports prefetch 1 tag reports-1')
    s.recv(10, conn_start(server_props()))
    s.recv(20, conn_close(403, 'ACCESS_REFUSED - Login was refused using '
                          'authentication mechanism PLAIN. For details see '
                          'the broker logfile.'))
    return s.end(30)


def session_vhost_denied():
    s = Session('vhost_denied', 'amqp://billing:unused@mq.internal/billing')
    client(s)
    s.add('queue invoices prefetch 1 tag billing-1')
    s.recv(10, conn_start(server_props()))
    s.recv(20, conn_tune(2047, 131072, 60))
    s.recv(30, conn_close(530, "NOT_ALLOWED - vhost billing not found", 10, 40))
    return s.end(40)


def session_no_plain():
    s = Session('no_plain', 'amqp://mq.internal/')
    client(s)
    s.add('queue jobs prefetch 1 tag jobs-1')
    s.recv(10, conn_start(server_props(), mechanisms=b'AMQPLAIN SCRAM-SHA-256'))
    return s.end(30)


def session_old_broker():
    s = Session('old_broker', 'amqp://mq-legacy.internal/')
    client(s)
    s.add('queue jobs prefetch 1 tag jobs-1')
    s.recv(10, b'AMQP\x01\x01\x08\x00')
    return s.end(20)


def session_version_mismatch():
    s = Session('version_mismatch', 'amqp://mq-legacy.internal/')
    client(s)
    s.add('queue jobs prefetch 1 tag jobs-1')
    s.recv(10, conn_start(server_props(version='1.8.1'), major=8, minor=0))
    return s.end(20)


def session_garbled_start():
    s = Session('garbled_start', 'amqp://mq.internal/')
    client(s)
    s.add('queue jobs prefetch 1 tag jobs-1')
    start = bytearray(conn_start(server_props()))
    start[-1] = 0x00
    s.recv(10, bytes(start), cuts=[100])
    return s.end(20)


def session_heartbeat_lost():
    s = Session('heartbeat_lost', 'amqp://mq.internal/?heartbeat=12')
    client(s, name='metrics')
    s.add('queue metrics prefetch 50 tag metrics-1')
    handshake(s, 10, hb=60)
    setup(s, 50, 'metrics', 'metrics-1')
    m = (deliver(1, 'metrics-1', 1, False, 'metrics', 'cpu') +
         header(1, 9, {'content_type': 'text/plain'}) +
         bodies(1, b'cpu=0.731', [9]))
    s.recv(200, m)
    return s.end(60000)


def session_blocked_too_long():
    s = Session('blocked_too_long', 'amqp://mq.internal/'
                '?blocked_connection_timeout=2.5&heartbeat=0')
    client(s, name='uploader')
    s.add('queue uploads prefetch 5 tag uploads-1')
    s.add('pub uploads upload.done 0')
    s.add('body text done')
    handshake(s, 10, caps=CAPS)
    setup(s, 50, 'uploads', 'uploads-1')
    s.recv(1000, conn_blocked('low on disk'))
    return s.end(10000)


def session_corrupt_frame():
    s = Session('corrupt_frame', 'amqp://mq.internal/?heartbeat=0')
    client(s)
    s.add('queue events prefetch 10 tag events-1')
    handshake(s, 10)
    setup(s, 50, 'events', 'events-1')
    good = (deliver(1, 'events-1', 1, False, 'events', 'user.signup') +
            header(1, 5, {}) + bodies(1, b'hello', [5]))
    bad = bytearray(deliver(1, 'events-1', 2, False, 'events', 'user.signup'))
    bad[-1] = 0xCD
    s.recv(100, good + bytes(bad) + heartbeat())
    return s.end(200)


def session_unknown_method():
    s = Session('unknown_method', 'amqp://mq.internal/?heartbeat=0')
    client(s)
    s.add('queue events prefetch 10 tag events-1')
    handshake(s, 10)
    setup(s, 50, 'events', 'events-1')
    s.recv(100, method(1, 60, 255, b'\x00\x00'))
    return s.end(200)


def session_bad_field():
    s = Session('bad_field', 'amqp://mq.internal/?heartbeat=0')
    client(s)
    s.add('queue events prefetch 10 tag events-1')
    handshake(s, 10)
    setup(s, 50, 'events', 'events-1')
    m = (deliver(1, 'events-1', 1, False, 'events', 'user.signup') +
         header(1, 2, {'headers': [('ok', ('I', 1)), ('odd', ('Z', 7))]}))
    s.recv(100, m)
    return s.end(200)


def session_body_too_long():
    s = Session('body_too_long', 'amqp://mq.internal/?heartbeat=0')
    client(s)
    s.add('queue events prefetch 10 tag events-1')
    handshake(s, 10)
    setup(s, 50, 'events', 'events-1')
    m = (deliver(1, 'events-1', 1, False, 'events', 'user.signup') +
         header(1, 10, {}) + bodies(1, b'abcdefghijkl', [6, 6]))
    s.recv(100, m)
    return s.end(200)


def session_unknown_frame_type():
    s = Session('unknown_frame_type', 'amqp://mq.internal/?heartbeat=0')
    client(s)
    s.add('queue events prefetch 10 tag events-1')
    handshake(s, 10)
    setup(s, 50, 'events', 'events-1')
    s.recv(100, heartbeat() + frame(9, 0, b'\x01\x02'))
    return s.end(200)


def session_no_confirms():
    s = Session('no_confirms', 'amqp://mq.internal/?heartbeat=0')
    client(s)
    s.add('queue events prefetch 10 tag events-1')
    caps = [c for c in CAPS if c[0] != 'publisher_confirms']
    handshake(s, 10, caps=caps)
    s.recv(50, chan_open_ok(1))
    s.recv(55, qos_ok(1))
    return s.end(200)


def session_consumer_cancelled():
    s = Session('consumer_cancelled', 'amqp://mq.internal/?heartbeat=0')
    client(s, name='audit')
    s.add('queue audit prefetch 10 tag audit-1')
    handshake(s, 10)
    setup(s, 50, 'audit', 'audit-1', messages=1)
    m = (deliver(1, 'audit-1', 1, False, 'audit', 'login') +
         header(1, 7, {'type': 'login'}) + bodies(1, b'user=42', [7]))
    s.recv(100, m)
    s.recv(200, cancel(1, 'audit-1'))
    m2 = (deliver(1, 'audit-1', 2, False, 'audit', 'login') +
          header(1, 7, {'type': 'login'}) + bodies(1, b'user=43', [7]))
    s.recv(210, m2 + chan_flow(1, False))
    s.recv(300, conn_close(320, "CONNECTION_FORCED - broker forced connection "
                           "closure with reason 'shutdown'"))
    return s.end(400)


SESSIONS = [session_orders, session_ledger, session_bad_password,
            session_vhost_denied, session_no_plain, session_old_broker,
            session_version_mismatch, session_garbled_start,
            session_heartbeat_lost, session_blocked_too_long,
            session_corrupt_frame, session_unknown_method, session_bad_field,
            session_body_too_long, session_unknown_frame_type,
            session_no_confirms, session_consumer_cancelled]

URLS = [
    'amqp://',
    'amqp://guest:guest@localhost:5672/%2F',
    'amqps://svc-billing:not-a-real-password@mq.example.internal/billing?heartbeat=30',
    'AMQP://Mq-01.Example.Internal:5673/orders?frame_max=8192&channel_max=128',
    'amqp://user%40corp:p%3Aw%2Fd@rabbit/a%2Fb/c',
    'amqp://:only-a-password@rabbit/',
    'amqp://user:@rabbit/',
    'amqp://reader@rabbit/',
    'amqp://rabbit:99999/',
    'amqp://rabbit:56x2/',
    'amqp://rabbit:/vh',
    'amqp://[::1]:5673/',
    'amqp://[::1/',
    'amqpx://rabbit/',
    'localhost:5672',
    'mq.internal:5672/orders',
    'amqp://rabbit/?heartbeat=10&heartbeat=20',
    'amqp://rabbit/?prefetch=10',
    'amqp://rabbit/?heartbeat=-1',
    'amqp://rabbit/?heartbeat=ten',
    'amqp://rabbit/?heartbeat=+30+',
    'amqp://rabbit/?frame_max=1000',
    'amqp://rabbit/?frame_max=200000',
    'amqp://rabbit/?frame_max=4096',
    'amqp://rabbit/?channel_max=0',
    'amqp://rabbit/?channel_max=65536',
    'amqp://rabbit/?channel_max=1_024',
    'amqp://rabbit/?channel_max=0x10',
    'amqp://rabbit/?channel_max=12.0',
    'amqp://rabbit/?connection_attempts=0',
    'amqp://rabbit/?connection_attempts=3&retry_delay=0.25',
    'amqp://rabbit/?retry_delay=soon',
    'amqp://rabbit/?socket_timeout=0',
    'amqp://rabbit/?socket_timeout=1e1&stack_timeout=1_5',
    'amqp://rabbit/?stack_timeout=-2',
    'amqp://rabbit/?blocked_connection_timeout=-1',
    'amqp://rabbit/?blocked_connection_timeout=inf',
    'amqp://rabbit/?blocked_connection_timeout=1__0',
    'amqp://rabbit/?locale=de_DE',
    'amqp://rabbit/?heartbeat=&locale=fr_FR',
    'amqp://rabbit/?heartbeat;locale=fr_FR',
    'amqp://rabbit/?heartbeat=5&&locale=pt%5FBR',
    'amqp://rabbit/vh;v=1?heartbeat=5',
    'amqp://rabbit/one/two',
    'amqp://rabbit//',
    'amqp://rabbit/%E2%9C%93',
    'amqp://rabbit/%ZZ',
    'amqp://rabbit/%C3%28',
    'amqp://rabbit?heartbeat=7',
    'amqp://rabbit#frag?heartbeat=7',
    'amqp://rabbit/?heartbeat=12&socket_timeout=2.5&blocked_connection_timeout=0',
    'amqps://secure.internal:443/',
    'amqp://rabbit/?socket_timeout=.5&stack_timeout=5.',
    'amqp://rabbit/?retry_delay=1e400',
    'amqp://rabbit/?socket_timeout=nan',
    'amqp://rabbit/?heartbeat=%2B7',
]


def main():
    with open('data/urls.txt', 'w') as f:
        for u in URLS:
            f.write(u + '\n')
    with open('data/sessions.txt', 'w') as f:
        for make in SESSIONS:
            f.write(make() + '\n\n')


if __name__ == '__main__':
    main()
