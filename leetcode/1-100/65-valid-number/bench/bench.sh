#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #65.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup), clang, karac.

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
require clang     "xcode-select --install (macOS) or your distro's clang package"
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

build_c() {
    local src="$1"
    local out="target/$(basename "$src" .c)_c"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src ..." >&2
        clang -O3 "$src" -o "$out"
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

build_rust valid.rs
build_c    valid.c
build_kara valid.kara

# Sanity: all four impls must agree on the sink before we time them.
kara_sink=$(./target/valid_kara)
rust_sink=$(./target/valid)
c_sink=$(./target/valid_c)
py_sink=$(python3 valid.py)
if [ "$kara_sink" != "$rust_sink" ] || [ "$kara_sink" != "$c_sink" ] || [ "$kara_sink" != "$py_sink" ]; then
    echo "sink mismatch: kara=$kara_sink rust=$rust_sink c=$c_sink py=$py_sink" >&2
    exit 1
fi
echo "sink (kara == rust == c == py): $kara_sink"
echo

echo "=== runtime ==="
hyperfine \
    --warmup 3 \
    --runs 10 \
    --shell=none \
    --command-name 'kara valid (codegen)' './target/valid_kara' \
    --command-name 'py   valid'           'python3 valid.py' \
    --command-name 'rust valid'           './target/valid' \
    --command-name 'c    valid'           './target/valid_c'

echo
echo "=== compile (cold, no cache) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --prepare 'rm -f target/valid_kara valid' \
    --command-name 'karac build valid.kara' 'sh -c "karac build valid.kara >/dev/null && mv valid target/valid_kara"' \
    --prepare 'rm -f target/valid' \
    --command-name 'rustc -O valid.rs'      'rustc -O valid.rs -o target/valid' \
    --prepare 'rm -f target/valid_c' \
    --command-name 'clang -O3 valid.c'      'clang -O3 valid.c -o target/valid_c'

echo
echo "=== binary size ==="
for spec in 'kara valid:target/valid_kara' 'rust valid:target/valid' 'c    valid:target/valid_c'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-30s %8s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara valid (codegen)' "$(mem_peak ./target/valid_kara)"
print_mem 'py   valid'           "$(mem_peak python3 valid.py)"
print_mem 'rust valid'           "$(mem_peak ./target/valid)"
print_mem 'c    valid'           "$(mem_peak ./target/valid_c)"

echo
echo "=== compile memory (cold) ==="
rm -f target/valid_kara valid
print_mem 'karac build valid.kara' "$(mem_peak karac build valid.kara)"
mv valid target/valid_kara 2>/dev/null || true
rm -f target/valid
print_mem 'rustc -O valid.rs' "$(mem_peak rustc -O valid.rs -o target/valid)"
rm -f target/valid_c
print_mem 'clang -O3 valid.c' "$(mem_peak clang -O3 valid.c -o target/valid_c)"
