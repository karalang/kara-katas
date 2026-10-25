"""Play data/jobs.txt through the vendored simplefix 1.0.17 and print what each
step returned or raised. Its output is expected.out.

The trading venue (sessions, sequence numbers, resends, heartbeats, the order
book) is this app's own code, the same here as in mini_simplefix.kara;
simplefix builds, encodes and parses every message on the wire.

Run: python3 -I -B oracle.py > expected.out"""
import datetime
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))

import simplefix  # noqa: E402
from simplefix import errors  # noqa: E402

SOH = b"\x01"


def unesc(text):
    out = []
    i = 0
    while i < len(text):
        if text[i] == "~":
            out.append(int(text[i + 1:i + 3], 16))
            i += 3
        else:
            out.append(ord(text[i]))
            i += 1
    return out


def value(tok):
    if tok == "-":
        return None
    if tok.startswith("b:"):
        return bytes(unesc(tok[2:]))
    if tok.startswith("s:"):
        return "".join(chr(c) for c in unesc(tok[2:]))
    if tok.startswith("i:"):
        return int(tok[2:])
    raise ValueError("bad value " + tok)


def when(tok):
    if tok.startswith("D:"):
        return datetime.datetime.strptime(tok[2:], "%Y-%m-%dT%H:%M:%S.%f")
    return float(tok[2:])


def err(e):
    msg = str(e)
    if msg:
        return "! %s: %s" % (type(e).__name__, msg)
    return "! %s" % type(e).__name__


def fnv(data):
    h = 2166136261
    for c in data:
        h = ((h ^ c) * 16777619) & 0xFFFFFFFF
    return h


def shown(m):
    if m is None:
        return "None"
    try:
        return m.to_string("|")
    except UnicodeDecodeError as e:
        return err(e)


def pretty(raw):
    return repr(simplefix.pretty_print(raw))


# ---------------------------------------------------------------- the venue

HB = 30
SYMBOLS = ["IBM", "MSFT"]
SESSION_TYPES = [b"A", b"0", b"1", b"2", b"4", b"5"]
BASE = datetime.datetime(2026, 10, 23, 13, 30, 0)


def cents(text):
    """A price with up to two decimals, in cents, or None."""
    if text is None:
        return None
    t = text.decode("latin-1")
    whole, _, frac = t.partition(".")
    if not whole.isdigit() or not whole.isascii() or len(frac) > 2 or (frac and not (frac.isdigit() and frac.isascii())):
        return None
    return int(whole) * 100 + int((frac + "00")[:2])


