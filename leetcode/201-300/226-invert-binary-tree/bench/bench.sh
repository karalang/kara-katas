#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #226.
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

build_rust recursive.rs
build_rust iterative.rs
build_kara recursive.kara
build_kara iterative.kara

hyperfine \
    --warmup 3 \
    --runs 10 \
    --shell=none \
    --command-name 'kara recursive (codegen)' './target/recursive_kara' \
    --command-name 'kara iterative (codegen)' './target/iterative_kara' \
    --command-name 'py   recursive'           'python3 recursive.py' \
    --command-name 'py   iterative'           'python3 iterative.py' \
    --command-name 'rust recursive'           './target/recursive' \
    --command-name 'rust iterative'           './target/iterative'

echo
echo "=== runtime memory (peak) ==="
# python's number includes ~10 MB CPython runtime baseline regardless of N;
# kara/rust are standalone compiled binaries.
print_mem 'kara recursive (codegen)' "$(mem_peak ./target/recursive_kara)"
print_mem 'kara iterative (codegen)' "$(mem_peak ./target/iterative_kara)"
print_mem 'py   recursive'           "$(mem_peak python3 recursive.py)"
print_mem 'py   iterative'           "$(mem_peak python3 iterative.py)"
print_mem 'rust recursive'           "$(mem_peak ./target/recursive)"
print_mem 'rust iterative'           "$(mem_peak ./target/iterative)"

echo
echo "=== compile memory (cold) ==="
# Artifact deleted before each measurement so the karac/rustc invocation is a
# full cold compile. karac's number covers lex → … → ownership → codegen IR
# build → LLVM optimization passes. Regression detection: a sudden 10× spike
# on `karac build` here is the signature of an algorithmic blowup in a
# frontend phase (cf. 2026-05-12 Array[T, N] Maranget O(N²) fix). karac and
# rustc are invoked directly under /usr/bin/time so rusage measures the
# compiler process itself, not a wrapping shell.
for src in recursive.kara iterative.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    print_mem "karac build $src" "$bytes"
done
for src in recursive.rs iterative.rs; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    print_mem "rustc -O $src" "$(mem_peak rustc -O "$src" -o "$out")"
done

# Note: interpreter rows are omitted (matches the 1665 / 3629 bench
# pattern). `karac run` walks a tree-of-RC-handle Option fields per
# inner iteration and 2_000 nodes × K=10 invert cycles dwarfs every
# other implementation by ~3 orders of magnitude — keeping it would
# stretch each hyperfine pass into multi-minute territory and crowd out
# the apples-to-apples codegen comparison. Spot-check interp parity
# manually with `karac run recursive.kara` at a smaller N (drop the
# `build_tree(2_000)` constant in `main` to e.g. 200).
