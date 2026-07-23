#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #34.
# See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the two-bounds style (★): per query, two textbook
# half-open binary searches — lower_bound (first index >= target) and upper_bound
# (first index > target) — that pin both ends of the target's run in O(log n).
# Pure branchy integer compute, no allocation in the hot loop, and TWO searches
# per query (~2× #33's per-call work, so TOTAL is scaled down to match the band).
# Workload: build one fixed sorted array of length N=4096 once (nums[p]=2*(p/RUN),
# RUN=4 — non-decreasing, each even value repeated 4×, odd values absent), then
# run the first+last query TOTAL=14M times for targets cycling through [0, 2N) so
# all four control-flow paths (hit / odd-miss / over-miss / boundary) fire. The
# target varies with the loop index, so no comparator can hoist the pure query
# out of the loop; fold both endpoints into a checksum (the un-elidable sink). The
# accumulator carries a loop-borne dependency, so this is a single-lane (seq)
# bench by construction.
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
    local out="target/search_range_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust         search_range.rs
build_rust_checked search_range.rs
build_c            search_range.c
build_kara         search_range.kara
build_kara_seq     search_range.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="421417033"
mismatch=""
for pair in \
    'kara:./target/search_range_kara' \
    'kara_seq:./target/search_range_kara_seq' \
    'rust:./target/search_range' \
    'rust_chk:./target/search_range_rschk' \
    'c:./target/search_range_c' \
    'go:./target/search_range_go_seq'; do
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
    py_out=$(python3 search_range.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=34 slug=find-first-and-last-position group=1-100 \
    title="Find First and Last Position of Element in Sorted Array" \
    workload="TOTAL=14M first+last queries (lower_bound+upper_bound) over a fixed sorted 4096-array with length-4 dup runs, cycling targets + checksum" \
    sink="$expected"

echo "=== runtime — seq lane (single-threaded two-bounds binary search) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach search_range --lane seq --mode codegen \
    --name 'kara search_range (seq, KARAC_AUTO_PAR=0)' --cmd './target/search_range_kara_seq'
rt_cmd --lang rust --approach search_range --lane seq --mode native \
    --name 'rust search_range' --cmd './target/search_range'
rt_cmd --lang rust --approach search_range_rschk --lane seq --mode native \
    --name 'rust search_range (overflow-checks=on, =Kara safety)' --cmd './target/search_range_rschk'
rt_cmd --lang c --approach search_range --lane seq --mode native \
    --name 'c    search_range' --cmd './target/search_range_c'
rt_cmd --lang go --approach search_range --lane seq --mode native \
    --name 'go   search_range' --cmd './target/search_range_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 1 --runs 3
rt_cmd --lang python --approach search_range --lane seq --mode interp \
    --name 'py   search_range' --cmd 'python3 search_range.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach search_range --mode codegen \
    --prepare 'rm -f target/search_range_kara search_range' \
    --name 'karac build search_range.kara' \
    --cmd 'sh -c "karac build search_range.kara >/dev/null && mv search_range target/search_range_kara"'
ce_cmd --lang rust --approach search_range --mode native \
    --prepare 'rm -f target/search_range' \
    --name 'rustc -O search_range.rs' --cmd 'rustc -O search_range.rs -o target/search_range'
ce_cmd --lang c --approach search_range --mode native \
    --prepare 'rm -f target/search_range_c' \
    --name 'clang -O3 search_range.c' --cmd 'clang -O3 search_range.c -o target/search_range_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach search_range --lane seq --mode codegen --path target/search_range_kara_seq
size_put --lang rust --approach search_range --lane seq --mode native  --path target/search_range
size_put --lang c    --approach search_range --lane seq --mode native  --path target/search_range_c
size_put --lang go   --approach search_range --lane seq --mode native  --path target/search_range_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach search_range --lane seq --mode codegen --bytes "$(mem_peak ./target/search_range_kara_seq)"
mem_put --lang rust --approach search_range --lane seq --mode native  --bytes "$(mem_peak ./target/search_range)"
mem_put --lang c    --approach search_range --lane seq --mode native  --bytes "$(mem_peak ./target/search_range_c)"
mem_put --lang go   --approach search_range --lane seq --mode native  --bytes "$(mem_peak ./target/search_range_go_seq)"
mem_put --lang python --approach search_range --lane seq --mode interp --bytes "$(mem_peak python3 search_range.py)"

echo
echo "=== compile memory (cold) ==="
for src in search_range.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in search_range.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in search_range.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
