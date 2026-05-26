#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #8.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Two-lane kata. The K=10M outer loop reduces via
# `sum += my_atoi(inputs[k % N]) as i64` — karac's auto-par-on-reduction
# recognizes the shape and emits a karac_par_reduce dispatch (binary grows
# from ~49 KiB to ~312 KiB, wall drops ~7.6× via multi-core dispatch).
# For the BENCH.md seq lane this masks the per-core codegen-vs-rustc
# comparison the kata corpus is built around, so we ship a second kara
# binary built with KARAC_AUTO_PAR=0 (codegen.rs Slice 6 gate —
# short-circuits all auto-par dispatch back to plain sequential
# compile_block; the documented mechanism for side-by-side seq-vs-par
# benchmarking of the same workload). The default binary still gets built
# so the auto-par number stays reported as the production regime.
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
    local out="target/atoi_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust     atoi.rs
build_c        atoi.c
build_kara     atoi.kara
build_kara_seq atoi.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before
# timing. Python skipped from sink check by default — at K=10M the py
# run takes ~4s and bench.sh would block on it. Set
# `KARA_BENCH_INCLUDE_PY=1` to opt in.
expected="15437323750000"
mismatch=""
for pair in \
    'kara:./target/atoi_kara' \
    'kara_seq:./target/atoi_kara_seq' \
    'rust:./target/atoi' \
    'c:./target/atoi_c' \
    'go:./target/atoi_go_seq'; do
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
    py_out=$(python3 atoi.py)
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
    --command-name 'kara atoi (seq, KARAC_AUTO_PAR=0)' './target/atoi_kara_seq' \
    --command-name 'rust atoi'                         './target/atoi' \
    --command-name 'c    atoi'                         './target/atoi_c' \
    --command-name 'go   atoi'                         './target/atoi_go_seq'

echo
echo "=== runtime — auto-par regime (kara default, multi-core) ==="
# Default `karac build` output: karac's auto-par-on-reduction recognizes
# the `sum +=` reduction in main's K=10M loop and emits a
# karac_par_reduce dispatch. Multi-core wall-time win on top of the seq
# lane. NOT directly comparable to the single-thread rows above per
# BENCH.md's two-lane discipline — reported separately so the production-
# default Kara behavior stays visible. Heavier warmup (10/50) absorbs
# worker-pool init noise that otherwise inflates σ on short auto-par runs.
hyperfine \
    --warmup 10 \
    --runs 50 \
    --shell=none \
    --command-name 'kara atoi (auto-par default)' './target/atoi_kara'

echo
echo "=== runtime — long workloads (py) ==="
hyperfine \
    --warmup 2 \
    --runs 10 \
    --shell=none \
    --command-name 'py   atoi' 'python3 atoi.py'

echo
echo "=== compile elapsed (cold) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --shell=none \
    --prepare 'rm -f target/atoi_kara atoi' \
    --command-name 'karac build atoi.kara' 'sh -c "karac build atoi.kara >/dev/null && mv atoi target/atoi_kara"' \
    --prepare 'rm -f target/atoi' \
    --command-name 'rustc -O atoi.rs'      'rustc -O atoi.rs -o target/atoi' \
    --prepare 'rm -f target/atoi_c' \
    --command-name 'clang -O3 atoi.c'      'clang -O3 atoi.c -o target/atoi_c'

echo
echo "=== binary size ==="
for spec in \
    'kara atoi (seq):target/atoi_kara_seq' \
    'kara atoi (auto-par):target/atoi_kara' \
    'rust atoi:target/atoi' \
    'c    atoi:target/atoi_c' \
    'go   atoi:target/atoi_go_seq'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-40s %10s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara atoi (seq)'      "$(mem_peak ./target/atoi_kara_seq)"
print_mem 'kara atoi (auto-par)' "$(mem_peak ./target/atoi_kara)"
print_mem 'rust atoi'            "$(mem_peak ./target/atoi)"
print_mem 'c    atoi'            "$(mem_peak ./target/atoi_c)"
print_mem 'go   atoi'            "$(mem_peak ./target/atoi_go_seq)"
print_mem 'py   atoi'            "$(mem_peak python3 atoi.py)"

echo
echo "=== compile memory (cold) ==="
for src in atoi.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    print_mem "karac build $src" "$bytes"
done
for src in atoi.rs; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    print_mem "rustc -O $src" "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in atoi.c; do
    out="target/$(basename "$src" .c)_c"
    rm -f "$out"
    print_mem "clang -O3 $src" "$(mem_peak clang -O3 "$src" -o "$out")"
done
