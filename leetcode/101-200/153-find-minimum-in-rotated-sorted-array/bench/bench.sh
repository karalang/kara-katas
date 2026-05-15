#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #153.
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

build_rust linear_scan.rs
build_rust binary_search.rs
build_kara linear_scan.kara
build_kara binary_search.kara

echo "=== runtime (linear scan, K=10) ==="
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara linear_scan (codegen)' './target/linear_scan_kara' \
    --command-name 'py   linear_scan'           'python3 linear_scan.py' \
    --command-name 'rust linear_scan'           './target/linear_scan'

echo
echo "=== runtime (binary search, K=2_000_000) ==="
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara binary_search (codegen)' './target/binary_search_kara' \
    --command-name 'py   binary_search'           'python3 binary_search.py' \
    --command-name 'rust binary_search'           './target/binary_search'

echo
echo "=== compile (cold, no cache) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --prepare 'rm -f target/linear_scan_kara linear_scan' \
    --command-name 'karac build linear_scan.kara'   'sh -c "karac build linear_scan.kara >/dev/null && mv linear_scan target/linear_scan_kara"' \
    --prepare 'rm -f target/linear_scan' \
    --command-name 'rustc -O linear_scan.rs'        'rustc -O linear_scan.rs -o target/linear_scan' \
    --prepare 'rm -f target/binary_search_kara binary_search' \
    --command-name 'karac build binary_search.kara' 'sh -c "karac build binary_search.kara >/dev/null && mv binary_search target/binary_search_kara"' \
    --prepare 'rm -f target/binary_search' \
    --command-name 'rustc -O binary_search.rs'      'rustc -O binary_search.rs -o target/binary_search'

echo
echo "=== binary size ==="
for spec in \
    'kara linear_scan:target/linear_scan_kara' \
    'rust linear_scan:target/linear_scan' \
    'kara binary_search:target/binary_search_kara' \
    'rust binary_search:target/binary_search'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-22s %8s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara linear_scan (codegen)'   "$(mem_peak ./target/linear_scan_kara)"
print_mem 'py   linear_scan'             "$(mem_peak python3 linear_scan.py)"
print_mem 'rust linear_scan'             "$(mem_peak ./target/linear_scan)"
print_mem 'kara binary_search (codegen)' "$(mem_peak ./target/binary_search_kara)"
print_mem 'py   binary_search'           "$(mem_peak python3 binary_search.py)"
print_mem 'rust binary_search'           "$(mem_peak ./target/binary_search)"

echo
echo "=== compile memory (cold) ==="
rm -f target/linear_scan_kara linear_scan
print_mem 'karac build linear_scan.kara' "$(mem_peak karac build linear_scan.kara)"
mv linear_scan target/linear_scan_kara 2>/dev/null || true
rm -f target/linear_scan
print_mem 'rustc -O linear_scan.rs' "$(mem_peak rustc -O linear_scan.rs -o target/linear_scan)"

rm -f target/binary_search_kara binary_search
print_mem 'karac build binary_search.kara' "$(mem_peak karac build binary_search.kara)"
mv binary_search target/binary_search_kara 2>/dev/null || true
rm -f target/binary_search
print_mem 'rustc -O binary_search.rs' "$(mem_peak rustc -O binary_search.rs -o target/binary_search)"
