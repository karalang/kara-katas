#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #3629.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup), karac.

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
require karac     "cargo install --path . --features llvm  (from karac-rust checkout)"

# /usr/bin/time -l (macOS BSD time) prints a "peak memory footprint" line on
# stderr. We capture its stderr through a brace-group redirect, discard the
# wrapped command's own stdout, and parse the bytes column. Memory is much
# more stable run-to-run than wall-time (no scheduling/cache variance), so a
# single sample is honest — no hyperfine-style averaging needed.
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

build_rust() {
    local src="$1"
    local out="target/$(basename "$src" .rs)"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src ..." >&2
        rustc -O "$src" -o "$out"
    fi
}

build_kara() {
    local src="$1"
    local stem="$(basename "$src" .kara)"
    local out="target/${stem}_kara"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src ..." >&2
        karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

build_rust bfs_sieve.rs
build_kara bfs_sieve.kara

hyperfine \
    --warmup 2 \
    --runs 10 \
    --shell=none \
    --command-name 'kara bfs_sieve (codegen)' './target/bfs_sieve_kara' \
    --command-name 'py   bfs_sieve'           'python3 bfs_sieve.py' \
    --command-name 'rust bfs_sieve'           './target/bfs_sieve'

echo
echo "=== runtime memory (peak) ==="
# python's number includes ~10 MB CPython runtime baseline regardless of N;
# kara/rust are standalone compiled binaries. The cap-=10^6 sieve buffer
# dominates the working set across all three implementations.
print_mem 'kara bfs_sieve (codegen)' "$(mem_peak ./target/bfs_sieve_kara)"
print_mem 'py   bfs_sieve'           "$(mem_peak python3 bfs_sieve.py)"
print_mem 'rust bfs_sieve'           "$(mem_peak ./target/bfs_sieve)"

echo
echo "=== compile memory (cold) ==="
# Artifact deleted before each measurement so the karac/rustc invocation is a
# full cold compile. karac's number covers lex → … → ownership → codegen IR
# build → LLVM optimization passes. Regression detection: a sudden 10× spike
# on `karac build` here is the signature of an algorithmic blowup in a
# frontend phase (cf. 2026-05-12 Array[T, N] Maranget O(N²) fix — bfs_sieve
# is the workload that surfaced that bug, OOM'd at >41 GB RSS pre-fix).
# karac and rustc are invoked directly under /usr/bin/time so rusage
# measures the compiler process itself, not a wrapping shell.
rm -f target/bfs_sieve_kara bfs_sieve
bytes=$(mem_peak karac build bfs_sieve.kara)
mv bfs_sieve target/bfs_sieve_kara 2>/dev/null || true
print_mem 'karac build bfs_sieve.kara' "$bytes"
rm -f target/bfs_sieve
print_mem 'rustc -O bfs_sieve.rs' "$(mem_peak rustc -O bfs_sieve.rs -o target/bfs_sieve)"
