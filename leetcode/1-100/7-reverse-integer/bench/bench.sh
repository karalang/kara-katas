#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #7.
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

build_rust reverse.rs
build_kara reverse.kara

# Sanity: all three impls must agree on the sink before we time them.
# Python is slow at K=50M (multi-minute), so we skip it from the
# runtime hyperfine pass and just verify the codegen + rust sinks.
kara_sink=$(./target/reverse_kara)
rust_sink=$(./target/reverse)
if [ "$kara_sink" != "$rust_sink" ]; then
    echo "sink mismatch: kara=$kara_sink rust=$rust_sink" >&2
    exit 1
fi
echo "sink (kara == rust): $kara_sink"
echo

echo "=== runtime (codegen + rust; py runs separately, see below) ==="
hyperfine \
    --warmup 3 \
    --runs 10 \
    --shell=none \
    --command-name 'kara reverse (codegen)' './target/reverse_kara' \
    --command-name 'rust reverse'           './target/reverse'

echo
echo "=== compile (cold, no cache) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --prepare 'rm -f target/reverse_kara reverse' \
    --command-name 'karac build reverse.kara' 'sh -c "karac build reverse.kara >/dev/null && mv reverse target/reverse_kara"' \
    --prepare 'rm -f target/reverse' \
    --command-name 'rustc -O reverse.rs'      'rustc -O reverse.rs -o target/reverse'

echo
echo "=== binary size ==="
for spec in 'kara reverse:target/reverse_kara' 'rust reverse:target/reverse'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-30s %8s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara reverse (codegen)' "$(mem_peak ./target/reverse_kara)"
print_mem 'rust reverse'           "$(mem_peak ./target/reverse)"

echo
echo "=== compile memory (cold) ==="
rm -f target/reverse_kara reverse
print_mem 'karac build reverse.kara' "$(mem_peak karac build reverse.kara)"
mv reverse target/reverse_kara 2>/dev/null || true
rm -f target/reverse
print_mem 'rustc -O reverse.rs' "$(mem_peak rustc -O reverse.rs -o target/reverse)"

# Python sink + a short single-K=1M timing in a separate stanza — the
# bench's K=50M would take ~10 minutes per python sample, well past the
# patience floor for an iterative dev loop. We sample a 50× smaller K
# and quote the ratio in the README so the kara-vs-py number stays
# anchored even if the headline kara-vs-rust comparison is the focus.
echo
echo "=== python (K=1M, scaled-down) ==="
python3 -c '
import sys
sys.path.insert(0, ".")
import reverse as r
r.k_iters_override = 1_000_000
# Reach into the module: we run a local copy of main with the scaled K.
inputs = [r.to_i32(i * 2_654_435_769 + 305_419_896) for i in range(1024)]
import time
t0 = time.perf_counter()
total = 0
for k in range(1_000_000):
    total += r.reverse(inputs[k % 1024])
t1 = time.perf_counter()
print(f"  py reverse (K=1M)               {(t1-t0)*1000:.1f} ms   sink={total}")
print(f"  -> projected K=50M              {(t1-t0)*50*1000:.0f} ms")
'
