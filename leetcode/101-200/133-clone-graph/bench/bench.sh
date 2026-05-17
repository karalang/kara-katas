#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #133.
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

build_rust clone_bfs.rs
build_kara clone_bfs.kara

echo "=== runtime (clone_bfs, N=2000 ring, K=500) ==="
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara clone_bfs (codegen)' './target/clone_bfs_kara' \
    --command-name 'py   clone_bfs'           'python3 clone_bfs.py' \
    --command-name 'rust clone_bfs'           './target/clone_bfs'

echo
echo "=== binary size ==="
for spec in \
    'kara clone_bfs (codegen):target/clone_bfs_kara' \
    'rust clone_bfs:target/clone_bfs'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-30s %8s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara clone_bfs (codegen)' "$(mem_peak ./target/clone_bfs_kara)"
print_mem 'py   clone_bfs'           "$(mem_peak python3 clone_bfs.py)"
print_mem 'rust clone_bfs'           "$(mem_peak ./target/clone_bfs)"
