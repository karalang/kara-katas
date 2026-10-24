#!/usr/bin/env bash
# The M4a load test: idle connections held and p99 latency at fixed rates,
# against the two Kāra servers in this directory. Linux only (it reads
# /proc). See README.md for what it measures and the bars.
#
#   bash run.sh [results-dir]
#
# KARAC names the compiler (default: karac on PATH). TIERS lists the idle
# connection counts (default 1000 5000 10000 and the descriptor cap);
# RATES the request rates; RATE_SECONDS how long each rate runs.
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
out=${1:-$here/results}
karac=${KARAC:-karac}
rates=${RATES:-"500 1000 2000"}
rate_seconds=${RATE_SECONDS:-30}
held_idle=${HELD_IDLE:-10000}
client="python3 -I -B $here/loadclient.py"
mkdir -p "$out/bin"

[ "$(uname -s)" = Linux ] || { echo "run.sh needs Linux (/proc)" >&2; exit 1; }

# Every connection is a descriptor in the server and one in the client, so
# the soft RLIMIT_NOFILE caps a tier. Raise it to the hard limit; a box that
# should reach 100k needs `ulimit -Hn` above that first.
ulimit -n "$(ulimit -Hn)" 2>/dev/null || true
nofile=$(ulimit -n)
cap=$((nofile - 500))
tiers=${TIERS:-"1000 5000 10000 $cap"}

for s in kv_serve proxy_serve; do
    "$karac" build "$here/$s.kara" -o "$out/bin/$s" > "$out/bin/$s.build.log" 2>&1 \
        || { cat "$out/bin/$s.build.log" >&2; exit 1; }
done

server_pid=
start_server() {  # name port
    "$out/bin/$1" > "$out/$1.log" 2>&1 &
    server_pid=$!
    for _ in $(seq 100); do
        if (exec 3<>"/dev/tcp/127.0.0.1/$2") 2>/dev/null; then return 0; fi
        python3 -c 'import time; time.sleep(0.1)'
    done
    echo "$1 did not start listening on $2" >&2
    exit 1
}
stop_server() {
    kill "$server_pid" 2>/dev/null || true
    wait "$server_pid" 2>/dev/null || true
}
trap stop_server EXIT

kv_probe='GET /kv/k1 HTTP/1.1\r\nHost: kv\r\n\r\n'
proxy_probe='GET /api/users/7 HTTP/1.1\r\nHost: shop.test\r\n\r\n'

results="$out/results.jsonl"
: > "$results"
note() {  # label json
    python3 -I -c 'import json, sys; d = json.loads(sys.argv[2]); d["run"] = sys.argv[1]; print(json.dumps(d))' "$1" "$2" | tee -a "$results"
}

{
    echo "date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "kernel: $(uname -r)"
    echo "cpus: $(nproc)"
    echo "mem_kib: $(awk '/MemTotal/{print $2}' /proc/meminfo)"
    echo "rlimit_nofile: $nofile"
    echo "ip_local_port_range: $(cat /proc/sys/net/ipv4/ip_local_port_range | tr '\t' ' ')"
    echo "somaxconn: $(cat /proc/sys/net/core/somaxconn)"
    echo "karac: $("$karac" --version 2>&1 | head -1)"
} > "$out/machine.txt"

# 1. Idle connections, one fresh server per tier.
for name in kv_serve proxy_serve; do
    if [ $name = kv_serve ]; then port=27760; probe=$kv_probe; close=; else port=27761; probe=$proxy_probe; close=--probe-close; fi
    for n in $tiers; do
        start_server $name $port
        note "idle $name $n" "$($client idle --pid "$server_pid" --port $port --conns "$n" --probe-request "$probe" $close)"
        stop_server
    done
done

# 2. Fixed request rates, with no idle connections and then with
#    $held_idle idle connections held open for the whole run.
for name in kv_serve proxy_serve; do
    if [ $name = kv_serve ]; then port=27760; target=kv; probe=$kv_probe; close=; else port=27761; target=proxy; probe=$proxy_probe; close=--probe-close; fi
    start_server $name $port
    for r in $rates; do
        note "rate $name $r" "$($client rate --target $target --port $port --rate "$r" --seconds "$rate_seconds")"
    done
    stop_server
    start_server $name $port
    nrates=$(echo $rates | wc -w)
    hold=$((nrates * (rate_seconds + 5) + 20))
    $client idle --pid "$server_pid" --port $port --conns "$held_idle" --hold "$hold" --probes 0 \
        --probe-request "$probe" $close > "$out/held.json" &
    idle_pid=$!
    # The ramp to 10k takes well under a second; give it and the accepts 15 s.
    python3 -c 'import time; time.sleep(15)'
    for r in $rates; do
        note "rate $name $r with $held_idle idle" "$($client rate --target $target --port $port --rate "$r" --seconds "$rate_seconds")"
    done
    wait $idle_pid
    note "idle $name $held_idle during rates" "$(cat "$out/held.json")"
    rm -f "$out/held.json"
    stop_server
done

python3 -I "$here/summarize.py" "$results" > "$out/summary.md"
cat "$out/summary.md"
