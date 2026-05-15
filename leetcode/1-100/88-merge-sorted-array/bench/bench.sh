#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #88.
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

build_rust two_pointer.rs
build_kara two_pointer.kara

echo "=== runtime ==="
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara two_pointer (codegen)' './target/two_pointer_kara' \
    --command-name 'py   two_pointer'           'python3 two_pointer.py' \
    --command-name 'rust two_pointer'           './target/two_pointer'

echo
echo "=== compile (cold, no cache) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --prepare 'rm -f target/two_pointer_kara two_pointer' \
    --command-name 'karac build two_pointer.kara' 'sh -c "karac build two_pointer.kara >/dev/null && mv two_pointer target/two_pointer_kara"' \
    --prepare 'rm -f target/two_pointer' \
    --command-name 'rustc -O two_pointer.rs'      'rustc -O two_pointer.rs -o target/two_pointer'

echo
echo "=== binary size ==="
for spec in 'kara two_pointer:target/two_pointer_kara' 'rust two_pointer:target/two_pointer'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-17s %8s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara two_pointer (codegen)' "$(mem_peak ./target/two_pointer_kara)"
print_mem 'py   two_pointer'           "$(mem_peak python3 two_pointer.py)"
print_mem 'rust two_pointer'           "$(mem_peak ./target/two_pointer)"

echo
echo "=== compile memory (cold) ==="
rm -f target/two_pointer_kara two_pointer
print_mem 'karac build two_pointer.kara' "$(mem_peak karac build two_pointer.kara)"
mv two_pointer target/two_pointer_kara 2>/dev/null || true
rm -f target/two_pointer
print_mem 'rustc -O two_pointer.rs' "$(mem_peak rustc -O two_pointer.rs -o target/two_pointer)"
