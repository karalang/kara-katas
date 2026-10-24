#!/usr/bin/env python3
"""The load client for the M4a gate (see README.md and run.sh).

Two measurements, each printed as one JSON object:

  idle  Open N TCP connections to a server and leave them idle. Reports how
        many the server accepted (from its open descriptors), its resident
        memory before and after, and the latency of a fresh request made
        while the idle connections are held.

  rate  Send requests at a fixed rate (open loop: request i is due at
        t0 + i / rate, whether or not earlier ones have finished) and report
        latency percentiles. Latency is measured from when a request was due,
        so time spent waiting for a free connection counts.

The client is Python, so its own overhead is in every latency it reports.
Run as: python3 -I -B loadclient.py idle|rate --help
"""
import argparse
import asyncio
import gc
import json
import multiprocessing
import os
import resource
import selectors
import socket
import statistics
import sys
import time


# ------------------------------------------------------------ server probes

def proc_status(pid):
    """VmRSS and VmHWM of the server, in KiB, its threads and its open
    descriptors."""
    out = {}
    with open('/proc/%d/status' % pid) as f:
        for line in f:
            if line.startswith(('VmRSS:', 'VmHWM:', 'Threads:')):
                out[line.split(':')[0]] = int(line.split()[1])
    out['fds'] = len(os.listdir('/proc/%d/fd' % pid))
    return out


def raise_nofile():
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    if soft < hard:
        resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))
    return resource.getrlimit(resource.RLIMIT_NOFILE)[0]


def one_request(host, port, raw, close):
    """Send one request on a fresh connection and return (seconds, status)."""
    t = time.perf_counter()
    s = socket.create_connection((host, port), timeout=30)
    try:
        s.sendall(raw)
        if close:
            s.shutdown(socket.SHUT_WR)
        data = b''
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            data += chunk
            if not close and complete_reply(data):
                break
    finally:
        s.close()
    return time.perf_counter() - t, status_of(data)


def status_of(data):
    try:
        return int(data.split(b' ', 2)[1])
    except (IndexError, ValueError):
        return 0


def complete_reply(data):
    """True once data holds a whole response with a Content-Length body."""
    end = data.find(b'\r\n\r\n')
    if end < 0:
        return False
    length = 0
    for line in data[:end].split(b'\r\n')[1:]:
        k, _, v = line.partition(b':')
        if k.strip().lower() == b'content-length':
            length = int(v.strip())
    return len(data) >= end + 4 + length


# ----------------------------------------------------------------- idle mode

