#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #4.
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

build_rust binary_search_partition.rs
build_kara binary_search_partition.kara

echo "=== runtime ==="
hyperfine \
    --warmup 3 \
    --runs 10 \
    --shell=none \
    --command-name 'kara binary_search_partition (codegen)' './target/binary_search_partition_kara' \
    --command-name 'py   binary_search_partition'           'python3 binary_search_partition.py' \
    --command-name 'rust binary_search_partition'           './target/binary_search_partition'

echo
echo "=== compile (cold, no cache) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --prepare 'rm -f target/binary_search_partition_kara binary_search_partition' \
    --command-name 'karac build binary_search_partition.kara' 'sh -c "karac build binary_search_partition.kara >/dev/null && mv binary_search_partition target/binary_search_partition_kara"' \
    --prepare 'rm -f target/binary_search_partition' \
    --command-name 'rustc -O binary_search_partition.rs'      'rustc -O binary_search_partition.rs -o target/binary_search_partition'

echo
echo "=== binary size ==="
for spec in 'kara binary_search_partition:target/binary_search_partition_kara' 'rust binary_search_partition:target/binary_search_partition'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-32s %8s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara binary_search_partition (codegen)' "$(mem_peak ./target/binary_search_partition_kara)"
print_mem 'py   binary_search_partition'           "$(mem_peak python3 binary_search_partition.py)"
print_mem 'rust binary_search_partition'           "$(mem_peak ./target/binary_search_partition)"

echo
echo "=== compile memory (cold) ==="
rm -f target/binary_search_partition_kara binary_search_partition
print_mem 'karac build binary_search_partition.kara' "$(mem_peak karac build binary_search_partition.kara)"
mv binary_search_partition target/binary_search_partition_kara 2>/dev/null || true
rm -f target/binary_search_partition
print_mem 'rustc -O binary_search_partition.rs' "$(mem_peak rustc -O binary_search_partition.rs -o target/binary_search_partition)"
