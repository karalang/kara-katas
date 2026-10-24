# apps/loadtest

The load test for the M4a gate (`review/m4-plan-2026-10-24.md` in the
project's shared folder, approved 2026-10-24). It measures two things on
Linux against Kāra servers built with `karac build`:

1. **Idle connections.** N TCP connections opened and left idle, and the
   server's resident memory while it holds them. The bar is 100k connections
   under 1 GB.
2. **Latency at a fixed rate.** p99 of requests sent at a fixed rate to
   the key-value store and the reverse proxy. The bar is under 10 ms.

It can't pass until M4a's reactor lands (item 2 of the plan). It exists now
to record today's baseline, so the reactor's change shows up as a number.

## Files

- `kv_serve.kara` is `apps/service/kv_http` as a long-running server: the
  same request parser, routes and replies, with a keep-alive read loop per
  connection, one task per connection, and the store behind a `Mutex`. It
  listens on `127.0.0.1:27760` and starts with 100 keys.
- `proxy_serve.kara` is `apps/service/rev_proxy` as a long-running
  server: the same routes, pools, header rewriting and failover, with the
  two live origins (b1, b2) in the same process, a task per connection, and
  the shared state behind a `Mutex`. The proxy listens on `27761`; b1 and b2
  on `27762` and `27763`; b4 and s1 are in the pools with nothing listening.
- `loadclient.py` is the client (Python 3, standard library only).
  `idle` opens N connections from several processes and loopback source
  addresses, then reads the server's descriptors and memory from `/proc`
  and times a fresh request while they are held. `rate` sends requests in
  an open loop (request i is due at t0 + i / rate whether or not the
  others have finished) and reports percentiles measured from when each
  request was due, so queueing counts.
- `run.sh` builds both servers and runs the tiers and rates; `summarize.py`
  turns `results.jsonl` into the tables below.

```bash
bash run.sh [results-dir]       # KARAC=<path to karac>; TIERS, RATES, RATE_SECONDS, HELD_IDLE
```

## Baseline

Measured 2026-10-24 in a cloud container (4 CPUs, 16 GB, Linux 6.18,
descriptor limit 20000) against servers built by `karac` at `4540c92380`.
The raw rows are in `results/results.jsonl`; `results/machine.txt` has the
machine. Each idle tier runs on a fresh server; "with 10000 idle" runs hold
10000 idle connections open for the whole rate run. Rates run 30 s after a
2 s warmup. The kv rates use 32 keep-alive connections (90% GET, 10% PUT);
the proxy rates open a connection per request, as `rev_proxy`'s clients do.

#### Idle connections

| run | asked | accepted | RSS before (MiB) | RSS held (MiB) | bytes per conn | threads | probe median (ms) | probe max (ms) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| idle kv_serve 1000 | 1000 | 1000 | 2.1 | 6.6 | 4788 | 1 | 1.306 | 5.029 |
| idle kv_serve 5000 | 5000 | 5000 | 2.1 | 25.2 | 4851 | 1 | 15.916 | 19.984 |
| idle kv_serve 10000 | 10000 | 10000 | 2.2 | 48.4 | 4848 | 1 | 29.929 | 37.14 |
| idle kv_serve 19500 | 19500 | 19500 | 2.1 | 92.2 | 4850 | 1 | 60.006 | 86.936 |
| idle proxy_serve 1000 | 1000 | 1000 | 2.1 | 4.0 | 2011 | 1 | 2.646 | 7.201 |
| idle proxy_serve 5000 | 5000 | 5000 | 2.1 | 12.0 | 2064 | 1 | 25.43 | 35.21 |
| idle proxy_serve 10000 | 10000 | 10000 | 2.1 | 21.8 | 2065 | 1 | 57.084 | 73.818 |
| idle proxy_serve 19500 | 19500 | 19500 | 2.0 | 40.5 | 2066 | 1 | 114.744 | 150.583 |
| idle kv_serve 10000 during rates | 10000 | 10000 | 2.0 | 48.4 | 4862 | 1 | None | None |
| idle proxy_serve 10000 during rates | 10000 | 10000 | 2.0 | 22.1 | 2107 | 1 | None | None |

#### Fixed request rates

| run | measured | achieved rps | p50 (ms) | p99 (ms) | p99.9 (ms) | max (ms) | client lag (ms) | errors |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| rate kv_serve 500 | 15000 | 499.7 | 0.943 | 1.769 | 10.517 | 36.436 | 32.926 | none |
| rate kv_serve 1000 | 30000 | 999.1 | 0.743 | 1.59 | 4.116 | 26.585 | 5.713 | none |
| rate kv_serve 2000 | 60000 | 1996.1 | 0.748 | 1.66 | 5.292 | 57.112 | 16.951 | none |
| rate kv_serve 500 with 10000 idle | 15000 | 499.5 | 8.834 | 18.63 | 21.485 | 29.604 | 4.062 | none |
| rate kv_serve 1000 with 10000 idle | 30000 | 998.1 | 8.79 | 18.64 | 29.569 | 67.556 | 32.432 | none |
| rate kv_serve 2000 with 10000 idle | 60000 | 1994.8 | 11.956 | 58.148 | 67.341 | 89.564 | 7.742 | none |
| rate proxy_serve 500 | 15000 | 499.8 | 1.241 | 2.591 | 12.076 | 28.362 | 5.902 | none |
| rate proxy_serve 1000 | 30000 | 998.4 | 1.051 | 2.842 | 17.116 | 46.944 | 22.16 | none |
| rate proxy_serve 2000 | 60000 | 1996.1 | 0.895 | 4.973 | 45.583 | 69.315 | 26.175 | none |
| rate proxy_serve 500 with 10000 idle | 15000 | 498.9 | 52.508 | 72.49 | 182.376 | 209.567 | 67.463 | none |
| rate proxy_serve 1000 with 10000 idle | 30000 | 996.7 | 56.438 | 77.252 | 89.379 | 107.433 | 16.639 | none |
| rate proxy_serve 2000 with 10000 idle | 60000 | 1991.4 | 61.817 | 87.086 | 105.474 | 133.089 | 34.735 | none |

#### Against the M4a bars

- Idle: NOT MEASURED. The most connections held was 19500 (descriptor limit 20000), short of 100000.
- p99 on kv_serve: FAIL, worst 58.148 ms (rate kv_serve 2000 with 10000 idle).
- p99 on proxy_serve: FAIL, worst 87.086 ms (rate proxy_serve 2000 with 10000 idle).

## What the numbers say

- **Memory per idle connection is small and flat**: about 4.8 KB on
  kv_serve (which reads into a 4 KB buffer per connection) and 2.1 KB on
  proxy_serve, the same from 1000 to 19500 connections, all on one OS
  thread. At that
  rate 100k idle connections would take about 485 MB and 207 MB. That is a
  projection: this container could not open more than 19500.
- **What fails is time, and it grows with the idle count.** A fresh request
  on kv_serve takes 1.3 ms with 1000 idle connections and 60 ms with 19500,
  about 3 ms per thousand; on proxy_serve, where each request also
  opens an origin connection, about 6 ms per thousand. This matches the
  scheduler the plan describes for today: readiness by `poll(2)` over
  every waiting task, so every wake costs time in proportion to the idle
  connections. The reactor (epoll) is meant to remove exactly this.
- **p99 passes with no idle load and fails with it.** With no idle
  connections p99 is 1.6 to 1.8 ms on kv_serve and 2.6 to 5.0 ms on
  proxy_serve at 500 to 2000 requests a second, under the 10 ms bar. With
  10000 idle connections held it is 18 to 58 ms and 72 to 87 ms.
- No request failed in this run. An earlier run with the servers on 4776x
  ports had 1 to 3 bad proxy replies per rate run; see the last point below.

## Limits of this measurement

- **This container caps descriptors at 20000** (`RLIMIT_NOFILE` soft and
  hard; raising the hard limit is not permitted here), so the top tier is
  19500 connections, not 100k. `run.sh` raises the soft limit to the hard
  one and sizes the top tier from it, so on a box with `ulimit -Hn` above
  about 101000 (and `fs.nr_open` to match) the same script measures the bar
  itself. The memory per connection above is measured; what 100k would use
  is a projection from it, not a measurement.
- **The client is Python.** Its own scheduling shows up as "client lag"
  (how late, at worst, it sent a request); when that is large, the high
  percentiles include the client's stall, not only the server's. The
  client disables Python's garbage collector during a rate run for that
  reason.
- **One machine.** Client and server share 4 CPUs over loopback, so
  network latency is absent and CPU contention is not.
- **Ports below 32768.** Linux picks source ports from 32768 to 60999. A
  connect to a dead port inside that range now and then picks that port as
  its own source and connects to itself, which made the proxy relay its own
  upstream request back to a client about once in 20k requests when these
  servers used 4776x ports. The ports here are outside the range, and
  `apps/service/rev_proxy`'s dead upstreams moved from 47740 and 47741 to
  27740 and 27741 for the same reason.
