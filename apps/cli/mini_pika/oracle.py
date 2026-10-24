"""Runs mini_pika's two jobs on the vendored pika 1.3.2 and prints what
mini_pika.kara must print: URLParameters over data/urls.txt, then every
session in data/sessions.txt replayed against pika's own Connection and
Channel."""
import datetime
import decimal
import os
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'vendor'))

import pika  # noqa: E402
from pika import connection, credentials, exceptions, frame, spec  # noqa: E402


# ------------------------------------------------------------ literals

class Lit:
    """The value syntax the session file uses for header tables and client
    properties: T F ~ 42 d1.50 @<epoch> "text" x<hex> [a,b] {k:v}."""

    def __init__(self, text):
        self.s = text
        self.i = 0

    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else ''

    def value(self):
        c = self.peek()
        if c == '{':
            self.i += 1
            out = {}
            if self.peek() == '}':
                self.i += 1
                return out
            while True:
                j = self.s.index(':', self.i)
                key = self.s[self.i:j]
                self.i = j + 1
                out[key] = self.value()
                c = self.peek()
                self.i += 1
                if c == '}':
                    return out
        if c == '[':
            self.i += 1
            out = []
            if self.peek() == ']':
                self.i += 1
                return out
            while True:
                out.append(self.value())
                c = self.peek()
                self.i += 1
                if c == ']':
                    return out
        if c == '"':
            j = self.s.index('"', self.i + 1)
            v = self.s[self.i + 1:j]
            self.i = j + 1
            return v
        j = self.i
        while j < len(self.s) and self.s[j] not in ',]}':
            j += 1
        tok = self.s[self.i:j]
        self.i = j
        if tok == 'T':
            return True
        if tok == 'F':
            return False
        if tok == '~':
            return None
        if tok[0] == 'd':
            return decimal.Decimal(tok[1:])
        if tok[0] == '@':
            return (datetime.datetime(1970, 1, 1) +
                    datetime.timedelta(seconds=int(tok[1:])))
        if tok[0] == 'x':
            return bytes.fromhex(tok[1:])
        return int(tok)


def lit(text):
    return Lit(text).value()


# ------------------------------------------------------------ URLs

def show_params(p):
    cred = p.credentials
    if isinstance(cred, credentials.PlainCredentials):
        who = 'user=%r password=%r' % (cred.username, cred.password)
    else:
        who = 'credentials=EXTERNAL'
    return ('host=%r port=%r vhost=%r %s ssl=%r heartbeat=%r frame_max=%r '
            'channel_max=%r locale=%r attempts=%r retry_delay=%r '
            'socket_timeout=%r stack_timeout=%r blocked_timeout=%r' % (
                p.host, p.port, p.virtual_host, who,
                p.ssl_options is not None, p.heartbeat, p.frame_max,
                p.channel_max, p.locale, p.connection_attempts, p.retry_delay,
                p.socket_timeout, p.stack_timeout,
                p.blocked_connection_timeout))


def url_job():
    print('# URLParameters')
    with open(os.path.join(HERE, 'data', 'urls.txt')) as f:
        urls = f.read().splitlines()
    for url in urls:
        print(url)
        try:
            print('  ' + show_params(pika.URLParameters(url)))
        except Exception as e:  # pylint: disable=broad-except
            print('  %s: %s' % (type(e).__name__, e))


# ------------------------------------------------------------ the replay

class Done(Exception):
    pass


class Replay(connection.Connection):
    """A Connection whose transport is the capture: the broker's segments
    are fed to it at their times, timers run on the capture's clock in
    milliseconds, and every frame it sends is decoded back and printed.
    It runs the way pika's external connection workflow runs it."""

    def __init__(self, params, app):
        self.now = 0
        self.timers = {}
        self.timer_seq = 0
        self.dropped = False
        self.tap = [0, 0, 0, 0]  # frames in, bytes in, frames out, bytes out
        self.app = app
        app.conn = self
        super().__init__(params, on_open_callback=app.on_open,
                         on_open_error_callback=app.on_open_error,
                         on_close_callback=app.on_closed,
                         internal_connection_workflow=False)

    def log(self, text):
        print('%7d %s' % (self.now, text))

    # the adapter

    def _adapter_call_later(self, delay, callback):
        self.timer_seq += 1
        self.timers[self.timer_seq] = (self.now + int(round(delay * 1000)),
                                       self.timer_seq, callback)
        return self.timer_seq

    def _adapter_remove_timeout(self, timeout_id):
        self.timers.pop(timeout_id, None)

    def _adapter_add_callback_threadsafe(self, callback):
        raise NotImplementedError

    def _adapter_connect_stream(self):
        pass

    def _adapter_disconnect_stream(self):
        self.dropped = True

    def _adapter_emit_data(self, data):
        self.tap[2] += 1
        self.tap[3] += len(data)
        _, value = frame.decode_frame(data)
        self.log('> ' + show_frame(value, data))

    # the tap on what comes in

    def _process_frame(self, frame_value):
        self.tap[0] += 1
        self.log('< ' + show_frame(frame_value, None))
        super()._process_frame(frame_value)

    def _trim_frame_buffer(self, byte_count):
        self.tap[1] += byte_count
        super()._trim_frame_buffer(byte_count)

    # driving it

    def settle(self):
        """After each event: a transport the connection dropped reports
        its loss."""
        if self.dropped:
            self.dropped = False
            self.log('transport closed')
            self._on_stream_terminated(None)
            raise Done()

    def event(self, fn, *args):
        try:
            fn(*args)
        except Done:
            raise
        except Exception as error:  # pylint: disable=broad-except
            # the transport aborts with the error, as pika's does when
            # data_received() raises
            self.dropped = False
            self.log('transport aborted')
            self._on_stream_terminated(exceptions.StreamLostError(
                'Stream connection lost: {!r}'.format(error)))
            raise Done()
        self.settle()

    def run_timers(self, until):
        while True:
            due = [t for t in self.timers.values() if t[0] <= until]
            if not due:
                break
            at, seq, callback = min(due)
            del self.timers[seq]
            self.now = at
            self.event(callback)
        self.now = until


