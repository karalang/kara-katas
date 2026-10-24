#!/usr/bin/env python3
"""Turn run.sh's results.jsonl into the Markdown tables in README.md.

Run as: python3 -I summarize.py results/results.jsonl
"""
import json
import sys

IDLE_BAR_CONNS = 100_000
IDLE_BAR_RSS_KIB = 1024 * 1024
P99_BAR_MS = 10.0


def mib(kib):
    return '%.1f' % (kib / 1024)


def main():
    rows = [json.loads(line) for line in open(sys.argv[1]) if line.strip()]
    idle = [r for r in rows if r['mode'] == 'idle']
    rate = [r for r in rows if r['mode'] == 'rate']
    print('### Idle connections\n')
    print('| run | asked | accepted | RSS before (MiB) | RSS held (MiB) | bytes per conn | threads | probe median (ms) | probe max (ms) |')
    print('|---|---:|---:|---:|---:|---:|---:|---:|---:|')
    for r in idle:
        print('| %s | %d | %d | %s | %s | %s | %s | %s | %s |' % (
            r['run'], r['target_conns'], r['server_accepted'], mib(r['server_rss_before_kib']),
            mib(r['server_rss_held_kib']), r['rss_per_conn_bytes'], r['server_threads_held'],
            r['probe_ms_median'], r['probe_ms_max']))
    print('\n### Fixed request rates\n')
    print('| run | measured | achieved rps | p50 (ms) | p99 (ms) | p99.9 (ms) | max (ms) | client lag (ms) | errors |')
    print('|---|---:|---:|---:|---:|---:|---:|---:|---|')
    for r in rate:
        errs = ', '.join('%s %d' % kv for kv in sorted(r['errors'].items())) or 'none'
        bad = {k: v for k, v in r['statuses'].items() if k != '200'}
        if bad:
            errs += '; ' + ', '.join('%s %d' % ('empty reply' if k == '0' else 'status ' + k, v)
                                     for k, v in sorted(bad.items()))
        print('| %s | %d | %s | %s | %s | %s | %s | %s | %s |' % (
            r['run'], r['measured'], r['achieved_rate'], r['p50_ms'], r['p99_ms'], r['p999_ms'],
            r['max_ms'], r['client_max_lag_ms'], errs))
    print('\n### Against the M4a bars\n')
    reached = [r for r in idle if r['server_accepted'] >= IDLE_BAR_CONNS]
    if reached:
        best = min(r['server_rss_held_kib'] for r in reached)
        verdict = 'PASS' if best < IDLE_BAR_RSS_KIB else 'FAIL'
        print('- Idle: %s, %s MiB held at %d connections or more.' % (verdict, mib(best), IDLE_BAR_CONNS))
    else:
        top = max(idle, key=lambda r: r['server_accepted'])
        print('- Idle: NOT MEASURED. The most connections held was %d (descriptor limit %d), short of %d.'
              % (top['server_accepted'], top['rlimit_nofile'], IDLE_BAR_CONNS))
    for target in ('kv_serve', 'proxy_serve'):
        mine = [r for r in rate if r['run'].split()[1] == target]
        if not mine:
            continue
        worst = max(mine, key=lambda r: r['p99_ms'] or 0)
        clean = all(not r['errors'] and set(r['statuses']) == {'200'} for r in mine)
        verdict = 'PASS' if worst['p99_ms'] < P99_BAR_MS and clean else 'FAIL'
        why = '' if clean else '; some requests failed or had no 200 reply'
        print('- p99 on %s: %s, worst %s ms (%s)%s.' % (target, verdict, worst['p99_ms'], worst['run'], why))


if __name__ == '__main__':
    main()
