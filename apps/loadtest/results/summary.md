### Idle connections

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

### Fixed request rates

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

### Against the M4a bars

- Idle: NOT MEASURED. The most connections held was 19500 (descriptor limit 20000), short of 100000.
- p99 on kv_serve: FAIL, worst 58.148 ms (rate kv_serve 2000 with 10000 idle).
- p99 on proxy_serve: FAIL, worst 87.086 ms (rate proxy_serve 2000 with 10000 idle).
