#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #204.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Kara's `bench/count.kara` carries a `#[par_unordered]` attribute that
# opts the outer loop into the auto-par collect-style codegen path
# (Phase 3 in karac-rust). Rust/C/Python are idiomatic single-threaded
# implementations — the comparison framing is "auto-par Kara vs the code
# a programmer writes when they don't reach for rayon / OpenMP." A
# parallel Rust row (rayon) is a worthwhile follow-up for transparency
# but the per-iter `is_prime()` work is heavy enough that even the
# single-threaded baselines are honest comparators.
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
require cargo     "rustup (https://rustup.rs)  — needed for the rayon-parallel Rust variant"
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

build_rust count.rs
build_c    count.c
build_kara count.kara
build_kara count_seq.kara

# Rayon variant lives in its own Cargo project under bench/rayon/ because
# rayon is a third-party crate (no rustc single-file path for that).
# `cargo build --release` is incremental; subsequent invocations are
# near-instant when the source hasn't changed.
echo "building rayon variant (cargo) ..." >&2
( cd rayon && cargo build --release --quiet )
cp -f rayon/target/release/count_rayon target/count_rayon

# Sanity: all four impls must agree on the (count, sum) sink before we
# time them. Python skipped from sink check by default — at N=10M it
# takes ~30s and bench.sh would block waiting on it. Set
# `KARA_BENCH_INCLUDE_PY=1` to opt in.
kara_sink=$(./target/count_kara)
kara_seq_sink=$(./target/count_seq_kara)
rust_sink=$(./target/count)
c_sink=$(./target/count_c)
rayon_sink=$(./target/count_rayon)
if [ "$kara_sink" != "$rust_sink" ] || [ "$kara_sink" != "$c_sink" ] || [ "$kara_sink" != "$rayon_sink" ] || [ "$kara_sink" != "$kara_seq_sink" ]; then
    echo "sink mismatch: kara=$kara_sink kara_seq=$kara_seq_sink rust=$rust_sink c=$c_sink rayon=$rayon_sink" >&2
    exit 1
fi
echo "sink (kara == kara-seq == rust == c == rust+rayon): $(echo "$kara_sink" | tr '\n' ' ' | sed 's/ $//')"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_sink=$(python3 count.py)
    if [ "$kara_sink" != "$py_sink" ]; then
        echo "python sink mismatch: kara=$kara_sink py=$py_sink" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

echo "=== runtime ==="
hyperfine \
    --warmup 3 \
    --runs 10 \
    --shell=none \
    --command-name 'kara count (codegen, #[par_unordered])' './target/count_kara' \
    --command-name 'kara count (codegen, single-threaded)'  './target/count_seq_kara' \
    --command-name 'rust count (single-threaded)'           './target/count' \
    --command-name 'rust count (rayon par_iter)'            './target/count_rayon' \
    --command-name 'c    count (single-threaded)'           './target/count_c'

echo
echo "=== compile (cold, no cache) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --prepare 'rm -f target/count_kara count' \
    --command-name 'karac build count.kara' 'sh -c "karac build count.kara >/dev/null && mv count target/count_kara"' \
    --prepare 'rm -f target/count' \
    --command-name 'rustc -O count.rs'      'rustc -O count.rs -o target/count' \
    --prepare 'rm -f target/count_c' \
    --command-name 'clang -O3 count.c'      'clang -O3 count.c -o target/count_c'

echo
echo "=== binary size ==="
for spec in 'kara count:target/count_kara' 'kara count (seq):target/count_seq_kara' 'rust count:target/count' 'rust+rayon count:target/count_rayon' 'c    count:target/count_c'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-30s %8s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara count (codegen)' "$(mem_peak ./target/count_kara)"
print_mem 'kara count (seq)'     "$(mem_peak ./target/count_seq_kara)"
print_mem 'rust count'           "$(mem_peak ./target/count)"
print_mem 'rust+rayon count'     "$(mem_peak ./target/count_rayon)"
print_mem 'c    count'           "$(mem_peak ./target/count_c)"

echo
echo "=== compile memory (cold) ==="
rm -f target/count_kara count
print_mem 'karac build count.kara' "$(mem_peak karac build count.kara)"
mv count target/count_kara 2>/dev/null || true
rm -f target/count
print_mem 'rustc -O count.rs' "$(mem_peak rustc -O count.rs -o target/count)"
rm -f target/count_c
print_mem 'clang -O3 count.c' "$(mem_peak clang -O3 count.c -o target/count_c)"
