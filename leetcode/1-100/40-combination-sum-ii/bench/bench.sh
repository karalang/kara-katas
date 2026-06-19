#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #40.
# See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the sorted same-level-dedup backtracking solver (★): sort the
# duplicate-bearing candidates, then an index-bounded DFS recursing at i+1 (each element
# used once) that skips `candidates[i] == candidates[i-1]` at i > start and suffix-`break`s
# once a candidate exceeds the remaining target, snapshotting the path (`path.clone()`) into
# a `Vec[Vec[i64]]` at each leaf. Like #39 this is a `Vec[Vec]`-ALLOCATION workload:
# recursion + per-node push/pop + a leaf clone + nested-Vec heap growth, here with the
# duplicate-skip dedup of #40.
# Workload: enumerate once-each combinations for a per-iteration target. TOTAL=30000 times,
# with a fixed duplicate-heavy multiset [1,1,2,2,3,3,4,5,6,7] (sorted once), set target =
# 10 + (k % 13) (a per-iteration target, so nothing hoists), solve, and fold a position-
# weighted signature of every combination plus the count into a rolling checksum. The target
# varies with the loop index (no hoisting) and the checksum carries a loop-borne dependency,
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
    local out="target/combination_sum_ii_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust         combination_sum_ii.rs
build_rust_checked combination_sum_ii.rs
build_c            combination_sum_ii.c
build_kara         combination_sum_ii.kara
build_kara_seq     combination_sum_ii.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="71775739"
mismatch=""
for pair in \
    'kara:./target/combination_sum_ii_kara' \
    'kara_seq:./target/combination_sum_ii_kara_seq' \
    'rust:./target/combination_sum_ii' \
    'rust_chk:./target/combination_sum_ii_rschk' \
    'c:./target/combination_sum_ii_c' \
    'go:./target/combination_sum_ii_go_seq'; do
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
    py_out=$(python3 combination_sum_ii.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=40 slug=combination-sum-ii group=1-100 \
    title="Combination Sum II" \
    workload="TOTAL=30000 combination-sum-II enumerations (duplicate-heavy multiset [1,1,2,2,3,3,4,5,6,7] sorted once, target = 10 + k%13), sorted same-level-dedup backtracking (each element used once) with a leaf path.clone() into Vec[Vec[i64]], every combination folded into a position-weighted checksum" \
    sink="$expected"

echo "=== runtime — seq lane (single-threaded mutable-path backtracking) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach combination_sum_ii --lane seq --mode codegen \
    --name 'kara combination_sum_ii (seq, KARAC_AUTO_PAR=0)' --cmd './target/combination_sum_ii_kara_seq'
rt_cmd --lang rust --approach combination_sum_ii --lane seq --mode native \
    --name 'rust combination_sum_ii' --cmd './target/combination_sum_ii'
rt_cmd --lang rust --approach combination_sum_ii_rschk --lane seq --mode native \
    --name 'rust combination_sum_ii (overflow-checks=on, =Kara safety)' --cmd './target/combination_sum_ii_rschk'
rt_cmd --lang c --approach combination_sum_ii --lane seq --mode native \
    --name 'c    combination_sum_ii' --cmd './target/combination_sum_ii_c'
rt_cmd --lang go --approach combination_sum_ii --lane seq --mode native \
    --name 'go   combination_sum_ii' --cmd './target/combination_sum_ii_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 1 --runs 3
rt_cmd --lang python --approach combination_sum_ii --lane seq --mode interp \
    --name 'py   combination_sum_ii' --cmd 'python3 combination_sum_ii.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach combination_sum_ii --mode codegen \
    --prepare 'rm -f target/combination_sum_ii_kara combination_sum_ii' \
    --name 'karac build combination_sum_ii.kara' \
    --cmd 'sh -c "karac build combination_sum_ii.kara >/dev/null && mv combination_sum_ii target/combination_sum_ii_kara"'
ce_cmd --lang rust --approach combination_sum_ii --mode native \
    --prepare 'rm -f target/combination_sum_ii' \
    --name 'rustc -O combination_sum_ii.rs' --cmd 'rustc -O combination_sum_ii.rs -o target/combination_sum_ii'
ce_cmd --lang c --approach combination_sum_ii --mode native \
    --prepare 'rm -f target/combination_sum_ii_c' \
    --name 'clang -O3 combination_sum_ii.c' --cmd 'clang -O3 combination_sum_ii.c -o target/combination_sum_ii_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach combination_sum_ii --lane seq --mode codegen --path target/combination_sum_ii_kara_seq
size_put --lang rust --approach combination_sum_ii --lane seq --mode native  --path target/combination_sum_ii
size_put --lang c    --approach combination_sum_ii --lane seq --mode native  --path target/combination_sum_ii_c
size_put --lang go   --approach combination_sum_ii --lane seq --mode native  --path target/combination_sum_ii_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach combination_sum_ii --lane seq --mode codegen --bytes "$(mem_peak ./target/combination_sum_ii_kara_seq)"
mem_put --lang rust --approach combination_sum_ii --lane seq --mode native  --bytes "$(mem_peak ./target/combination_sum_ii)"
mem_put --lang c    --approach combination_sum_ii --lane seq --mode native  --bytes "$(mem_peak ./target/combination_sum_ii_c)"
mem_put --lang go   --approach combination_sum_ii --lane seq --mode native  --bytes "$(mem_peak ./target/combination_sum_ii_go_seq)"
mem_put --lang python --approach combination_sum_ii --lane seq --mode interp --bytes "$(mem_peak python3 combination_sum_ii.py)"

echo
echo "=== compile memory (cold) ==="
for src in combination_sum_ii.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in combination_sum_ii.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in combination_sum_ii.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