def idle_worker(host, port, n, src_ips, batch, conn_pipe):
    """Open n connections from the given source addresses, report the count,
    then hold them until the parent says stop."""
    raise_nofile()
    sel = selectors.DefaultSelector()
    held = []
    failed = 0
    ip_i = 0
    while len(held) < n:
        pending = []
        for _ in range(min(batch, n - len(held))):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(False)
            try:
                s.bind((src_ips[ip_i % len(src_ips)], 0))
            except OSError:
                s.close()
                ip_i += 1
                failed += 1
                continue
            s.connect_ex((host, port))
            sel.register(s, selectors.EVENT_WRITE)
            pending.append(s)
        deadline = time.monotonic() + 10
        waiting = set(pending)
        while waiting and time.monotonic() < deadline:
            for key, _ in sel.select(timeout=0.5):
                s = key.fileobj
                sel.unregister(s)
                waiting.discard(s)
                if s.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR) == 0:
                    held.append(s)
                else:
                    failed += 1
                    s.close()
        # Connects still in progress after 10 s count as failed.
        for s in waiting:
            sel.unregister(s)
            failed += 1
            s.close()
        conn_pipe.send(('progress', len(held), failed))
        if failed > max(100, n // 10):
            break
        ip_i += 1
    conn_pipe.send(('done', len(held), failed))
    try:
        conn_pipe.recv()
    except EOFError:
        pass
    for s in held:
        s.close()


def run_idle(a):
    nofile = raise_nofile()
    per_worker = max(1, min(a.per_worker, nofile - 100))
    workers = (a.conns + per_worker - 1) // per_worker
    # One loopback source address per 25k connections keeps every worker
    # inside the ephemeral port range.
    ips = ['127.0.%d.%d' % (1 + i // 250, 1 + i % 250) for i in range(max(4, a.conns // 25000 + 1))]
    base = proc_status(a.pid)
    t0 = time.monotonic()
    pipes, procs = [], []
    left = a.conns
    for w in range(workers):
        n = min(per_worker, left)
        left -= n
        parent, child = multiprocessing.Pipe()
        p = multiprocessing.Process(target=idle_worker, args=(a.host, a.port, n, ips[w % len(ips):] + ips[:w % len(ips)], a.batch, child))
        p.start()
        pipes.append(parent)
        procs.append(p)
    opened = [0] * workers
    failed = [0] * workers
    done = [False] * workers
    deadline = t0 + a.ramp_limit
    while not all(done) and time.monotonic() < deadline:
        for i, pipe in enumerate(pipes):
            while not done[i] and pipe.poll(0.05):
                kind, n, f = pipe.recv()
                opened[i], failed[i] = n, f
                done[i] = kind == 'done'
    ramp = time.monotonic() - t0
    # Wait for the server to accept what the kernel has queued for it.
    accepted = proc_status(a.pid)['fds'] - base['fds']
    settle_until = time.monotonic() + a.settle
    last, last_change = accepted, time.monotonic()
    while accepted < sum(opened) and time.monotonic() < settle_until:
        time.sleep(0.5)
        accepted = proc_status(a.pid)['fds'] - base['fds']
        if accepted != last:
            last, last_change = accepted, time.monotonic()
        elif time.monotonic() - last_change > 10:
            break
    time.sleep(a.hold)
    held = proc_status(a.pid)
    probes = []
    probe_status = []
    for _ in range(a.probes):
        try:
            dt, st = one_request(a.host, a.port, a.probe_request.encode().decode('unicode_escape').encode(), a.probe_close)
            probes.append(dt)
            probe_status.append(st)
        except OSError as e:
            probe_status.append(str(e))
    # A forked worker holds a copy of the parent's end of its pipe, so
    # closing that end never reaches it as EOF: tell it to stop instead.
    for pipe in pipes:
        try:
            pipe.send('stop')
        except OSError:
            pass
        pipe.close()
    for p in procs:
        p.join(timeout=30)
        if p.is_alive():
            p.terminate()
            p.join()
    accepted = held['fds'] - base['fds']
    out = {
        'mode': 'idle',
        'target_conns': a.conns,
        'client_open': sum(opened),
        'client_failed': sum(failed),
        'ramp_s': round(ramp, 2),
        'ramp_complete': all(done),
        'server_accepted': accepted,
        'server_rss_before_kib': base['VmRSS'],
        'server_rss_held_kib': held['VmRSS'],
        'server_hwm_kib': held['VmHWM'],
        'server_threads_before': base['Threads'],
        'server_threads_held': held['Threads'],
        'rss_per_conn_bytes': round((held['VmRSS'] - base['VmRSS']) * 1024 / accepted) if accepted > 0 else None,
        'rlimit_nofile': nofile,
        'probe_ms_median': round(statistics.median(probes) * 1000, 3) if probes else None,
        'probe_ms_max': round(max(probes) * 1000, 3) if probes else None,
        'probe_status': sorted(set(str(s) for s in probe_status)),
    }
    print(json.dumps(out))


# ----------------------------------------------------------------- rate mode

def kv_request(i):
    key = 'k%d' % (i % 100)
    if i % 10 == 9:
        body = '{"value":"v%d","tags":["load"]}' % i
        return ('PUT /kv/%s HTTP/1.1\r\nHost: kv\r\nContent-Length: %d\r\n\r\n%s' % (key, len(body), body)).encode()
    return ('GET /kv/%s HTTP/1.1\r\nHost: kv\r\n\r\n' % key).encode()


def proxy_request(i):
    return ('GET /api/users/%d HTTP/1.1\r\nHost: shop.test\r\n\r\n' % (i % 10)).encode()


async def read_reply(reader):
    head = await reader.readuntil(b'\r\n\r\n')
    length = 0
    for line in head.split(b'\r\n')[1:]:
        k, _, v = line.partition(b':')
        if k.strip().lower() == b'content-length':
            length = int(v.strip())
    body = await reader.readexactly(length) if length else b''
    return head + body


async def rate_main(a):
    loop = asyncio.get_running_loop()
    make = kv_request if a.target == 'kv' else proxy_request
    keepalive = a.target == 'kv'
    lat = []
    statuses = {}
    errors = {}
    bad = []
    pool = asyncio.Queue()
    if keepalive:
        for _ in range(a.conns):
            pool.put_nowait(await asyncio.open_connection(a.host, a.port))

    def note(d, k):
        d[k] = d.get(k, 0) + 1

    async def one(i, due, record):
        try:
            if keepalive:
                r, w = await pool.get()
                try:
                    w.write(make(i))
                    await w.drain()
                    reply = await asyncio.wait_for(read_reply(r), a.timeout)
                    pool.put_nowait((r, w))
                except Exception:
                    w.close()
                    pool.put_nowait(await asyncio.open_connection(a.host, a.port))
                    raise
            else:
                r, w = await asyncio.wait_for(asyncio.open_connection(a.host, a.port), a.timeout)
                w.write(make(i))
                await w.drain()
                w.write_eof()
                reply = await asyncio.wait_for(r.read(), a.timeout)
                w.close()
            done = loop.time()
            if record:
                lat.append(done - due)
                st = status_of(reply)
                note(statuses, st)
                if st != 200 and len(bad) < 10:
                    bad.append({'i': i, 'at_s': round(due - t0, 3), 'status': st, 'bytes': len(reply), 'head': reply[:60].decode('latin-1')})
        except Exception as e:
            if record:
                note(errors, type(e).__name__)
                if len(bad) < 10:
                    bad.append({'i': i, 'at_s': round(due - t0, 3), 'error': type(e).__name__})

    total = int(a.rate * (a.warmup + a.seconds))
    warm = int(a.rate * a.warmup)
    t0 = loop.time() + 0.2
    tasks = []
    behind = 0.0
    for i in range(total):
        due = t0 + i / a.rate
        now = loop.time()
        if due > now:
            await asyncio.sleep(due - now)
        else:
            behind = max(behind, now - due)
        tasks.append(asyncio.ensure_future(one(i, due, i >= warm)))
    await asyncio.gather(*tasks)
    elapsed = loop.time() - t0
    lat.sort()

    def pct(p):
        return round(lat[min(len(lat) - 1, int(p * len(lat)))] * 1000, 3) if lat else None
    out = {
        'mode': 'rate',
        'target': a.target,
        'rate': a.rate,
        'seconds': a.seconds,
        'warmup_s': a.warmup,
        'connections': a.conns if keepalive else 'one per request',
        'measured': len(lat),
        'statuses': {str(k): v for k, v in sorted(statuses.items())},
        'errors': errors,
        'first_bad': bad,
        'p50_ms': pct(0.50),
        'p90_ms': pct(0.90),
        'p99_ms': pct(0.99),
        'p999_ms': pct(0.999),
        'max_ms': round(lat[-1] * 1000, 3) if lat else None,
        'achieved_rate': round(total / elapsed, 1),
        'client_max_lag_ms': round(behind * 1000, 3),
    }
    print(json.dumps(out))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='mode', required=True)
    i = sub.add_parser('idle')
    i.add_argument('--pid', type=int, required=True, help='the server process, for /proc')
    i.add_argument('--host', default='127.0.0.1')
    i.add_argument('--port', type=int, required=True)
    i.add_argument('--conns', type=int, required=True)
    i.add_argument('--per-worker', type=int, default=15000, help='connections per client process')
    i.add_argument('--batch', type=int, default=500)
    i.add_argument('--ramp-limit', type=float, default=600, help='seconds allowed to open them')
    i.add_argument('--settle', type=float, default=120, help='seconds allowed for the server to accept them')
    i.add_argument('--hold', type=float, default=5)
    i.add_argument('--probes', type=int, default=20)
    i.add_argument('--probe-request', default='GET /kv/k1 HTTP/1.1\\r\\nHost: kv\\r\\n\\r\\n')
    i.add_argument('--probe-close', action='store_true', help='shut the write side after the probe request')
    r = sub.add_parser('rate')
    r.add_argument('--target', choices=['kv', 'proxy'], required=True)
    r.add_argument('--host', default='127.0.0.1')
    r.add_argument('--port', type=int, required=True)
    r.add_argument('--rate', type=float, default=500)
    r.add_argument('--seconds', type=float, default=30)
    r.add_argument('--warmup', type=float, default=2)
    r.add_argument('--conns', type=int, default=32, help='keep-alive connections (kv)')
    r.add_argument('--timeout', type=float, default=10)
    a = ap.parse_args()
    if a.mode == 'idle':
        run_idle(a)
    else:
        raise_nofile()
        # A collection pass over thousands of live tasks stalls the loop for
        # tens of milliseconds, which would land in the server's latency.
        gc.disable()
        asyncio.run(rate_main(a))


if __name__ == '__main__':
    multiprocessing.set_start_method('fork')
    main()