def show_frame(value, data):
    if isinstance(value, frame.Body):
        frag = value.fragment
        return 'body ch%d %d bytes crc %08x' % (value.channel_number,
                                                 len(frag), zlib.crc32(frag))
    text = repr(value)
    if data is not None:
        text += ' [%d bytes crc %08x]' % (len(data), zlib.crc32(data))
    return text


def preview(body):
    if len(body) <= 40:
        return repr(body)
    return '%r... (%d bytes, crc %08x)' % (body[:40], len(body),
                                           zlib.crc32(body))


class App:
    """The client program: it opens a channel, sets its prefetch, declares
    its queue, turns on publisher confirms, publishes its messages,
    consumes, acks what it gets (nacks a poison message) and closes the
    connection after close_after deliveries."""

    def __init__(self, cfg):
        self.cfg = cfg
        self.conn = None
        self.channel = None
        self.next_tag = 1
        self.unconfirmed = []
        self.delivered = 0

    def log(self, text):
        self.conn.log('app: ' + text)

    def on_open(self, conn):
        sp = conn.server_properties
        self.log('connection open to %s %s, frame_max %d, channel_max %d, '
                 'heartbeat %r' % (sp.get('product'), sp.get('version'),
                                   conn.params.frame_max,
                                   conn.params.channel_max,
                                   conn.params.heartbeat))
        conn.channel(on_open_callback=self.on_channel_open)

    def on_open_error(self, conn, error):
        self.log('could not connect: %r' % (error,))

    def on_closed(self, conn, reason):
        self.log('connection closed: %r' % (reason,))

    def on_blocked(self, conn, method_frame):
        self.log('blocked by the broker: %s' % method_frame.method.reason)

    def on_unblocked(self, conn, method_frame):
        self.log('unblocked')

    def on_channel_open(self, ch):
        self.channel = ch
        self.log('channel %d open' % ch.channel_number)
        ch.add_on_close_callback(self.on_channel_closed)
        ch.add_on_return_callback(self.on_return)
        ch.add_on_cancel_callback(self.on_cancelled)
        ch.basic_qos(prefetch_count=self.cfg['prefetch'])
        ch.queue_declare(self.cfg['queue'], durable=True,
                         callback=self.on_declared)
        ch.confirm_delivery(self.on_confirm, callback=self.on_confirms_on)

    def on_declared(self, method_frame):
        m = method_frame.method
        self.log('queue %s declared: %d messages, %d consumers' % (
            m.queue, m.message_count, m.consumer_count))
        for exchange, key, mandatory, props, body in self.cfg['publish']:
            self.channel.basic_publish(exchange, key, body,
                                       spec.BasicProperties(**props),
                                       mandatory=mandatory)
            self.unconfirmed.append(self.next_tag)
            self.log('published #%d to %r with key %s, %d bytes' % (
                self.next_tag, exchange, key, len(body)))
            self.next_tag += 1
        self.channel.basic_consume(self.cfg['queue'], self.on_message,
                                   consumer_tag=self.cfg['tag'])

    def on_confirms_on(self, method_frame):
        self.log('publisher confirms on')

    def on_confirm(self, method_frame):
        m = method_frame.method
        kind = 'ack' if isinstance(m, spec.Basic.Ack) else 'nack'
        if m.multiple:
            done = [t for t in self.unconfirmed if t <= m.delivery_tag]
        else:
            done = [t for t in self.unconfirmed if t == m.delivery_tag]
        self.unconfirmed = [t for t in self.unconfirmed if t not in done]
        self.log('broker %s for %s; %d unconfirmed' % (
            kind, ', '.join('#%d' % t for t in done) or 'nothing',
            len(self.unconfirmed)))

    def on_message(self, ch, deliver, props, body):
        self.delivered += 1
        self.log('message %d from %r key %s%s: %s' % (
            deliver.delivery_tag, deliver.exchange, deliver.routing_key,
            ' (redelivered)' if deliver.redelivered else '', preview(body)))
        if body.startswith(b'poison'):
            ch.basic_nack(deliver.delivery_tag, requeue=False)
        else:
            ch.basic_ack(deliver.delivery_tag)
        if self.delivered == self.cfg['close_after']:
            self.log('closing after %d messages' % self.delivered)
            self.conn.close()

    def on_return(self, ch, method, props, body):
        self.log('returned by the broker: %d %s, %s/%s: %s' % (
            method.reply_code, method.reply_text, method.exchange,
            method.routing_key, preview(body)))

    def on_cancelled(self, method_frame):
        self.log('consumer %s cancelled by the broker' %
                 method_frame.method.consumer_tag)

    def on_channel_closed(self, ch, reason):
        self.log('channel %d closed: %r' % (ch.channel_number, reason))
        if self.conn.is_open:
            self.conn.close()


