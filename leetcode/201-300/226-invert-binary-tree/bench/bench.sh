#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #226.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Multi-approach kata: recursive and iterative share one bench.sh with
# compiled runtime batch (warmup 5 / runs 30) and python in a separate batch.
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup), clang,
# go, karac.

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
    local pkg="$1"
    local out="target/${pkg}_go_seq"
    local src="go-seq/${pkg}/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq/${pkg} ..." >&2
        ( cd go-seq && go build -o "../$out" "./${pkg}" )
    fi
}

build_rust recursive.rs
build_rust iterative.rs
build_c    recursive.c
build_c    iterative.c
build_kara recursive.kara
build_kara iterative.kara
build_go_seq recursive
build_go_seq iterative

expected="2666665501"
mismatch=""
for pair in \
    'rec_kara:./target/recursive_kara' \
    'rec_rust:./target/recursive' \
    'rec_c:./target/recursive_c' \
    'rec_go:./target/recursive_go_seq' \
    'iter_kara:./target/iterative_kara' \
    'iter_rust:./target/iterative' \
    'iter_c:./target/iterative_c' \
    'iter_go:./target/iterative_go_seq'; do
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
echo "sink (all eight: kara/rust/c/go × recursive/iterative): $expected"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_rec=$(python3 recursive.py)
    py_iter=$(python3 iterative.py)
    if [ "$py_rec" != "$expected" ] || [ "$py_iter" != "$expected" ]; then
        echo "python sink mismatch: py_rec=$py_rec py_iter=$py_iter" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

echo "=== runtime — compiled (warmup 5 / runs 30) ==="
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara recursive (codegen)' './target/recursive_kara' \
    --command-name 'kara iterative (codegen)' './target/iterative_kara' \
    --command-name 'rust recursive'           './target/recursive' \
    --command-name 'rust iterative'           './target/iterative' \
    --command-name 'c    recursive'           './target/recursive_c' \
    --command-name 'c    iterative'           './target/iterative_c' \
    --command-name 'go   recursive'           './target/recursive_go_seq' \
    --command-name 'go   iterative'           './target/iterative_go_seq'

if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    echo
    echo "=== runtime — python ==="
    hyperfine \
        --warmup 5 \
        --runs 30 \
        --shell=none \
        --command-name 'py   recursive' 'python3 recursive.py' \
        --command-name 'py   iterative' 'python3 iterative.py'
fi

echo
echo "=== compile elapsed (cold) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --shell=none \
    --prepare 'rm -f target/recursive_kara recursive' \
    --command-name 'karac build recursive.kara' 'sh -c "karac build recursive.kara >/dev/null && mv recursive target/recursive_kara"' \
    --prepare 'rm -f target/iterative_kara iterative' \
    --command-name 'karac build iterative.kara' 'sh -c "karac build iterative.kara >/dev/null && mv iterative target/iterative_kara"' \
    --prepare 'rm -f target/recursive' \
    --command-name 'rustc -O recursive.rs'      'rustc -O recursive.rs -o target/recursive' \
    --prepare 'rm -f target/iterative' \
    --command-name 'rustc -O iterative.rs'      'rustc -O iterative.rs -o target/iterative' \
    --prepare 'rm -f target/recursive_c' \
    --command-name 'clang -O3 recursive.c'      'clang -O3 recursive.c -o target/recursive_c' \
    --prepare 'rm -f target/iterative_c' \
    --command-name 'clang -O3 iterative.c'      'clang -O3 iterative.c -o target/iterative_c'

echo
echo "=== binary size ==="
for spec in \
    'kara recursive:target/recursive_kara' \
    'kara iterative:target/iterative_kara' \
    'rust recursive:target/recursive' \
    'rust iterative:target/iterative' \
    'c    recursive:target/recursive_c' \
    'c    iterative:target/iterative_c' \
    'go   recursive:target/recursive_go_seq' \
    'go   iterative:target/iterative_go_seq'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-30s %10s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara recursive (codegen)' "$(mem_peak ./target/recursive_kara)"
print_mem 'kara iterative (codegen)' "$(mem_peak ./target/iterative_kara)"
print_mem 'rust recursive'           "$(mem_peak ./target/recursive)"
print_mem 'rust iterative'           "$(mem_peak ./target/iterative)"
print_mem 'c    recursive'           "$(mem_peak ./target/recursive_c)"
print_mem 'c    iterative'           "$(mem_peak ./target/iterative_c)"
print_mem 'go   recursive'           "$(mem_peak ./target/recursive_go_seq)"
print_mem 'go   iterative'           "$(mem_peak ./target/iterative_go_seq)"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    print_mem 'py   recursive' "$(mem_peak python3 recursive.py)"
    print_mem 'py   iterative' "$(mem_peak python3 iterative.py)"
fi

echo
echo "=== compile memory (cold) ==="
for src in recursive.kara iterative.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    print_mem "karac build $src" "$bytes"
done
for src in recursive.rs iterative.rs; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    print_mem "rustc -O $src" "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in recursive.c iterative.c; do
    out="target/$(basename "$src" .c)_c"
    rm -f "$out"
    print_mem "clang -O3 $src" "$(mem_peak clang -O3 "$src" -o "$out")"
done
