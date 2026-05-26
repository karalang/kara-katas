#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #6.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Two-lane kata. The per-call `convert_off` work (one push per input
# char + one flatten copy = 2N ops per call, ~20 µs at N=10K) is large
# enough that the K=10K outer loop's reduction (`sum += result[0] +
# result[N-1]`) amortizes par-dispatch overhead cleanly — karac's
# auto-par-on-reduction recognizes the shape and emits a karac_par_reduce
# dispatch. We ship a second kara binary built with KARAC_AUTO_PAR=0 for
# the BENCH.md seq lane apples-to-apples row.
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

# Sequential variant — karac's auto-par-on-reduction recognizes
# `sum += result[0] + result[N-1]` in main's K=10K loop and emits a
# karac_par_reduce dispatch (binary grows from ~50 KiB to ~312 KiB,
# wall drops ~4× via multi-core dispatch). For the BENCH.md seq lane
# this masks the per-core codegen-vs-rustc comparison the kata corpus
# is built around, so we ship a second kara binary built with
# KARAC_AUTO_PAR=0 (codegen.rs Slice 6 gate — short-circuits all auto-par
# dispatch back to plain sequential compile_block; the documented
# mechanism for side-by-side seq-vs-par benchmarking of the same
# workload). The default binary still gets built above so the auto-par
# number stays reported as the production regime.
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
    local out="target/row_buffers_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust     row_buffers.rs
build_c        row_buffers.c
build_kara     row_buffers.kara
build_kara_seq row_buffers.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before
# timing. Python skipped from sink check by default — at K=10K the py
# run takes ~3.3s and bench.sh would block on it. Set
# `KARA_BENCH_INCLUDE_PY=1` to opt in.
expected="1514240"
mismatch=""
for pair in \
    'kara:./target/row_buffers_kara' \
    'kara_seq:./target/row_buffers_kara_seq' \
    'rust:./target/row_buffers' \
    'c:./target/row_buffers_c' \
    'go:./target/row_buffers_go_seq'; do
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
    py_out=$(python3 row_buffers.py)
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
    --command-name 'kara row_buffers (seq, KARAC_AUTO_PAR=0)' './target/row_buffers_kara_seq' \
    --command-name 'rust row_buffers'                         './target/row_buffers' \
    --command-name 'c    row_buffers'                         './target/row_buffers_c' \
    --command-name 'go   row_buffers'                         './target/row_buffers_go_seq'

echo
echo "=== runtime — auto-par regime (kara default, multi-core) ==="
# Default `karac build` output: karac's auto-par-on-reduction recognizes
# the `sum +=` reduction in main's K=10K loop and emits a
# karac_par_reduce dispatch. Multi-core wall-time win on top of the seq
# lane. NOT directly comparable to the single-thread rows above per
# BENCH.md's two-lane discipline — reported separately so the production-
# default Kara behavior stays visible.
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara row_buffers (auto-par default)' './target/row_buffers_kara'

echo
echo "=== runtime — long workloads (py) ==="
hyperfine \
    --warmup 2 \
    --runs 10 \
    --shell=none \
    --command-name 'py   row_buffers' 'python3 row_buffers.py'

echo
echo "=== compile elapsed (cold) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --shell=none \
    --prepare 'rm -f target/row_buffers_kara row_buffers' \
    --command-name 'karac build row_buffers.kara' 'sh -c "karac build row_buffers.kara >/dev/null && mv row_buffers target/row_buffers_kara"' \
    --prepare 'rm -f target/row_buffers' \
    --command-name 'rustc -O row_buffers.rs'      'rustc -O row_buffers.rs -o target/row_buffers' \
    --prepare 'rm -f target/row_buffers_c' \
    --command-name 'clang -O3 row_buffers.c'      'clang -O3 row_buffers.c -o target/row_buffers_c'

echo
echo "=== binary size ==="
for spec in \
    'kara row_buffers (seq):target/row_buffers_kara_seq' \
    'kara row_buffers (auto-par):target/row_buffers_kara' \
    'rust row_buffers:target/row_buffers' \
    'c    row_buffers:target/row_buffers_c' \
    'go   row_buffers:target/row_buffers_go_seq'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-40s %10s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara row_buffers (seq)'      "$(mem_peak ./target/row_buffers_kara_seq)"
print_mem 'kara row_buffers (auto-par)' "$(mem_peak ./target/row_buffers_kara)"
print_mem 'rust row_buffers'            "$(mem_peak ./target/row_buffers)"
print_mem 'c    row_buffers'            "$(mem_peak ./target/row_buffers_c)"
print_mem 'go   row_buffers'            "$(mem_peak ./target/row_buffers_go_seq)"
print_mem 'py   row_buffers'            "$(mem_peak python3 row_buffers.py)"

echo
echo "=== compile memory (cold) ==="
for src in row_buffers.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    print_mem "karac build $src" "$bytes"
done
for src in row_buffers.rs; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    print_mem "rustc -O $src" "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in row_buffers.c; do
    out="target/$(basename "$src" .c)_c"
    rm -f "$out"
    print_mem "clang -O3 $src" "$(mem_peak clang -O3 "$src" -o "$out")"
done
