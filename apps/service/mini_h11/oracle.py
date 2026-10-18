#!/usr/bin/env python3
"""The oracle: runs the connection scripts in data/scripts/ against h11
0.16.0, the sans-I/O HTTP/1.1 library under httpx and uvicorn, and prints
expected.out. Run mk.py first."""
import os

import h11


def unescape(s):
    """\\r, \\n, \\t, \\\\ and \\xHH; nothing else is special."""
    out = bytearray()
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            n = s[i + 1]
            if n == "x":
                out.append(int(s[i + 2:i + 4], 16))
                i += 4
                continue
            out += {"r": b"\r", "n": b"\n", "t": b"\t", "\\": b"\\"}[n]
            i += 2
            continue
        out += c.encode()
        i += 1
    return bytes(out)


def split_headers(rest):
    """`A B C | Name: value | Name: value` -> ([A, B, C], [(name, value)])."""
    parts = rest.split(" | ")
    head = parts[0].split(" ") if parts[0] else []
    headers = []
    for p in parts[1:]:
        name, _, value = p.partition(": ")
        headers.append((unescape(name), unescape(value)))
    return head, headers


def error_line(e):
    if isinstance(e, h11.ProtocolError):
        return "  %s: %s [%d]" % (type(e).__name__, e, e.error_status_hint)
    return "  %s: %s" % (type(e).__name__, e)


class Script:
    def __init__(self):
        self.conn = None
        self.out = []

    def say(self, s):
        self.out.append(s)

    def states(self):
        c = self.conn
        s = "  = CLIENT=%s SERVER=%s" % (c.states[h11.CLIENT], c.states[h11.SERVER])
        if c.client_is_waiting_for_100_continue:
            s += " waiting-100"
        if not c._cstate.keep_alive:
            s += " no-keep-alive"
        self.say(s)

    def next(self):
        try:
            e = self.conn.next_event()
        except Exception as e:
            self.say(error_line(e))
            return False
        self.say("  " + repr(e))
        return e not in (h11.NEED_DATA, h11.PAUSED) and type(e) is not h11.ConnectionClosed

    def drain(self):
        for _ in range(100):
            if not self.next():
                return

    def feed(self, data):
        try:
            self.conn.receive_data(data)
        except Exception as e:
            self.say(error_line(e))
            return
        self.drain()

    def send(self, make):
        try:
            event = make()
        except Exception as e:
            self.say(error_line(e))
            return
        try:
            data = self.conn.send(event)
        except Exception as e:
            self.say(error_line(e))
            return
        self.say("  sent " + repr(data))

    def op(self, line):
        word, _, rest = line.partition(" ")
        if word == "role":
            args = rest.split(" ")
            role = h11.CLIENT if args[0] == "client" else h11.SERVER
            size = int(args[2]) if len(args) > 2 else 16 * 1024
            self.conn = h11.Connection(role, max_incomplete_event_size=size)
        elif word == "recv":
            self.feed(unescape(rest))
        elif word == "recvfile":
            path, size = rest.split(" ")
            with open("data/" + path, "rb") as f:
                data = f.read()
            for i in range(0, len(data), int(size)):
                self.say("  .. %d bytes" % len(data[i:i + int(size)]))
                self.feed(data[i:i + int(size)])
        elif word == "eof":
            self.feed(b"")
        elif word == "next":
            self.next()
        elif word == "drain":
            self.drain()
        elif word in ("request", "response", "info"):
            head, headers = split_headers(rest)
            if word == "request":
                self.send(lambda: h11.Request(method=head[0], target=unescape(head[1]),
                                              http_version=head[2], headers=headers))
            else:
                cls = h11.Response if word == "response" else h11.InformationalResponse
                reason = " ".join(head[2:])
                self.send(lambda: cls(status_code=int(head[0]), http_version=head[1],
                                      reason=reason, headers=headers))
        elif word == "data":
            self.send(lambda: h11.Data(data=unescape(rest)))
        elif word == "eom":
            _, headers = split_headers(rest)
            self.send(lambda: h11.EndOfMessage(headers=headers))
        elif word == "close":
            self.send(lambda: h11.ConnectionClosed())
        elif word == "cycle":
            try:
                self.conn.start_next_cycle()
            except Exception as e:
                self.say(error_line(e))
        elif word == "failed":
            self.conn.send_failed()
        else:
            raise ValueError(word)
        self.states()


def main():
    names = sorted(os.listdir("data/scripts"))
    for name in names:
        print("== " + name)
        s = Script()
        with open("data/scripts/" + name) as f:
            lines = f.read().split("\n")
        for line in lines:
            if not line or line.startswith("#"):
                continue
            s.say("> " + line)
            s.op(line)
        data, closed = s.conn.trailing_data
        s.say("  trailing %r closed=%s" % (data, closed))
        print("\n".join(s.out))


if __name__ == "__main__":
    main()
