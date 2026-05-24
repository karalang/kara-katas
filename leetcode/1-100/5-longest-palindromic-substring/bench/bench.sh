#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #5.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata. Requires: hyperfine, rustc, clang, go, karac.

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
    local out="target/expand_around_center_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust expand_around_center.rs
build_c    expand_around_center.c
build_kara expand_around_center.kara
build_go_seq

expected=$(./target/expand_around_center_kara)
mismatch=""
for pair in \
    'rust:./target/expand_around_center' \
    'c:./target/expand_around_center_c' \
    'go:./target/expand_around_center_go_seq'; do
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
    py_out=$(python3 expand_around_center.py)
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
    --command-name 'kara expand_around_center (codegen)' './target/expand_around_center_kara' \
    --command-name 'rust expand_around_center'           './target/expand_around_center' \
    --command-name 'c    expand_around_center'           './target/expand_around_center_c' \
    --command-name 'go   expand_around_center'           './target/expand_around_center_go_seq'

echo
echo "=== runtime — long workloads (py) ==="
hyperfine \
    --warmup 2 \
    --runs 10 \
    --shell=none \
    --command-name 'py   expand_around_center'           'python3 expand_around_center.py'

echo
echo "=== compile elapsed (cold) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --shell=none \
    --prepare 'rm -f target/expand_around_center_kara expand_around_center' \
    --command-name 'karac build expand_around_center.kara' 'sh -c "karac build expand_around_center.kara >/dev/null && mv expand_around_center target/expand_around_center_kara"' \
    --prepare 'rm -f target/expand_around_center' \
    --command-name 'rustc -O expand_around_center.rs'      'rustc -O expand_around_center.rs -o target/expand_around_center' \
    --prepare 'rm -f target/expand_around_center_c' \
    --command-name 'clang -O3 expand_around_center.c'      'clang -O3 expand_around_center.c -o target/expand_around_center_c'

echo
echo "=== binary size ==="
for spec in \
    'kara expand_around_center:target/expand_around_center_kara' \
    'rust expand_around_center:target/expand_around_center' \
    'c    expand_around_center:target/expand_around_center_c' \
    'go   expand_around_center:target/expand_around_center_go_seq'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-30s %10s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara expand_around_center (codegen)' "$(mem_peak ./target/expand_around_center_kara)"
print_mem 'rust expand_around_center'           "$(mem_peak ./target/expand_around_center)"
print_mem 'c    expand_around_center'           "$(mem_peak ./target/expand_around_center_c)"
print_mem 'go   expand_around_center'           "$(mem_peak ./target/expand_around_center_go_seq)"
print_mem 'py   expand_around_center'           "$(mem_peak python3 expand_around_center.py)"

echo
echo "=== compile memory (cold) ==="
for src in expand_around_center.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    print_mem "karac build $src" "$bytes"
done
for src in expand_around_center.rs; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    print_mem "rustc -O $src" "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in expand_around_center.c; do
    out="target/$(basename "$src" .c)_c"
    rm -f "$out"
    print_mem "clang -O3 $src" "$(mem_peak clang -O3 "$src" -o "$out")"
done
