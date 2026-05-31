#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #65.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Two-lane kata. The K=10M outer loop's body is the conditional accumulator
# update `if r { sum = sum + 1i64; }`. karac's slice-1 analyzer (commit
# 3294e50, 2026-05-20) recognizes this as a +-reduction and emits a
# karac_par_reduce dispatch (binary grows from ~49 KiB to ~312 KiB, wall
# drops ~7× via multi-core dispatch). For the BENCH.md seq lane this
# masks the per-core codegen-vs-rustc comparison the kata corpus is
# built around, so we ship a second kara binary built with KARAC_AUTO_PAR=0
# (codegen.rs Slice 6 gate — short-circuits all auto-par dispatch back to
# plain sequential compile_block; the documented mechanism for side-by-side
# seq-vs-par benchmarking of the same workload). The default binary still
# gets built so the auto-par number stays reported as the production regime.
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup), clang,
# go, karac (with --features llvm for the codegen path).

set -euo pipefail
cd "$(dirname "$0")"

require() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "$1 not found — install with: $2" >&2
        exit 1
    fi
}

require hyperfine "brew install hyperfine"
require rustc     "rustup (https://rustup.rs) or 'brew install rustup-init'"
require clang     "xcode-select --install (macOS) or your distro's clang package"
require go        "brew install go  or your distro's golang package"
require karac     "cargo install --path . --features llvm  (from karac-rust checkout)"

# Structured-JSON emission (writes bench/results.json). Set BENCH_JSON=0 to
# skip — the human-readable console output below is unaffected either way.
if [ "${BENCH_JSON:-1}" = "1" ]; then
    require jq      "brew install jq"
    require python3 "python3 ships with macOS; or 'brew install python'"
fi
ROOT="$(cd ../../../.. && pwd)"
. "$ROOT/scripts/bench-lib.sh"

mem_peak() {
    { /usr/bin/time -l "$@" >/dev/null; } 2>&1 \
        | awk '/peak memory footprint/ {print $1}'
}
print_mem() {
    local label="$1" bytes="$2"
    local mib
    mib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1048576}')
    printf '  %-40s %12s bytes (%6s MiB)\n' "$label" "$bytes" "$mib"
}

mkdir -p target

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

build_kara() {
    local src="$1"
    local stem="$(basename "$src" .kara)"
    local out="target/${stem}_kara"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling $src (auto-par default) ..." >&2
        karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

build_kara_seq() {
    local src="$1"
    local stem="$(basename "$src" .kara)"
    local out="target/${stem}_kara_seq"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling $src (KARAC_AUTO_PAR=0, seq lane) ..." >&2
        KARAC_AUTO_PAR=0 karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

build_go_seq() {
    local out="target/valid_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust     valid.rs
build_c        valid.c
build_kara     valid.kara
build_kara_seq valid.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before
# timing. Python skipped from sink check by default — at K=10M the py
# run takes ~3s and bench.sh would block on it. Set
# `KARA_BENCH_INCLUDE_PY=1` to opt in.
expected="6250000"
mismatch=""
for pair in \
    'kara:./target/valid_kara' \
    'kara_seq:./target/valid_kara_seq' \
    'rust:./target/valid' \
    'c:./target/valid_c' \
    'go:./target/valid_go_seq'; do
    name="${pair%%:*}"
    cmd="${pair#*:}"
    out=$("$cmd")
    if [ "$out" != "$expected" ]; then
        mismatch="$mismatch ${name}=${out}"
    fi
done
if [ -n "$mismatch" ]; then
    echo "sink mismatch (expected=$expected):$mismatch" >&2
    exit 1
fi
echo "sink (kara/kara_seq/rust/c/go): $expected"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_out=$(python3 valid.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=65 slug=valid-number group=1-100 \
    title="Valid Number" workload="K=10M validation passes" \
    sink="$expected"

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
# All four comparators here run single-threaded. The kara binary built
# with KARAC_AUTO_PAR=0 short-circuits auto-par dispatch back to plain
# sequential codegen — this is the row directly comparable to rustc -O /
# clang -O3 / go build on a per-core codegen-quality basis.
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach valid --lane seq --mode codegen \
    --name 'kara valid (seq, KARAC_AUTO_PAR=0)' --cmd './target/valid_kara_seq'
rt_cmd --lang rust --approach valid --lane seq --mode native \
    --name 'rust valid' --cmd './target/valid'
rt_cmd --lang c --approach valid --lane seq --mode native \
    --name 'c    valid' --cmd './target/valid_c'
rt_cmd --lang go --approach valid --lane seq --mode native \
    --name 'go   valid' --cmd './target/valid_go_seq'
rt_end

echo
echo "=== runtime — auto-par regime (kara default, multi-core) ==="
# Default `karac build` output: karac's auto-par-on-reduction recognizes
# the `if r { sum = sum + 1i64; }` conditional accumulator update in main's
# K=10M loop and emits a karac_par_reduce dispatch. Multi-core wall-time
# win on top of the seq lane. NOT directly comparable to the single-thread
# rows above per BENCH.md's two-lane discipline — reported separately so
# the production-default Kara behavior stays visible. Heavier warmup (10/50)
# absorbs worker-pool init noise that otherwise inflates σ on short
# auto-par runs.
rt_begin --warmup 10 --runs 50
rt_cmd --lang kara --approach valid --lane par --mode codegen \
    --name 'kara valid (auto-par default)' --cmd './target/valid_kara'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach valid --lane seq --mode interp \
    --name 'py   valid' --cmd 'python3 valid.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach valid --mode codegen \
    --prepare 'rm -f target/valid_kara valid' \
    --name 'karac build valid.kara' \
    --cmd 'sh -c "karac build valid.kara >/dev/null && mv valid target/valid_kara"'
ce_cmd --lang rust --approach valid --mode native \
    --prepare 'rm -f target/valid' \
    --name 'rustc -O valid.rs' --cmd 'rustc -O valid.rs -o target/valid'
ce_cmd --lang c --approach valid --mode native \
    --prepare 'rm -f target/valid_c' \
    --name 'clang -O3 valid.c' --cmd 'clang -O3 valid.c -o target/valid_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach valid --lane seq --mode codegen --path target/valid_kara_seq
size_put --lang kara --approach valid --lane par --mode codegen --path target/valid_kara
size_put --lang rust --approach valid --lane seq --mode native  --path target/valid
size_put --lang c    --approach valid --lane seq --mode native  --path target/valid_c
size_put --lang go   --approach valid --lane seq --mode native  --path target/valid_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach valid --lane seq --mode codegen --bytes "$(mem_peak ./target/valid_kara_seq)"
mem_put --lang kara --approach valid --lane par --mode codegen --bytes "$(mem_peak ./target/valid_kara)"
mem_put --lang rust --approach valid --lane seq --mode native  --bytes "$(mem_peak ./target/valid)"
mem_put --lang c    --approach valid --lane seq --mode native  --bytes "$(mem_peak ./target/valid_c)"
mem_put --lang go   --approach valid --lane seq --mode native  --bytes "$(mem_peak ./target/valid_go_seq)"
mem_put --lang python --approach valid --lane seq --mode interp --bytes "$(mem_peak python3 valid.py)"

echo
echo "=== compile memory (cold) ==="
for src in valid.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach valid --mode codegen --bytes "$bytes"
done
for src in valid.rs; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    cmem_put --lang rust --approach valid --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in valid.c; do
    out="target/$(basename "$src" .c)_c"
    rm -f "$out"
    cmem_put --lang c --approach valid --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
