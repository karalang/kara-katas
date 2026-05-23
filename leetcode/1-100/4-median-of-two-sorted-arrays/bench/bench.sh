#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #4.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata: a single middle_pair_off call does ~log2(M) ≈ 20
# partition cross-checks — pure integer arithmetic + a handful of
# i64 loads, no allocator surface on the inner loop. The outer K = 10M
# loop carries `off = k % R` cross-iteration state but each call is
# independent; a par lane is plausible but the per-call work (~hundred-ns)
# is small enough that goroutine/rayon dispatch would dominate. Stays
# single-threaded so the kata measures pure codegen quality per the
# BENCH.md two-lane protocol.
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup), clang,
# go, karac (with --features llvm for the codegen path).

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
require go        "brew install go  or your distro's golang package"
require karac     "cargo install --path . --features llvm  (from karac-rust checkout)"

mem_peak() {
    { /usr/bin/time -l "$@" >/dev/null; } 2>&1 \
        | awk '/peak memory footprint/ {print $1}'
}
print_mem() {
    local label="$1" bytes="$2"
    local mib
    mib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1048576}')
    printf '  %-40s %12s bytes (%6s MiB)\n' "$label" "$bytes" "$mib"
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

build_go_seq() {
    local out="target/binary_search_partition_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust binary_search_partition.rs
build_c    binary_search_partition.c
build_kara binary_search_partition.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before
# timing. Python skipped from sink check by default — at K=10M the py
# run takes ~2s and bench.sh would block on it. Set
# `KARA_BENCH_INCLUDE_PY=1` to opt in.
#
# Plain "name:command" pairs (no associative arrays — macOS bash is 3.2).
expected="20019970000000"
mismatch=""
for pair in \
    'kara:./target/binary_search_partition_kara' \
    'rust:./target/binary_search_partition' \
    'c:./target/binary_search_partition_c' \
    'go:./target/binary_search_partition_go_seq'; do
    name="${pair%%:*}"
    cmd="${pair#*:}"
    out=$("$cmd")
    if [ "$out" != "$expected" ]; then
        mismatch="$mismatch ${name}=${out}"
    fi
done
if [ -n "$mismatch" ]; then
    echo "sink mismatch (expected=$expected):$mismatch" >&2
    exit 1
fi
echo "sink (kara/rust/c/go): $expected"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_out=$(python3 binary_search_partition.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

echo "=== runtime — short workloads (compiled) ==="
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara binary_search_partition (codegen)' './target/binary_search_partition_kara' \
    --command-name 'rust binary_search_partition'           './target/binary_search_partition' \
    --command-name 'c    binary_search_partition'           './target/binary_search_partition_c' \
    --command-name 'go   binary_search_partition'           './target/binary_search_partition_go_seq'

echo
echo "=== runtime — long workloads (py) ==="
hyperfine \
    --warmup 2 \
    --runs 10 \
    --shell=none \
    --command-name 'py   binary_search_partition'           'python3 binary_search_partition.py'

echo
echo "=== compile elapsed (cold) ==="
# Per BENCH.md: hyperfine --warmup 1 --runs 10 with --prepare deleting the
# build artifact so every invocation is a true cold compile. karac/rustc/clang
# are the single-file compilers; go is excluded — its first invocation mixes
# module resolution + std-lib link and isn't comparable to single-file.
hyperfine \
    --warmup 1 \
    --runs 10 \
    --shell=none \
    --prepare 'rm -f target/binary_search_partition_kara binary_search_partition' \
    --command-name 'karac build binary_search_partition.kara' 'sh -c "karac build binary_search_partition.kara >/dev/null && mv binary_search_partition target/binary_search_partition_kara"' \
    --prepare 'rm -f target/binary_search_partition' \
    --command-name 'rustc -O binary_search_partition.rs'      'rustc -O binary_search_partition.rs -o target/binary_search_partition' \
    --prepare 'rm -f target/binary_search_partition_c' \
    --command-name 'clang -O3 binary_search_partition.c'      'clang -O3 binary_search_partition.c -o target/binary_search_partition_c'

echo
echo "=== binary size ==="
for spec in \
    'kara binary_search_partition:target/binary_search_partition_kara' \
    'rust binary_search_partition:target/binary_search_partition' \
    'c    binary_search_partition:target/binary_search_partition_c' \
    'go   binary_search_partition:target/binary_search_partition_go_seq'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-36s %10s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara binary_search_partition (codegen)' "$(mem_peak ./target/binary_search_partition_kara)"
print_mem 'rust binary_search_partition'           "$(mem_peak ./target/binary_search_partition)"
print_mem 'c    binary_search_partition'           "$(mem_peak ./target/binary_search_partition_c)"
print_mem 'go   binary_search_partition'           "$(mem_peak ./target/binary_search_partition_go_seq)"
print_mem 'py   binary_search_partition'           "$(mem_peak python3 binary_search_partition.py)"

echo
echo "=== compile memory (cold) ==="
# Artifact deleted before each measurement so the karac/rustc/clang invocation
# is a full cold compile. Go is omitted per BENCH.md — `go build`'s first run
# mixes module resolution + std-lib link and is not comparable to a single-file
# rustc/clang/karac invocation.
for src in binary_search_partition.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    print_mem "karac build $src" "$bytes"
done
for src in binary_search_partition.rs; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    print_mem "rustc -O $src" "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in binary_search_partition.c; do
    out="target/$(basename "$src" .c)_c"
    rm -f "$out"
    print_mem "clang -O3 $src" "$(mem_peak clang -O3 "$src" -o "$out")"
done
