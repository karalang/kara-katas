#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #91 (Decode Ways).
# See ../README.md § Benchmarks for what these numbers mean.
#
# Workload: 100 fixed-content digit strings of length 80, 200_000 hot-loop
# calls to decode_ways indexing strings[i % 100], sum reduced mod 1e9+7.
# Sink: one line, the final reduced sum (must match across mirrors before
# anything is timed).
#
# Seq-only kata: the DP's rolling-window state (prev1/prev2) carries a
# strict cross-iteration dependency, so the par lane doesn't apply per
# BENCH.md § Par lane.
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup),
# clang (xcode-select --install), go, karac.

set -euo pipefail
cd "$(dirname "$0")"

require() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "$1 not found — install with: $2" >&2
        exit 1
    fi
}

require hyperfine "brew install hyperfine"
require rustc     "rustup (https://rustup.rs)"
require clang     "xcode-select --install / your distro's clang"
require go        "brew install go / your distro's golang"
require karac     "cargo install --path . --features llvm  (from karac-rust)"

# Structured-JSON emission (writes bench/results.json). Set BENCH_JSON=0 to
# skip — the human-readable console output below is unaffected either way.
if [ "${BENCH_JSON:-1}" = "1" ]; then
    require jq      "brew install jq"
    require python3 "python3 ships with macOS; or 'brew install python'"
fi
ROOT="$(cd ../../../.. && pwd)"
. "$ROOT/scripts/bench-lib.sh"

# /usr/bin/time -l (macOS BSD time) prints a "peak memory footprint" line
# on stderr. Single sample — memory is stable run-to-run.
mem_peak() {
    { /usr/bin/time -l "$@" >/dev/null; } 2>&1 \
        | awk '/peak memory footprint/ {print $1}'
}
print_mem() {
    local label="$1" bytes="$2"
    local mib
    mib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1048576}')
    printf '  %-30s %12s bytes (%6s MiB)\n' "$label" "$bytes" "$mib"
}

mkdir -p target

