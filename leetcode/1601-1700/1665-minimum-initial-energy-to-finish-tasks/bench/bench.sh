#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #1665.
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

# /usr/bin/time -l (macOS BSD time) prints a "peak memory footprint" line on
# stderr. We capture its stderr through a brace-group redirect, discard the
# wrapped command's own stdout, and parse the bytes column. Memory is much
# more stable run-to-run than wall-time (no scheduling/cache variance), so a
# single sample is honest — no hyperfine-style averaging needed.
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

build_rust greedy.rs
build_kara greedy.kara

echo "=== runtime ==="
hyperfine \
    --warmup 2 \
    --runs 10 \
    --shell=none \
    --command-name 'kara greedy (codegen)' './target/greedy_kara' \
    --command-name 'py   greedy'           'python3 greedy.py' \
    --command-name 'rust greedy'           './target/greedy'

echo
echo "=== compile (cold, no cache) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --prepare 'rm -f target/greedy_kara greedy' \
    --command-name 'karac build greedy.kara' 'sh -c "karac build greedy.kara >/dev/null && mv greedy target/greedy_kara"' \
    --prepare 'rm -f target/greedy' \
    --command-name 'rustc -O greedy.rs'      'rustc -O greedy.rs -o target/greedy'

echo
echo "=== binary size ==="
for spec in 'kara greedy:target/greedy_kara' 'rust greedy:target/greedy'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-12s %8s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
# python's number includes ~10 MB CPython runtime baseline regardless of N;
# kara/rust are standalone compiled binaries.
print_mem 'kara greedy (codegen)' "$(mem_peak ./target/greedy_kara)"
print_mem 'py   greedy'           "$(mem_peak python3 greedy.py)"
print_mem 'rust greedy'           "$(mem_peak ./target/greedy)"

echo
echo "=== compile memory (cold) ==="
# Artifact deleted before each measurement so the karac/rustc invocation is a
# full cold compile. karac's number covers lex → … → ownership → codegen IR
# build → LLVM optimization passes. Regression detection: a sudden 10× spike
# on `karac build` here is the signature of an algorithmic blowup in a
# frontend phase (cf. 2026-05-12 Array[T, N] Maranget O(N²) fix). We invoke
# karac and rustc *directly* under /usr/bin/time so rusage measures the
# compiler process itself, not a wrapping shell (sh -c would only report
# sh's footprint, missing the compiler entirely).
rm -f target/greedy_kara greedy
print_mem 'karac build greedy.kara' "$(mem_peak karac build greedy.kara)"
mv greedy target/greedy_kara 2>/dev/null || true
rm -f target/greedy
print_mem 'rustc -O greedy.rs' "$(mem_peak rustc -O greedy.rs -o target/greedy)"