def px(c):
    return "%d.%02d" % (c // 100, c % 100)


def avg_px(value, qty):
    if qty == 0:
        return "0"
    v = value * 100 // qty
    return "%d.%04d" % (v // 10000, v % 10000)


class Session:
    def __init__(self, me, them):
        self.me = me
        self.them = them
        self.out_seq = 1
        self.in_seq = 1
        self.sent = {}
        self.up = False
        self.last_tx = 0
        self.last_rx = 0
        self.test_out = None
        self.test_at = 0
        self.tests = 0
        self.resend_pending = False
        self.parser = simplefix.FixParser()
        self.n_tx = 0
        self.n_rx = 0
        self.gaps = 0
        self.resends = 0
        self.dups = 0
        self.garbled = 0
        self.ignored = 0


class Link:
    def __init__(self):
        self.drop = 0
        self.cut = False
        self.garble = False
        self.chunk = 0


class Order:
    pass


class Venue:
    def __init__(self):
        self.clock = 0
        self.sessions = []
        self.links = {}
        for c in ("CLIENT1", "CLIENT2"):
            self.sessions.append(Session(c, "BROKER"))
            self.sessions.append(Session("BROKER", c))
            self.links[(c, "BROKER")] = Link()
            self.links[("BROKER", c)] = Link()
        self.queue = []
        self.log = []
        self.orders = []
        self.book = {s: [] for s in SYMBOLS}
        self.next_order = 1
        self.next_exec = 1
        self.arrivals = 0
        self.views = {"CLIENT1": [], "CLIENT2": []}
        self.placed = {"CLIENT1": [], "CLIENT2": []}

    def sess(self, me, them):
        for s in self.sessions:
            if s.me == me and s.them == them:
                return s
        raise KeyError(me + them)

    def stamp(self):
        return BASE + datetime.timedelta(milliseconds=self.clock)

    # ---- sending

    def build(self, s, mtype, fields, seq, poss_dup, orig):
        m = simplefix.FixMessage()
        m.append_pair(8, "FIX.4.4")
        m.append_pair(35, mtype)
        m.append_pair(49, s.me, header=True)
        m.append_pair(56, s.them, header=True)
        m.append_pair(34, seq, header=True)
        if poss_dup:
            m.append_pair(43, "Y", header=True)
            m.append_pair(122, orig, header=True)
        m.append_utc_timestamp(52, self.stamp(), precision=3, header=True)
        for t, v in fields:
            m.append_pair(t, v)
        return m

    def send(self, me, them, mtype, fields):
        s = self.sess(me, them)
        self.clock += 1
        seq = s.out_seq
        s.out_seq += 1
        m = self.build(s, mtype, fields, seq, False, None)
        s.sent[seq] = (mtype, fields, m.get(52).decode())
        self.transmit(s, m)

    def resend(self, s, seq, mtype, fields, orig):
        self.clock += 1
        m = self.build(s, mtype, fields, seq, True, orig)
        self.transmit(s, m)

    def transmit(self, s, m):
        raw = m.encode()
        s.last_tx = self.clock
        s.n_tx += 1
        self.log.append(raw)
        link = self.links[(s.me, s.them)]
        note = ""
        if link.cut:
            note = " (lost: link cut)"
        elif link.drop > 0:
            link.drop -= 1
            note = " (lost)"
        elif link.garble:
            link.garble = False
            k = raw.rindex(b"10=")
            bad = (int(raw[k + 3:k + 6]) + 1) % 256
            raw = raw[:k + 3] + ("%03d" % bad).encode() + raw[k + 6:]
            note = " (garbled)"
        print("  %s %s>%s %s%s" % (self.stamp().strftime("%H:%M:%S.%f")[:12], s.me, s.them,
                                   simplefix.pretty_print(raw).decode("latin-1"), note))
        if note and note != " (garbled)":
            return
        self.queue.append((s.them, s.me, raw))

    def run(self):
        while self.queue:
            me, them, raw = self.queue.pop(0)
            s = self.sess(me, them)
            link = self.links[(them, me)]
            point = 0
            sizes = [7, 19, 64, 3, 200]
            while point < len(raw):
                n = sizes[link.chunk % len(sizes)]
                link.chunk += 1
                s.parser.append_buffer(raw[point:point + n])
                point += n
                while True:
                    m = s.parser.get_message()
                    if m is None:
                        break
                    self.receive(s, m)

    # ---- receiving

    def say(self, s, text):
        print("  %s: %s" % (s.me, text))

    def disconnect(self, s, why):
        self.say(s, "disconnected from %s (%s)" % (s.them, why))
        s.up = False
        s.parser.reset()
        s.test_out = None
        s.resend_pending = False

    def receive(self, s, m):
        raw = m.encode(raw=True)
        k = raw.rindex(b"10=")
        total = sum(raw[:k]) % 256
        start = raw.index(b"\x01", raw.index(b"9=")) + 1
        length = k - start
        if int(m.get(10)) != total or int(m.get(9)) != length:
            s.garbled += 1
            self.say(s, "ignored a garbled message from %s (CheckSum %s, computed %03d; BodyLength %s, counted %d)" % (
                s.them, m.get(10).decode(), total, m.get(9).decode(), length))
            return
        s.last_rx = self.clock
        s.n_rx += 1
        mtype = m.get(35)
        seq = int(m.get(34))
        dup = m.get(43) == b"Y"
        if not s.up and mtype != b"A":
            s.ignored += 1
            self.say(s, "not logged on; ignored %s %d" % (mtype.decode(), seq))
            return
        if mtype == b"A":
            if not s.up:
                s.up = True
                self.say(s, "logged on with %s (their seq %d, expected %d)" % (s.them, seq, s.in_seq))
                if s.me == "BROKER":
                    self.send(s.me, s.them, "A", [(98, "0"), (108, HB)])
            if seq < s.in_seq:
                self.send(s.me, s.them, "5", [(58, "MsgSeqNum too low, expecting %d but received %d" % (s.in_seq, seq))])
                self.disconnect(s, "sequence too low")
                return
        if seq < s.in_seq:
            if dup:
                s.dups += 1
                self.say(s, "ignored duplicate %s %d" % (mtype.decode(), seq))
                return
            self.send(s.me, s.them, "5", [(58, "MsgSeqNum too low, expecting %d but received %d" % (s.in_seq, seq))])
            self.disconnect(s, "sequence too low")
            return
        if seq > s.in_seq:
            s.gaps += 1
            if mtype == b"2":
                # a resend request is answered even when it is ahead of
                # the sequence, or both ends would wait for each other
                self.replay(s, int(m.get(7)), int(m.get(16)))
            if s.resend_pending:
                self.say(s, "gap: expected %d, got %s %d; resend already asked" % (s.in_seq, mtype.decode(), seq))
            else:
                self.say(s, "gap: expected %d, got %s %d; asking for a resend" % (s.in_seq, mtype.decode(), seq))
                s.resend_pending = True
                self.send(s.me, s.them, "2", [(7, s.in_seq), (16, 0)])
            return
        s.resend_pending = False
        if mtype == b"4":
            new = int(m.get(36))
            self.say(s, "gap filled from %d to %d" % (seq, new))
            s.in_seq = new
            return
        s.in_seq += 1
        if mtype == b"A":
            return
        if mtype == b"0":
            if s.test_out is not None and m.get(112) == s.test_out.encode():
                self.say(s, "test request %s answered" % s.test_out)
                s.test_out = None
            return
        if mtype == b"1":
            self.send(s.me, s.them, "0", [(112, m.get(112))])
            return
        if mtype == b"2":
            self.replay(s, int(m.get(7)), int(m.get(16)))
            return
        if mtype == b"5":
            if s.me == "BROKER":
                self.send(s.me, s.them, "5", [(58, "Goodbye")])
            self.disconnect(s, "logout: %s" % m.get(58).decode())
            return
        if mtype == b"3":
            self.say(s, "session reject of %s: tag %s, reason %s, %s" % (
                m.get(45).decode(), m.get(371).decode(), m.get(373).decode(), m.get(58).decode()))
            return
        if s.me == "BROKER":
            self.business(s, m, seq)
        else:
            self.client(s, m)

    def replay(self, s, begin, end):
        last = s.out_seq - 1 if end == 0 else end
        s.resends += 1
        self.say(s, "resending %d to %d to %s" % (begin, last, s.them))
        gap = None
        for seq in range(begin, last + 1):
            mtype, fields, orig = s.sent[seq]
            if mtype.encode() in SESSION_TYPES:
                if gap is None:
                    gap = (seq, orig)
                continue
            if gap is not None:
                self.resend(s, gap[0], "4", [(123, "Y"), (36, seq)], gap[1])
                gap = None
            self.resend(s, seq, mtype, fields, orig)
        if gap is not None:
            self.resend(s, gap[0], "4", [(123, "Y"), (36, last + 1)], gap[1])

    # ---- the broker

    def report(self, o, exec_type, extra, to=None):
        fields = [(37, o.oid), (11, o.clordid), (17, "E%d" % self.next_exec), (150, exec_type), (39, o.status),
                  (55, o.sym), (54, o.side), (38, o.qty)]
        self.next_exec += 1
        if o.px is not None:
            fields.append((44, px(o.px)))
        fields += extra
        fields += [(14, o.cum), (151, o.leaves), (6, avg_px(o.value, o.cum))]
        self.send("BROKER", o.client, "8", fields)

    def business(self, s, m, seq):
        mtype = m.get(35)
        if mtype == b"D":
            for tag in (11, 55, 54, 38, 40):
                if m.get(tag) is None:
                    self.send("BROKER", s.them, "3", [(45, seq), (371, tag), (373, 1), (58, "Required tag missing")])
                    return
            self.new_order(s, m)
        elif mtype == b"F":
            for tag in (11, 41, 55, 54):
                if m.get(tag) is None:
                    self.send("BROKER", s.them, "3", [(45, seq), (371, tag), (373, 1), (58, "Required tag missing")])
                    return
            self.cancel(s, m)
        else:
            self.send("BROKER", s.them, "3", [(45, seq), (372, mtype), (373, 11), (58, "Invalid MsgType")])

    def new_order(self, s, m):
        o = Order()
        o.oid = "O%d" % self.next_order
        o.client = s.them
        o.clordid = m.get(11).decode()
        o.sym = m.get(55).decode()
        o.side = m.get(54).decode()
        q = m.get(38)
        o.qty = int(q) if q.isdigit() else 0
        o.typ = m.get(40).decode()
        o.px = cents(m.get(44)) if o.typ == "2" else None
        o.cum = 0
        o.leaves = 0
        o.value = 0
        o.status = "0"
        o.seq = self.arrivals
        self.arrivals += 1
        why = None
        if o.sym not in SYMBOLS:
            why = "Unknown symbol '%s'" % o.sym
        elif o.side not in ("1", "2"):
            why = "Bad side '%s'" % o.side
        elif o.qty <= 0:
            why = "Bad quantity '%s'" % q.decode()
        elif o.typ not in ("1", "2"):
            why = "Unsupported order type '%s'" % o.typ
        elif o.typ == "2" and m.get(44) is None:
            why = "Limit order without a price"
        elif o.typ == "2" and o.px is None:
            why = "Bad price '%s'" % m.get(44).decode()
        elif any(x.client == o.client and x.clordid == o.clordid for x in self.orders):
            why = "Duplicate ClOrdID '%s'" % o.clordid
        if why is not None:
            o.oid = "NONE"
            o.status = "8"
            self.report(o, "8", [(58, why)])
            return
        self.next_order += 1
        o.leaves = o.qty
        self.orders.append(o)
        self.report(o, "0", [])
        book = self.book[o.sym]
        while o.leaves > 0:
            best = None
            for r in book:
                if r.side != o.side and (best is None or self.better(r, best)):
                    best = r
            if best is None:
                break
            if o.px is not None and ((o.side == "1" and best.px > o.px) or (o.side == "2" and best.px < o.px)):
                break
            fill = min(o.leaves, best.leaves)
            for x in (best, o):
                x.cum += fill
                x.leaves -= fill
                x.value += fill * best.px
                x.status = "2" if x.leaves == 0 else "1"
            self.report(best, "F", [(32, fill), (31, px(best.px))])
            self.report(o, "F", [(32, fill), (31, px(best.px))])
            if best.leaves == 0:
                book.remove(best)
        if o.leaves > 0:
            if o.px is None:
                o.status = "4"
                left = o.leaves
                o.leaves = 0
                self.report(o, "4", [(58, "No liquidity for %d" % left)])
            else:
                book.append(o)

    def better(self, a, b):
        if a.px != b.px:
            return a.px < b.px if a.side == "2" else a.px > b.px
        return a.seq < b.seq

    def cancel(self, s, m):
        orig = m.get(41).decode()
        clid = m.get(11).decode()
        o = None
        for x in self.orders:
            if x.client == s.them and x.clordid == orig:
                o = x
        if o is None or o.leaves == 0:
            fields = [(37, o.oid if o is not None else "NONE"), (11, clid), (41, orig),
                      (39, o.status if o is not None else "8"), (434, 1), (102, 0 if o is not None else 1),
                      (58, "Too late to cancel" if o is not None else "Unknown order")]
            self.send("BROKER", s.them, "9", fields)
            return
        self.book[o.sym].remove(o)
        o.status = "4"
        left = o.leaves
        o.leaves = 0
        o.clordid = clid
        self.report(o, "4", [(41, orig), (58, "Cancelled %d" % left)])

    # ---- the clients

    def client(self, s, m):
        mtype = m.get(35)
        view = self.views[s.me]
        if mtype == b"8":
            key = m.get(11).decode() + " " + m.get(37).decode()
            row = [key, m.get(39).decode(), m.get(14).decode(), m.get(151).decode(), m.get(6).decode(),
                   m.get(58).decode() if m.get(58) is not None else ""]
            for k in range(len(view)):
                if view[k][0] == key:
                    view[k] = row
                    break
            else:
                view.append(row)
            orig = m.get(41)
            if orig is not None:
                old = orig.decode() + " " + m.get(37).decode()
                for k in range(len(view)):
                    if view[k][0] == old:
                        view[k] = [old, "4", view[k][2], "0", view[k][4], "cancelled as " + m.get(11).decode()]
        elif mtype == b"9":
            view.append([m.get(11).decode() + " " + m.get(37).decode(), "cancel rejected", "-", "-", "-",
                         m.get(58).decode()])

    # ---- steps

    def step(self, toks):
        op = toks[0]
        if op == "logon":
            s = self.sess(toks[1], "BROKER")
            self.send(toks[1], "BROKER", "A", [(98, "0"), (108, HB)])
        elif op in ("order", "cancel", "bare"):
            s = self.sess(toks[1], "BROKER")
            if not s.up:
                print("  %s: not logged on; %s %s not sent" % (toks[1], op, toks[2]))
                return
            if op == "order":
                fields = [(11, toks[2]), (55, toks[4]), (54, toks[3]), (38, toks[5]), (40, toks[6])]
                if len(toks) > 7:
                    fields.append((44, toks[7]))
                self.placed[toks[1]].append((toks[2], toks[4], toks[3]))
                self.send(toks[1], "BROKER", "D", fields)
            elif op == "cancel":
                sym, side = "MSFT", "1"
                for row in self.placed[toks[1]]:
                    if row[0] == toks[3]:
                        sym, side = row[1], row[2]
                fields = [(11, toks[2]), (41, toks[3]), (55, sym), (54, side)]
                self.send(toks[1], "BROKER", "F", fields)
            else:
                fields = []
                for t in toks[3:]:
                    tag, _, v = t.partition("=")
                    fields.append((int(tag), v))
                self.send(toks[1], "BROKER", toks[2], fields)
        elif op == "logout":
            s = self.sess(toks[1], "BROKER")
            self.send(toks[1], "BROKER", "5", [(58, "End of day")])
        elif op == "drop":
            self.links[(toks[1], toks[2])].drop += int(toks[3])
            print("  the link %s>%s will lose %s" % (toks[1], toks[2], toks[3]))
        elif op == "garble":
            self.links[(toks[1], toks[2])].garble = True
            print("  the link %s>%s will garble the next message" % (toks[1], toks[2]))
        elif op in ("cut", "heal"):
            for key in ((toks[1], "BROKER"), ("BROKER", toks[1])):
                self.links[key].cut = op == "cut"
            print("  the link to %s is %s" % (toks[1], "cut" if op == "cut" else "back"))
        elif op == "tick":
            for _ in range(int(toks[1])):
                self.clock += 1000 - self.clock % 1000
                for s in self.sessions:
                    if not s.up:
                        continue
                    if s.test_out is not None and self.clock - s.test_at >= HB * 1000:
                        self.send(s.me, s.them, "5", [(58, "No answer to test request %s" % s.test_out)])
                        self.disconnect(s, "heartbeat timeout")
                        continue
                    if s.test_out is None and self.clock - s.last_rx >= (HB + HB // 5) * 1000:
                        s.tests += 1
                        s.test_out = "%s-T%d" % (s.me, s.tests)
                        s.test_at = self.clock
                        self.send(s.me, s.them, "1", [(112, s.test_out)])
                    elif self.clock - s.last_tx >= HB * 1000:
                        self.send(s.me, s.them, "0", [])
                    self.run()
        elif op == "book":
            book = self.book[toks[1]]
            bids = sorted([o for o in book if o.side == "1"], key=lambda o: (-o.px, o.seq))
            asks = sorted([o for o in book if o.side == "2"], key=lambda o: (o.px, o.seq))
            print("  %s book: bids %s; asks %s" % (
                toks[1], ", ".join("%d@%s %s" % (o.leaves, px(o.px), o.clordid) for o in bids) or "none",
                ", ".join("%d@%s %s" % (o.leaves, px(o.px), o.clordid) for o in asks) or "none"))
        elif op == "orders":
            for row in self.views[toks[1]]:
                print("  %s %s: status %s, filled %s, open %s, avg %s%s" % (
                    toks[1], row[0], row[1], row[2], row[3], row[4], "; " + row[5] if row[5] else ""))
        elif op == "stats":
            for s in self.sessions:
                print("  %s>%s: %s, sent %d (next %d), received %d (next %d), gaps %d, resends %d, duplicates %d, "
                      "garbled %d, ignored %d" % (s.me, s.them, "up" if s.up else "down", s.n_tx, s.out_seq,
                                                   s.n_rx, s.in_seq, s.gaps, s.resends, s.dups, s.garbled, s.ignored))
        elif op == "log":
            with open("fix.log", "wb") as f:
                f.write(b"".join(raw + b"\n" for raw in self.log))
            with open("fix.log", "rb") as f:
                data = f.read()
            p = simplefix.FixParser(stop_byte=b"\n")
            p.append_buffer(data)
            first = 0
            while p.get_message() is not None:
                first += 1
            print("  fix.log read until the first None: %d message, %d bytes left" % (first, len(p.get_buffer())))
            p.reset()
            p.append_buffer(data)
            counts = {}
            bad = 0
            n = 0
            nones = 0
            while len(p.get_buffer()) > 0:
                m = p.get_message()
                if m is None:
                    nones += 1
                    continue
                n += 1
                t = m.get(35).decode()
                counts[t] = counts.get(t, 0) + 1
                raw = m.encode(raw=True)
                k = raw.rindex(b"10=")
                if int(m.get(10)) != sum(raw[:k]) % 256:
                    bad += 1
            print("  fix.log read until the buffer is empty: %d messages and %d Nones, %d bytes, fnv %08x; "
                  "by type %s; %d bad checksums" % (n, nones, len(data), fnv(data),
                                                     " ".join("%s:%d" % (t, counts[t]) for t in sorted(counts)), bad))
            os.remove("fix.log")
        if op not in ("tick",):
            self.run()


# ---------------------------------------------------------------- steps

def run_step(st, line):
    toks = line.split(" ")
    op = toks[0]
    if op == "venue":
        st["venue"] = Venue()
        print("venue: BROKER with CLIENT1 and CLIENT2, heartbeat %d s, symbols %s" % (HB, " ".join(SYMBOLS)))
        return
    if op in ("logon", "order", "cancel", "bare", "logout", "drop", "garble", "cut", "heal", "tick", "book",
              "orders", "stats", "log"):
        print(line)
        st["venue"].step(toks)
        return
    ms = st["msgs"]
    ps = st["parsers"]
    try:
        if op == "new":
            ms[toks[1]] = simplefix.FixMessage()
        elif op == "pair":
            ms[toks[1]].append_pair(value(toks[2]), value(toks[3]), header=len(toks) > 4)
        elif op == "str":
            ms[toks[1]].append_string(value(toks[2]))
        elif op == "strs":
            ms[toks[1]].append_strings([value(t) for t in toks[2:]])
        elif op == "data":
            ms[toks[1]].append_data(value(toks[2]), value(toks[3]), value(toks[4]), header=len(toks) > 5)
        elif op == "utc":
            ms[toks[1]].append_utc_timestamp(value(toks[2]), when(toks[3]), precision=value(toks[4]),
                                             header=len(toks) > 5)
        elif op == "utct":
            ms[toks[1]].append_utc_time_only(value(toks[2]), when(toks[3]), precision=value(toks[4]))
        elif op == "atime":
            ms[toks[1]].append_time(value(toks[2]), when(toks[3]), precision=value(toks[4]))
        elif op == "utcp":
            ms[toks[1]].append_utc_time_only_parts(value(toks[2]), value(toks[3]), value(toks[4]), value(toks[5]),
                                                   value(toks[6]), value(toks[7]))
        elif op == "tzp":
            ms[toks[1]].append_tz_time_only_parts(value(toks[2]), value(toks[3]), value(toks[4]), value(toks[5]),
                                                  value(toks[6]), value(toks[7]), offset=value(toks[8]))
        elif op == "get":
            print("%s = %r" % (line, ms[toks[1]].get(value(toks[2]), *[value(t) for t in toks[3:]])))
        elif op == "rm":
            print("%s = %r" % (line, ms[toks[1]].remove(value(toks[2]), *[value(t) for t in toks[3:]])))
        elif op == "has":
            print("%s = %s" % (line, value(toks[2]) in ms[toks[1]]))
        elif op == "count":
            print("%s = %d" % (line, ms[toks[1]].count()))
        elif op == "item":
            tag, v = ms[toks[1]][value(toks[2])]
            print("%s = (%d, %r)" % (line, tag, v))
        elif op == "eq":
            print("%s = %s" % (line, ms[toks[1]] == ms[toks[2]]))
        elif op == "enc":
            print("%s = %s" % (line, pretty(ms[toks[1]].encode(raw=len(toks) > 2))))
        elif op == "show":
            sep = value(toks[2]) if len(toks) > 2 else "|"
            print("%s = %s" % (line, ms[toks[1]].to_string(sep)))
        elif op == "parser":
            kw = {}
            for t in toks[2:]:
                k, v = t.split("=", 1)
                if k == "empty":
                    kw["allow_empty_values"] = v == "1"
                elif k == "missing":
                    kw["allow_missing_begin_string"] = v == "1"
                elif k == "strip":
                    kw["strip_fields_before_begin_string"] = v == "1"
                elif k == "stop_tag":
                    kw["stop_tag"] = int(v)
                elif k == "stop_byte":
                    kw["stop_byte"] = value(v)
            ps[toks[1]] = simplefix.FixParser(**kw)
        elif op == "feed":
            ps[toks[1]].append_buffer(value(toks[2]))
        elif op == "next":
            print("%s = %s" % (line, shown(ps[toks[1]].get_message())))
        elif op == "drain":
            p = ps[toks[1]]
            while True:
                m = p.get_message()
                print("%s = %s" % (line, shown(m)))
                if m is None:
                    break
        elif op == "buf":
            print("%s = %r" % (line, ps[toks[1]].get_buffer()))
        elif op == "reset":
            ps[toks[1]].reset()
        elif op == "addraw":
            ps[toks[1]].add_raw(value(toks[2]), value(toks[3]))
        elif op == "rmraw":
            ps[toks[1]].remove_raw(value(toks[2]), value(toks[3]))
        elif op == "set":
            p = ps[toks[1]]
            v = value(toks[3])
            if toks[2] == "stop_tag":
                p.set_stop_tag(v)
            elif toks[2] == "stop_byte":
                p.set_stop_byte(v)
            elif toks[2] == "empty":
                p.set_allow_empty_values(v == 1)
            elif toks[2] == "missing":
                p.set_allow_missing_begin_string(v == 1)
            else:
                p.set_strip_fields_before_begin_string(v == 1)
        elif op == "term":
            p = ps[toks[1]]
            a = toks[2]
            if a == "both":
                p.set_message_terminator(tag=10, char=b"\n")
            elif a == "none":
                p.set_message_terminator()
            elif a.startswith("tag="):
                p.set_message_terminator(tag=int(a[4:]))
            else:
                p.set_message_terminator(char=value(a[5:]))
        elif op == "pipe":
            m = ms[toks[1]]
            p = ps[toks[2]]
            sizes = [int(x) for x in toks[3].split(",")]
            buf = m.encode()
            point = 0
            k = 0
            got = 0
            while point < len(buf):
                n = sizes[k % len(sizes)]
                k += 1
                p.append_buffer(buf[point:point + n])
                point += n
                while True:
                    r = p.get_message()
                    if r is None:
                        break
                    got += 1
                    print("%s @%d = %s" % (line, min(point, len(buf)), shown(r)))
            print("%s: %d bytes in %d chunks, %d messages, %r left" % (line, len(buf), k, got, p.get_buffer()))
        elif op == "pretty":
            print("%s = %s" % (line, pretty(value(toks[1]))))
        else:
            raise SystemExit("bad step " + line)
    except (ValueError, IndexError, errors.ParsingError, errors.ParserConfigError) as e:
        print("%s = %s" % (line, err(e)))


def main():
    with open(os.path.join(HERE, "data", "jobs.txt")) as f:
        lines = f.read().split("\n")
    st = {"msgs": {}, "parsers": {}, "venue": None}
    for line in lines:
        if not line:
            continue
        if line.startswith("job "):
            st["msgs"] = {}
            st["parsers"] = {}
            print("== " + line[4:])
            continue
        run_step(st, line)


main()
