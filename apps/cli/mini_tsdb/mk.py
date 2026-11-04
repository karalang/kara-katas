"""Writes data/ for mini_tsdb: an hour of Prometheus scrapes from three
hosts (one file per host), a file of late and broken samples, and the
queries to run.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)

T0 = 1700000000000
seed = 7


def rnd(n):
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return (seed // 65536) % n


def host(name, down, reset):
    lines = [f"# scrapes of {name}, every 15 s for an hour"]
    reqs = {"200": 1000 * (1 + rnd(9)), "500": rnd(40)}
    temp = 400 + rnd(80)
    depth = rnd(20)
    for k in range(240):
        if down[0] <= k < down[1]:
            continue
        ts = T0 + k * 15000 + (rnd(7) - 3)
        if k == reset:
            reqs = {"200": 0, "500": 0}
            lines.append(f"# {name} restarted: its counters start again from zero")
        reqs["200"] += 50 + rnd(120)
        reqs["500"] += rnd(4) if k % 10 else 0
        temp = max(300, min(950, temp + rnd(21) - 10))
        depth = max(0, depth + rnd(9) - 4)
        for code in ("200", "500"):
            lines.append(f'http_requests_total{{job="api",instance="{name}",code="{code}"}} {reqs[code]} {ts}')
        lines.append(f'node_cpu_temp{{instance="{name}"}} {temp // 10}.{temp % 10} {ts}')
        lines.append(f'queue_depth{{instance="{name}",job="worker"}} {depth} {ts}')
    return "\n".join(lines) + "\n"


files = {
    "h1.prom": host("h1", (0, 0), -1),
    "h2.prom": host("h2", (100, 112), -1),
    "h3.prom": host("h3", (0, 0), 130),
    "zz_late.prom": f"""# A scrape that arrived late, and some broken lines.
node_cpu_temp{{instance="h1"}} 55.5 {T0 + 1200000}
node_cpu_temp{{instance="h4"}} 39.0 {T0 + 1200000}
queue_depth{{instance="h2",job="worker"}} 3 {T0 + 30000}
http_requests_total{{job="api",instance="h1",code="200"}} 1 {T0 + 1800000}
node_cpu_temp{{instance="h4"}} 39.0 {T0 + 1200000}
node_cpu_temp{{instance="h4"}} 39.5 {T0 + 1200000}
node_cpu_temp{{instance="h4"}} 40.25 {T0 + 1215000}
node_cpu_temp{{instance=h4}} 40.0 {T0 + 1230000}
node_cpu_temp{{instance="h4"}} warm {T0 + 1230000}
node_cpu_temp{{instance="h4"}} 40.0
{{instance="h4"}} 40.0 {T0 + 1230000}
""",
    "queries.promql": """# instant <seconds> <expr>, or range <start> <end> <step> <expr>;
# seconds count from the first scrape.
instant 600 node_cpu_temp
instant 600 node_cpu_temp{instance="h2"}
instant 1590 queue_depth{instance="h2"}
instant 3599 http_requests_total{code="500"}
instant 1800 rate(http_requests_total[5m])
instant 1800 sum by (code) (rate(http_requests_total[5m]))
instant 2100 increase(http_requests_total{instance="h3"}[10m])
instant 1800 rate(http_requests_total{code="200"}[1m]) * 60
range 600 1200 300 avg_over_time(node_cpu_temp[5m])
range 0 3600 900 max by (instance) (max_over_time(queue_depth[15m]))
instant 1800 sum(queue_depth)
instant 1800 avg by (job) (queue_depth)
instant 1800 count_over_time(queue_depth{instance!="h1"}[1m])
instant 1800 min_over_time(node_cpu_temp{instance!="h4"}[1h]) / 10
instant 1230 node_cpu_temp{instance="h4"}
instant 5000 node_cpu_temp
instant 1800 nosuch_metric
instant 1800 rate(node_cpu_temp)
instant 1800 sum by code (queue_depth)
range 100 50 10 queue_depth
""",
}
for name, text in files.items():
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
