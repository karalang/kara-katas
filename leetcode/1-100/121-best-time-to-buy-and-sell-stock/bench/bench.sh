#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #121.
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

build_rust one_pass.rs
build_kara one_pass.kara

echo "=== runtime ==="
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara one_pass (codegen)' './target/one_pass_kara' \
    --command-name 'py   one_pass'           'python3 one_pass.py' \
    --command-name 'rust one_pass'           './target/one_pass'

echo
echo "=== compile (cold, no cache) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --prepare 'rm -f target/one_pass_kara one_pass' \
    --command-name 'karac build one_pass.kara' 'sh -c "karac build one_pass.kara >/dev/null && mv one_pass target/one_pass_kara"' \
    --prepare 'rm -f target/one_pass' \
    --command-name 'rustc -O one_pass.rs'      'rustc -O one_pass.rs -o target/one_pass'

echo
echo "=== binary size ==="
for spec in 'kara one_pass:target/one_pass_kara' 'rust one_pass:target/one_pass'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-14s %8s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara one_pass (codegen)' "$(mem_peak ./target/one_pass_kara)"
print_mem 'py   one_pass'           "$(mem_peak python3 one_pass.py)"
print_mem 'rust one_pass'           "$(mem_peak ./target/one_pass)"

echo
echo "=== compile memory (cold) ==="
rm -f target/one_pass_kara one_pass
print_mem 'karac build one_pass.kara' "$(mem_peak karac build one_pass.kara)"
mv one_pass target/one_pass_kara 2>/dev/null || true
rm -f target/one_pass
print_mem 'rustc -O one_pass.rs' "$(mem_peak rustc -O one_pass.rs -o target/one_pass)"