build_kara() {
    local src="$1"
    local stem="$(basename "$src" .kara)"
    local out="target/${stem}_kara"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling $src ..." >&2
        rm -f "$stem"
        karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

build_rust() {
    local src="$1"
    local out="target/$(basename "$src" .rs)"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src ..." >&2
        rustc -O "$src" -o "$out"
    fi
}

build_c() {
    local src="$1"
    local out="target/$(basename "$src" .c)_c"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src ..." >&2
        clang -O3 "$src" -o "$out"
    fi
}

build_go() {
    local dir="$1"
    local out="target/$(basename "$dir" | tr '-' '_')"
    if [ ! -x "$out" ] || [ "$dir/main.go" -nt "$out" ]; then
        echo "compiling $dir ..." >&2
        ( cd "$dir" && go build -o "../$out" . )
    fi
}

build_kara decode_ways.kara
build_rust decode_ways.rs
build_c    decode_ways.c
build_go   go-seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
# Python is gated behind KARA_BENCH_INCLUDE_PY=1 because at 200_000 calls the
# Python run dominates wall time, and the comparison framing already includes
# the codegen langs as the load-bearing lane.
kara_sink=$(./target/decode_ways_kara)
rust_sink=$(./target/decode_ways)
c_sink=$(./target/decode_ways_c)
go_seq_sink=$(./target/go_seq)
mismatch=""
for pair in "rust:$rust_sink" "c:$c_sink" "go_seq:$go_seq_sink"; do
    name="${pair%%:*}"
    sink="${pair#*:}"
    if [ "$sink" != "$kara_sink" ]; then
        mismatch="$mismatch $name=$sink"
    fi
done
if [ -n "$mismatch" ]; then
    echo "sink mismatch (vs kara=$kara_sink):$mismatch" >&2
    exit 1
fi
echo "sink (kara == rust == c == go-seq): $kara_sink"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_sink=$(python3 decode_ways.py)
    if [ "$kara_sink" != "$py_sink" ]; then
        echo "python sink mismatch: kara=$kara_sink py=$py_sink" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=91 slug=decode-ways group=1-100 \
    title="Decode Ways" \
    workload="100 strings len 80, 200_000 hot-loop calls, sum mod 1e9+7" \
    sink="$kara_sink"

# === runtime ===
# Workload sits in the long-bucket for kara (~10s) but short-bucket for
# rust/c/go (~10ms). Per BENCH.md § Hyperfine discipline, long workloads
# get --warmup 2 --runs 10 (kara dominates the wall here, and at >1s
# RSD is already <2%); rust/c/go each finish their 10 runs in well under
# a second of total wall, so the conservative bucket is honest for all.
echo "=== runtime ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang kara --approach decode_ways --lane seq --mode codegen \
    --name 'kara decode_ways' --cmd './target/decode_ways_kara'
rt_cmd --lang rust --approach decode_ways --lane seq --mode native \
    --name 'rust decode_ways (rustc -O)' --cmd './target/decode_ways'
rt_cmd --lang c --approach decode_ways --lane seq --mode native \
    --name 'c    decode_ways (clang -O3)' --cmd './target/decode_ways_c'
rt_cmd --lang go --approach decode_ways --lane seq --mode native \
    --name 'go   decode_ways' --cmd './target/go_seq'
rt_end
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    echo
    echo "=== runtime — python (opt-in) ==="
    rt_begin --warmup 2 --runs 10
    rt_cmd --lang python --approach decode_ways --lane seq --mode interp \
        --name 'py   decode_ways' --cmd 'python3 decode_ways.py'
    rt_end
fi

echo
echo "=== compile elapsed (cold) ==="
# Per BENCH.md: --warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none.
# Multi-file Go module deliberately omitted — its first build mixes module
# resolution + std-lib link with codegen, not comparable to a single-file
# rustc/clang/karac invocation.
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach decode_ways --mode codegen \
    --prepare 'rm -f target/decode_ways_kara decode_ways' \
    --name 'karac build decode_ways.kara' \
    --cmd 'sh -c "karac build decode_ways.kara >/dev/null && mv decode_ways target/decode_ways_kara"'
ce_cmd --lang rust --approach decode_ways --mode native \
    --prepare 'rm -f target/decode_ways' \
    --name 'rustc -O decode_ways.rs' --cmd 'rustc -O decode_ways.rs -o target/decode_ways'
ce_cmd --lang c --approach decode_ways --mode native \
    --prepare 'rm -f target/decode_ways_c' \
    --name 'clang -O3 decode_ways.c' --cmd 'clang -O3 decode_ways.c -o target/decode_ways_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach decode_ways --lane seq --mode codegen --path target/decode_ways_kara
size_put --lang rust --approach decode_ways --lane seq --mode native  --path target/decode_ways
size_put --lang c    --approach decode_ways --lane seq --mode native  --path target/decode_ways_c
size_put --lang go   --approach decode_ways --lane seq --mode native  --path target/go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach decode_ways --lane seq --mode codegen --bytes "$(mem_peak ./target/decode_ways_kara)"
mem_put --lang rust --approach decode_ways --lane seq --mode native  --bytes "$(mem_peak ./target/decode_ways)"
mem_put --lang c    --approach decode_ways --lane seq --mode native  --bytes "$(mem_peak ./target/decode_ways_c)"
mem_put --lang go   --approach decode_ways --lane seq --mode native  --bytes "$(mem_peak ./target/go_seq)"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    mem_put --lang python --approach decode_ways --lane seq --mode interp --bytes "$(mem_peak python3 decode_ways.py)"
fi

echo
echo "=== compile memory (cold) ==="
rm -f target/decode_ways_kara decode_ways
cmem_put --lang kara --approach decode_ways --mode codegen --bytes "$(mem_peak karac build decode_ways.kara)"
mv decode_ways target/decode_ways_kara 2>/dev/null || true
rm -f target/decode_ways
cmem_put --lang rust --approach decode_ways --mode native --bytes "$(mem_peak rustc -O decode_ways.rs -o target/decode_ways)"
rm -f target/decode_ways_c
cmem_put --lang c --approach decode_ways --mode native --bytes "$(mem_peak clang -O3 decode_ways.c -o target/decode_ways_c)"

echo
bench_emit
