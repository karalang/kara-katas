#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #3.
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

build_rust sliding_window.rs
build_kara sliding_window.kara

echo "=== runtime ==="
hyperfine \
    --warmup 3 \
    --runs 10 \
    --shell=none \
    --command-name 'kara sliding_window (codegen)' './target/sliding_window_kara' \
    --command-name 'py   sliding_window'           'python3 sliding_window.py' \
    --command-name 'rust sliding_window'           './target/sliding_window'

echo
echo "=== compile (cold, no cache) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --prepare 'rm -f target/sliding_window_kara sliding_window' \
    --command-name 'karac build sliding_window.kara' 'sh -c "karac build sliding_window.kara >/dev/null && mv sliding_window target/sliding_window_kara"' \
    --prepare 'rm -f target/sliding_window' \
    --command-name 'rustc -O sliding_window.rs'      'rustc -O sliding_window.rs -o target/sliding_window'

echo
echo "=== binary size ==="
for spec in 'kara sliding_window:target/sliding_window_kara' 'rust sliding_window:target/sliding_window'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-21s %8s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara sliding_window (codegen)' "$(mem_peak ./target/sliding_window_kara)"
print_mem 'py   sliding_window'           "$(mem_peak python3 sliding_window.py)"
print_mem 'rust sliding_window'           "$(mem_peak ./target/sliding_window)"

echo
echo "=== compile memory (cold) ==="
rm -f target/sliding_window_kara sliding_window
print_mem 'karac build sliding_window.kara' "$(mem_peak karac build sliding_window.kara)"
mv sliding_window target/sliding_window_kara 2>/dev/null || true
rm -f target/sliding_window
print_mem 'rustc -O sliding_window.rs' "$(mem_peak rustc -O sliding_window.rs -o target/sliding_window)"
