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

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
# All four comparators here run single-threaded. The kara binary built
# with KARAC_AUTO_PAR=0 short-circuits auto-par dispatch back to plain
# sequential codegen — this is the row directly comparable to rustc -O /
# clang -O3 / go build on a per-core codegen-quality basis.
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara valid (seq, KARAC_AUTO_PAR=0)' './target/valid_kara_seq' \
    --command-name 'rust valid'                        './target/valid' \
    --command-name 'c    valid'                        './target/valid_c' \
    --command-name 'go   valid'                        './target/valid_go_seq'

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
hyperfine \
    --warmup 10 \
    --runs 50 \
    --shell=none \
    --command-name 'kara valid (auto-par default)' './target/valid_kara'

echo
echo "=== runtime — long workloads (py) ==="
hyperfine \
    --warmup 2 \
    --runs 10 \
    --shell=none \
    --command-name 'py   valid' 'python3 valid.py'

echo
echo "=== compile elapsed (cold) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --shell=none \
    --prepare 'rm -f target/valid_kara valid' \
    --command-name 'karac build valid.kara' 'sh -c "karac build valid.kara >/dev/null && mv valid target/valid_kara"' \
    --prepare 'rm -f target/valid' \
    --command-name 'rustc -O valid.rs'      'rustc -O valid.rs -o target/valid' \
    --prepare 'rm -f target/valid_c' \
    --command-name 'clang -O3 valid.c'      'clang -O3 valid.c -o target/valid_c'

echo
echo "=== binary size ==="
for spec in \
    'kara valid (seq):target/valid_kara_seq' \
    'kara valid (auto-par):target/valid_kara' \
    'rust valid:target/valid' \
    'c    valid:target/valid_c' \
    'go   valid:target/valid_go_seq'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-40s %10s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara valid (seq)'      "$(mem_peak ./target/valid_kara_seq)"
print_mem 'kara valid (auto-par)' "$(mem_peak ./target/valid_kara)"
print_mem 'rust valid'            "$(mem_peak ./target/valid)"
print_mem 'c    valid'            "$(mem_peak ./target/valid_c)"
print_mem 'go   valid'            "$(mem_peak ./target/valid_go_seq)"
print_mem 'py   valid'            "$(mem_peak python3 valid.py)"

echo
echo "=== compile memory (cold) ==="
for src in valid.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    print_mem "karac build $src" "$bytes"
done
for src in valid.rs; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    print_mem "rustc -O $src" "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in valid.c; do
    out="target/$(basename "$src" .c)_c"
    rm -f "$out"
    print_mem "clang -O3 $src" "$(mem_peak clang -O3 "$src" -o "$out")"
done
