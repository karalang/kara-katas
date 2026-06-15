#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #31.
# See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the one-pass modified binary search (★ style): a single
# O(log n) pass that picks the sorted half at each midpoint — pure branchy integer
# compute, no allocation. Workload: build one fixed rotated-sorted array of length
# N=4096 once (values 2*((p+ROT)%N) — even, so odd targets MISS), then run search()
# TOTAL=18M times for targets cycling through [0, 2N) so ~half hit and ~half miss
# (both control-flow paths). The target varies with the loop index, so no comparator
# can hoist the pure call out of the loop; fold each result index into a checksum
# (the un-elidable sink). The accumulator carries a loop-borne dependency, so this
# is a single-lane (seq) bench by construction.
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup), clang, go,
# karac (with --features llvm for the codegen path).

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
require karac     "cargo install --path . --features llvm  (from karac checkout)"

if [ "${BENCH_JSON:-1}" = "1" ]; then
    require jq      "brew install jq"
    require python3 "python3 ships with macOS; or 'brew install python'"
fi
ROOT="$(cd ../../../.. && pwd)"
. "$ROOT/scripts/bench-lib.sh"

mem_peak() {
    { /usr/bin/time -l "$@" >/dev/null; } 2>&1 \
        | awk '/peak memory footprint/ {print $1}'
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

# Apples-to-apples safety comparator: Rust with overflow checks ON, matching
# Kāra's checked-by-default integer semantics (design.md § Arithmetic Overflow).
# `rustc -O` alone silently WRAPS; this `-C overflow-checks=on` variant traps
# like Kāra. The checksum modulus keeps every value well inside i64, so neither
# variant traps — the safety tax isolates codegen, not arithmetic.
build_rust_checked() {
    local src="$1"
    local out="target/$(basename "$src" .rs)_rschk"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src (overflow-checks=on) ..." >&2
        rustc -O -C overflow-checks=on "$src" -o "$out"
    fi
}

build_kara() {
    local src="$1"
    local stem="$(basename "$src" .kara)"
    local out="target/${stem}_kara"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling $src (auto-par default) ..." >&2
        karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

build_kara_seq() {
    local src="$1"
    local stem="$(basename "$src" .kara)"
    local out="target/${stem}_kara_seq"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling $src (KARAC_AUTO_PAR=0, seq lane) ..." >&2
        KARAC_AUTO_PAR=0 karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

build_go_seq() {
    local out="target/search_rotated_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust         search_rotated.rs
build_rust_checked search_rotated.rs
build_c            search_rotated.c
build_kara         search_rotated.kara
build_kara_seq     search_rotated.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="455834850"
mismatch=""
for pair in \
    'kara:./target/search_rotated_kara' \
    'kara_seq:./target/search_rotated_kara_seq' \
    'rust:./target/search_rotated' \
    'rust_chk:./target/search_rotated_rschk' \
    'c:./target/search_rotated_c' \
    'go:./target/search_rotated_go_seq'; do
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
echo "sink (kara/kara_seq/rust/c/go): $expected"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_out=$(python3 search_rotated.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=33 slug=search-in-rotated-sorted-array group=1-100 \
    title="Search in Rotated Sorted Array" \
    workload="TOTAL=18M one-pass binary searches over a fixed rotated 4096-array, cycling targets + checksum" \
    sink="$expected"

echo "=== runtime — seq lane (single-threaded rotated binary search) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach search_rotated --lane seq --mode codegen \
    --name 'kara search_rotated (seq, KARAC_AUTO_PAR=0)' --cmd './target/search_rotated_kara_seq'
rt_cmd --lang rust --approach search_rotated --lane seq --mode native \
    --name 'rust search_rotated' --cmd './target/search_rotated'
rt_cmd --lang rust --approach search_rotated_rschk --lane seq --mode native \
    --name 'rust search_rotated (overflow-checks=on, =Kara safety)' --cmd './target/search_rotated_rschk'
rt_cmd --lang c --approach search_rotated --lane seq --mode native \
    --name 'c    search_rotated' --cmd './target/search_rotated_c'
rt_cmd --lang go --approach search_rotated --lane seq --mode native \
    --name 'go   search_rotated' --cmd './target/search_rotated_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 1 --runs 3
rt_cmd --lang python --approach search_rotated --lane seq --mode interp \
    --name 'py   search_rotated' --cmd 'python3 search_rotated.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach search_rotated --mode codegen \
    --prepare 'rm -f target/search_rotated_kara search_rotated' \
    --name 'karac build search_rotated.kara' \
    --cmd 'sh -c "karac build search_rotated.kara >/dev/null && mv search_rotated target/search_rotated_kara"'
ce_cmd --lang rust --approach search_rotated --mode native \
    --prepare 'rm -f target/search_rotated' \
    --name 'rustc -O search_rotated.rs' --cmd 'rustc -O search_rotated.rs -o target/search_rotated'
ce_cmd --lang c --approach search_rotated --mode native \
    --prepare 'rm -f target/search_rotated_c' \
    --name 'clang -O3 search_rotated.c' --cmd 'clang -O3 search_rotated.c -o target/search_rotated_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach search_rotated --lane seq --mode codegen --path target/search_rotated_kara_seq
size_put --lang rust --approach search_rotated --lane seq --mode native  --path target/search_rotated
size_put --lang c    --approach search_rotated --lane seq --mode native  --path target/search_rotated_c
size_put --lang go   --approach search_rotated --lane seq --mode native  --path target/search_rotated_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach search_rotated --lane seq --mode codegen --bytes "$(mem_peak ./target/search_rotated_kara_seq)"
mem_put --lang rust --approach search_rotated --lane seq --mode native  --bytes "$(mem_peak ./target/search_rotated)"
mem_put --lang c    --approach search_rotated --lane seq --mode native  --bytes "$(mem_peak ./target/search_rotated_c)"
mem_put --lang go   --approach search_rotated --lane seq --mode native  --bytes "$(mem_peak ./target/search_rotated_go_seq)"
mem_put --lang python --approach search_rotated --lane seq --mode interp --bytes "$(mem_peak python3 search_rotated.py)"

echo
echo "=== compile memory (cold) ==="
for src in search_rotated.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in search_rotated.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in search_rotated.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
