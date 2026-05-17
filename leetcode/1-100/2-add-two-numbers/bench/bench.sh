#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #2.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup), karac
# (with --features llvm for the codegen path).

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

mem_peak() {
    { /usr/bin/time -l "$@" >/dev/null; } 2>&1 \
        | awk '/peak memory footprint/ {print $1}'
}
print_mem() {
    local label="$1" bytes="$2"
    local mib
    mib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1048576}')
    printf '  %-34s %12s bytes (%6s MiB)\n' "$label" "$bytes" "$mib"
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

build_rust iterative.rs
build_kara iterative.kara

echo "=== runtime (iterative, N=100 digits, K=500_000) ==="
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara iterative (codegen)' './target/iterative_kara' \
    --command-name 'py   iterative'           'python3 iterative.py' \
    --command-name 'rust iterative'           './target/iterative'

echo
echo "=== binary size ==="
for spec in \
    'kara iterative (codegen):target/iterative_kara' \
    'rust iterative:target/iterative'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-30s %8s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara iterative (codegen)' "$(mem_peak ./target/iterative_kara)"
print_mem 'py   iterative'           "$(mem_peak python3 iterative.py)"
print_mem 'rust iterative'           "$(mem_peak ./target/iterative)"
