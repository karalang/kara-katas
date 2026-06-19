#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #41.
# See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the in-place cyclic-sort solver (★): send each in-range value to
# its home index v-1 by swapping (`nums[v-1] != v` guard caps total swaps at n), then scan
# for the first slot not holding its home value. Unlike #38/#39/#40 (heap-allocating) this
# is ALLOCATION-FREE integer compute on a reused buffer — the in-place-array footing of
# #36/#37.
# Workload: a reused length-N=100 buffer is refilled each iteration with a k-rotated
# permutation of 1..N, one slot is punched out of range to create a k-dependent gap, and the
# cyclic sort finds the missing positive. TOTAL=200000 times, fold the answer into a rolling
# checksum. The buffer is allocated once and overwritten in place (the hot loop allocates
# nothing), the gap location varies with the loop index (no hoisting), and the checksum
# carries a loop-borne dependency,
# so this is a single-lane (seq) bench by construction.
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
    local out="target/first_missing_positive_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust         first_missing_positive.rs
build_rust_checked first_missing_positive.rs
build_c            first_missing_positive.c
build_kara         first_missing_positive.kara
build_kara_seq     first_missing_positive.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="783878544"
mismatch=""
for pair in \
    'kara:./target/first_missing_positive_kara' \
    'kara_seq:./target/first_missing_positive_kara_seq' \
    'rust:./target/first_missing_positive' \
    'rust_chk:./target/first_missing_positive_rschk' \
    'c:./target/first_missing_positive_c' \
    'go:./target/first_missing_positive_go_seq'; do
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
    py_out=$(python3 first_missing_positive.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=41 slug=first-missing-positive group=1-100 \
    title="First Missing Positive" \
    workload="TOTAL=200000 first-missing-positive solves on a reused length-100 buffer (refilled each iteration with a k-rotated permutation of 1..100 plus one punched gap), in-place cyclic-sort (swap each value to its home index v-1, then scan), each answer folded into a rolling checksum" \
    sink="$expected"

echo "=== runtime — seq lane (single-threaded in-place cyclic sort) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach first_missing_positive --lane seq --mode codegen \
    --name 'kara first_missing_positive (seq, KARAC_AUTO_PAR=0)' --cmd './target/first_missing_positive_kara_seq'
rt_cmd --lang rust --approach first_missing_positive --lane seq --mode native \
    --name 'rust first_missing_positive' --cmd './target/first_missing_positive'
rt_cmd --lang rust --approach first_missing_positive_rschk --lane seq --mode native \
    --name 'rust first_missing_positive (overflow-checks=on, =Kara safety)' --cmd './target/first_missing_positive_rschk'
rt_cmd --lang c --approach first_missing_positive --lane seq --mode native \
    --name 'c    first_missing_positive' --cmd './target/first_missing_positive_c'
rt_cmd --lang go --approach first_missing_positive --lane seq --mode native \
    --name 'go   first_missing_positive' --cmd './target/first_missing_positive_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 1 --runs 3
rt_cmd --lang python --approach first_missing_positive --lane seq --mode interp \
    --name 'py   first_missing_positive' --cmd 'python3 first_missing_positive.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach first_missing_positive --mode codegen \
    --prepare 'rm -f target/first_missing_positive_kara first_missing_positive' \
    --name 'karac build first_missing_positive.kara' \
    --cmd 'sh -c "karac build first_missing_positive.kara >/dev/null && mv first_missing_positive target/first_missing_positive_kara"'
ce_cmd --lang rust --approach first_missing_positive --mode native \
    --prepare 'rm -f target/first_missing_positive' \
    --name 'rustc -O first_missing_positive.rs' --cmd 'rustc -O first_missing_positive.rs -o target/first_missing_positive'
ce_cmd --lang c --approach first_missing_positive --mode native \
    --prepare 'rm -f target/first_missing_positive_c' \
    --name 'clang -O3 first_missing_positive.c' --cmd 'clang -O3 first_missing_positive.c -o target/first_missing_positive_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach first_missing_positive --lane seq --mode codegen --path target/first_missing_positive_kara_seq
size_put --lang rust --approach first_missing_positive --lane seq --mode native  --path target/first_missing_positive
size_put --lang c    --approach first_missing_positive --lane seq --mode native  --path target/first_missing_positive_c
size_put --lang go   --approach first_missing_positive --lane seq --mode native  --path target/first_missing_positive_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach first_missing_positive --lane seq --mode codegen --bytes "$(mem_peak ./target/first_missing_positive_kara_seq)"
mem_put --lang rust --approach first_missing_positive --lane seq --mode native  --bytes "$(mem_peak ./target/first_missing_positive)"
mem_put --lang c    --approach first_missing_positive --lane seq --mode native  --bytes "$(mem_peak ./target/first_missing_positive_c)"
mem_put --lang go   --approach first_missing_positive --lane seq --mode native  --bytes "$(mem_peak ./target/first_missing_positive_go_seq)"
mem_put --lang python --approach first_missing_positive --lane seq --mode interp --bytes "$(mem_peak python3 first_missing_positive.py)"

echo
echo "=== compile memory (cold) ==="
for src in first_missing_positive.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in first_missing_positive.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in first_missing_positive.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
