#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #6.
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
    printf '  %-32s %12s bytes (%6s MiB)\n' "$label" "$bytes" "$mib"
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

build_rust row_buffers.rs
build_kara row_buffers.kara

echo "=== runtime ==="
hyperfine \
    --warmup 3 \
    --runs 10 \
    --shell=none \
    --command-name 'kara row_buffers (codegen)' './target/row_buffers_kara' \
    --command-name 'py   row_buffers'           'python3 row_buffers.py' \
    --command-name 'rust row_buffers'           './target/row_buffers'

echo
echo "=== compile (cold, no cache) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --prepare 'rm -f target/row_buffers_kara row_buffers' \
    --command-name 'karac build row_buffers.kara' 'sh -c "karac build row_buffers.kara >/dev/null && mv row_buffers target/row_buffers_kara"' \
    --prepare 'rm -f target/row_buffers' \
    --command-name 'rustc -O row_buffers.rs'      'rustc -O row_buffers.rs -o target/row_buffers'

echo
echo "=== binary size ==="
for spec in 'kara row_buffers:target/row_buffers_kara' 'rust row_buffers:target/row_buffers'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-30s %8s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara row_buffers (codegen)' "$(mem_peak ./target/row_buffers_kara)"
print_mem 'py   row_buffers'           "$(mem_peak python3 row_buffers.py)"
print_mem 'rust row_buffers'           "$(mem_peak ./target/row_buffers)"

echo
echo "=== compile memory (cold) ==="
rm -f target/row_buffers_kara row_buffers
print_mem 'karac build row_buffers.kara' "$(mem_peak karac build row_buffers.kara)"
mv row_buffers target/row_buffers_kara 2>/dev/null || true
rm -f target/row_buffers
print_mem 'rustc -O row_buffers.rs' "$(mem_peak rustc -O row_buffers.rs -o target/row_buffers)"
