#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #1.
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

build_rust brute_force.rs
build_rust hash_map.rs
build_kara brute_force.kara
build_kara hash_map.kara

hyperfine \
    --warmup 3 \
    --runs 10 \
    --shell=none \
    --command-name 'kara brute_force (codegen)' './target/brute_force_kara' \
    --command-name 'kara hash_map (codegen)'    './target/hash_map_kara' \
    --command-name 'kara brute_force (interp)'  'karac run brute_force.kara' \
    --command-name 'kara hash_map (interp)'     'karac run hash_map.kara' \
    --command-name 'py   brute_force'           'python3 brute_force.py' \
    --command-name 'py   hash_map'              'python3 hash_map.py' \
    --command-name 'rust brute_force'           './target/brute_force' \
    --command-name 'rust hash_map'              './target/hash_map'

echo
echo "=== runtime memory (peak) ==="
# python's number includes ~7 MB CPython runtime baseline regardless of N.
# `interp` rows include the karac binary itself (~7 MB with --features llvm)
# plus the AST/value heap karac walks at runtime — `karac run` re-runs
# lex → … → ownership → tree-walk every invocation, so the number measures
# interpreter overhead + algorithm working set, not algorithm alone.
print_mem 'kara brute_force (codegen)' "$(mem_peak ./target/brute_force_kara)"
print_mem 'kara hash_map (codegen)'    "$(mem_peak ./target/hash_map_kara)"
print_mem 'kara brute_force (interp)'  "$(mem_peak karac run brute_force.kara)"
print_mem 'kara hash_map (interp)'     "$(mem_peak karac run hash_map.kara)"
print_mem 'py   brute_force'           "$(mem_peak python3 brute_force.py)"
print_mem 'py   hash_map'              "$(mem_peak python3 hash_map.py)"
print_mem 'rust brute_force'           "$(mem_peak ./target/brute_force)"
print_mem 'rust hash_map'              "$(mem_peak ./target/hash_map)"

echo
echo "=== compile memory (cold) ==="
# Artifact deleted before each measurement so the karac/rustc invocation is a
# full cold compile. karac's number covers lex → … → ownership → codegen IR
# build → LLVM optimization passes. Regression detection: a sudden 10× spike
# on `karac build` here is the signature of an algorithmic blowup in a
# frontend phase (cf. 2026-05-12 Array[T, N] Maranget O(N²) fix). karac and
# rustc are invoked directly under /usr/bin/time so rusage measures the
# compiler process itself, not a wrapping shell.
for src in brute_force.kara hash_map.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    print_mem "karac build $src" "$bytes"
done
for src in brute_force.rs hash_map.rs; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    print_mem "rustc -O $src" "$(mem_peak rustc -O "$src" -o "$out")"
done
