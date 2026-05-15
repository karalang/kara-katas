#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #5.
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

build_rust expand_around_center.rs
build_kara expand_around_center.kara

echo "=== runtime ==="
hyperfine \
    --warmup 3 \
    --runs 10 \
    --shell=none \
    --command-name 'kara expand_around_center (codegen)' './target/expand_around_center_kara' \
    --command-name 'py   expand_around_center'           'python3 expand_around_center.py' \
    --command-name 'rust expand_around_center'           './target/expand_around_center'

echo
echo "=== compile (cold, no cache) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --prepare 'rm -f target/expand_around_center_kara expand_around_center' \
    --command-name 'karac build expand_around_center.kara' 'sh -c "karac build expand_around_center.kara >/dev/null && mv expand_around_center target/expand_around_center_kara"' \
    --prepare 'rm -f target/expand_around_center' \
    --command-name 'rustc -O expand_around_center.rs'      'rustc -O expand_around_center.rs -o target/expand_around_center'

echo
echo "=== binary size ==="
for spec in 'kara expand_around_center:target/expand_around_center_kara' 'rust expand_around_center:target/expand_around_center'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-30s %8s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara expand_around_center (codegen)' "$(mem_peak ./target/expand_around_center_kara)"
print_mem 'py   expand_around_center'           "$(mem_peak python3 expand_around_center.py)"
print_mem 'rust expand_around_center'           "$(mem_peak ./target/expand_around_center)"

echo
echo "=== compile memory (cold) ==="
rm -f target/expand_around_center_kara expand_around_center
print_mem 'karac build expand_around_center.kara' "$(mem_peak karac build expand_around_center.kara)"
mv expand_around_center target/expand_around_center_kara 2>/dev/null || true
rm -f target/expand_around_center
print_mem 'rustc -O expand_around_center.rs' "$(mem_peak rustc -O expand_around_center.rs -o target/expand_around_center)"