# ------------------------------------------------------------ sessions

def body_of(spec_text):
    kind, _, rest = spec_text.partition(' ')
    if kind == 'text':
        return rest.encode('utf-8')
    n, _, word = rest.partition(' ')
    n = int(n)
    out = b''
    k = 0
    while len(out) < n:
        k += 1
        out += ('%s-%d ' % (word, k)).encode()
    return out[:n]


INT_PROPS = ('delivery_mode', 'priority', 'timestamp')


def parse_sessions():
    with open(os.path.join(HERE, 'data', 'sessions.txt')) as f:
        lines = f.read().splitlines()
    sessions = []
    cur = None
    for line in lines:
        if not line:
            continue
        word, _, rest = line.partition(' ')
        if word == 'session':
            cur = {'name': rest, 'client': None, 'external': False,
                   'close_after': 0, 'publish': [], 'recv': [], 'end': 0}
            sessions.append(cur)
        elif word == 'url':
            cur['url'] = rest
        elif word == 'client':
            cur['client'] = lit(rest)
        elif word == 'credentials':
            cur['external'] = rest == 'external'
        elif word == 'queue':
            parts = rest.split(' ')
            cur['queue'] = parts[0]
            cur['prefetch'] = int(parts[2])
            cur['tag'] = parts[4]
        elif word == 'close_after':
            cur['close_after'] = int(rest)
        elif word == 'pub':
            ex, key, mand = rest.split(' ')
            cur['publish'].append([
                '' if ex == '-' else ex, key, mand == '1', {}, b''])
        elif word == 'prop':
            name, _, value = rest.partition(' ')
            props = cur['publish'][-1][3]
            if name == 'headers':
                props[name] = lit(value)
            elif name in INT_PROPS:
                props[name] = int(value)
            else:
                props[name] = value
        elif word == 'body':
            cur['publish'][-1][4] = body_of(rest)
        elif word == 'recv':
            t, data = rest.split(' ')
            cur['recv'].append((int(t), bytes.fromhex(data)))
        elif word == 'end':
            cur['end'] = int(rest)
    return sessions


def replay(cfg):
    print()
    print('== %s: %s' % (cfg['name'], cfg['url']))
    params = pika.URLParameters(cfg['url'])
    params.client_properties = cfg['client']
    if cfg['external']:
        params.credentials = credentials.ExternalCredentials()
    app = App(cfg)
    conn = Replay(params, app)
    conn.add_on_connection_blocked_callback(app.on_blocked)
    conn.add_on_connection_unblocked_callback(app.on_unblocked)
    try:
        conn.event(conn._on_stream_connected)  # pylint: disable=W0212
        for at, data in cfg['recv']:
            conn.run_timers(at)
            conn.event(conn._on_data_available, data)  # pylint: disable=W0212
        conn.run_timers(cfg['end'])
        conn.log('end of capture')
        conn._on_stream_terminated(  # pylint: disable=W0212
            exceptions.StreamLostError('Transport indicated EOF'))
    except Done:
        pass
    t = conn.tap
    print('  received %d frames, %d bytes; sent %d frames, %d bytes; '
          'delivered %d, unconfirmed %s' % (
              t[0], t[1], t[2], t[3], app.delivered,
              ' '.join('#%d' % n for n in app.unconfirmed) or 'none'))


def main():
    url_job()
    print()
    print('# sessions')
    for cfg in parse_sessions():
        replay(cfg)


if __name__ == '__main__':
    main()
