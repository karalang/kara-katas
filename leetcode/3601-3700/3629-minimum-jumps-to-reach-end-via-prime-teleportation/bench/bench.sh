#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #3629.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata. Long workload (~1s+). Requires: hyperfine, rustc, clang, go, karac.

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
    local out="target/bfs_sieve_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust bfs_sieve.rs
build_c    bfs_sieve.c
build_kara bfs_sieve.kara
build_go_seq

expected=$(./target/bfs_sieve_kara)
mismatch=""
for pair in \
    'rust:./target/bfs_sieve' \
    'c:./target/bfs_sieve_c' \
    'go:./target/bfs_sieve_go_seq'; do
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
    py_out=$(python3 bfs_sieve.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

echo "=== runtime — long workloads (compiled) ==="
hyperfine \
    --warmup 2 \
    --runs 10 \
    --shell=none \
    --command-name 'kara bfs_sieve (codegen)' './target/bfs_sieve_kara' \
    --command-name 'rust bfs_sieve'           './target/bfs_sieve' \
    --command-name 'c    bfs_sieve'           './target/bfs_sieve_c' \
    --command-name 'go   bfs_sieve'           './target/bfs_sieve_go_seq'

echo
echo "=== runtime — long workloads (py) ==="
hyperfine \
    --warmup 2 \
    --runs 10 \
    --shell=none \
    --command-name 'py   bfs_sieve'           'python3 bfs_sieve.py'

echo
echo "=== compile elapsed (cold) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --shell=none \
    --prepare 'rm -f target/bfs_sieve_kara bfs_sieve' \
    --command-name 'karac build bfs_sieve.kara' 'sh -c "karac build bfs_sieve.kara >/dev/null && mv bfs_sieve target/bfs_sieve_kara"' \
    --prepare 'rm -f target/bfs_sieve' \
    --command-name 'rustc -O bfs_sieve.rs'      'rustc -O bfs_sieve.rs -o target/bfs_sieve' \
    --prepare 'rm -f target/bfs_sieve_c' \
    --command-name 'clang -O3 bfs_sieve.c'      'clang -O3 bfs_sieve.c -o target/bfs_sieve_c'

echo
echo "=== binary size ==="
for spec in \
    'kara bfs_sieve:target/bfs_sieve_kara' \
    'rust bfs_sieve:target/bfs_sieve' \
    'c    bfs_sieve:target/bfs_sieve_c' \
    'go   bfs_sieve:target/bfs_sieve_go_seq'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-30s %10s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara bfs_sieve (codegen)' "$(mem_peak ./target/bfs_sieve_kara)"
print_mem 'rust bfs_sieve'           "$(mem_peak ./target/bfs_sieve)"
print_mem 'c    bfs_sieve'           "$(mem_peak ./target/bfs_sieve_c)"
print_mem 'go   bfs_sieve'           "$(mem_peak ./target/bfs_sieve_go_seq)"
print_mem 'py   bfs_sieve'           "$(mem_peak python3 bfs_sieve.py)"

echo
echo "=== compile memory (cold) ==="
for src in bfs_sieve.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    print_mem "karac build $src" "$bytes"
done
for src in bfs_sieve.rs; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    print_mem "rustc -O $src" "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in bfs_sieve.c; do
    out="target/$(basename "$src" .c)_c"
    rm -f "$out"
    print_mem "clang -O3 $src" "$(mem_peak clang -O3 "$src" -o "$out")"
done
