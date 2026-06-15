#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #32.
# See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the index-stack longest-valid-parentheses (★ style):
# a Vec[i64] stack of unmatched-boundary indices with a -1 base sentinel,
# allocated FRESH per call (as the solution function does). Workload: build one
# fixed pseudo-random parens buffer of length L=4096 once, then run longest_valid
# over a SLIDING WINDOW [start, start+W=2048) of it TOTAL=330K times, the window
# offset varying with the iteration index so no comparator can fold the pure call
# out of the loop; fold each window's answer into a checksum (the un-elidable
# sink). The loop accumulates into one scalar with a loop-borne dependency, so it
# does not auto-parallelize — a single-lane (seq) bench by construction.
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
    local out="target/longest_valid_parentheses_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust         longest_valid_parentheses.rs
build_rust_checked longest_valid_parentheses.rs
build_c            longest_valid_parentheses.c
build_kara         longest_valid_parentheses.kara
build_kara_seq     longest_valid_parentheses.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="675510162"
mismatch=""
for pair in \
    'kara:./target/longest_valid_parentheses_kara' \
    'kara_seq:./target/longest_valid_parentheses_kara_seq' \
    'rust:./target/longest_valid_parentheses' \
    'rust_chk:./target/longest_valid_parentheses_rschk' \
    'c:./target/longest_valid_parentheses_c' \
    'go:./target/longest_valid_parentheses_go_seq'; do
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
    py_out=$(python3 longest_valid_parentheses.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=32 slug=longest-valid-parentheses group=1-100 \
    title="Longest Valid Parentheses" \
    workload="TOTAL=330K sliding windows (W=2048) of a fixed 4096 parens buffer, index-stack longest-valid + checksum" \
    sink="$expected"

echo "=== runtime — seq lane (single-threaded sliding-window scan) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach longest_valid_parentheses --lane seq --mode codegen \
    --name 'kara longest_valid_parentheses (seq, KARAC_AUTO_PAR=0)' --cmd './target/longest_valid_parentheses_kara_seq'
rt_cmd --lang rust --approach longest_valid_parentheses --lane seq --mode native \
    --name 'rust longest_valid_parentheses' --cmd './target/longest_valid_parentheses'
rt_cmd --lang rust --approach longest_valid_parentheses_rschk --lane seq --mode native \
    --name 'rust longest_valid_parentheses (overflow-checks=on, =Kara safety)' --cmd './target/longest_valid_parentheses_rschk'
rt_cmd --lang c --approach longest_valid_parentheses --lane seq --mode native \
    --name 'c    longest_valid_parentheses' --cmd './target/longest_valid_parentheses_c'
rt_cmd --lang go --approach longest_valid_parentheses --lane seq --mode native \
    --name 'go   longest_valid_parentheses' --cmd './target/longest_valid_parentheses_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 1 --runs 3
rt_cmd --lang python --approach longest_valid_parentheses --lane seq --mode interp \
    --name 'py   longest_valid_parentheses' --cmd 'python3 longest_valid_parentheses.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach longest_valid_parentheses --mode codegen \
    --prepare 'rm -f target/longest_valid_parentheses_kara longest_valid_parentheses' \
    --name 'karac build longest_valid_parentheses.kara' \
    --cmd 'sh -c "karac build longest_valid_parentheses.kara >/dev/null && mv longest_valid_parentheses target/longest_valid_parentheses_kara"'
ce_cmd --lang rust --approach longest_valid_parentheses --mode native \
    --prepare 'rm -f target/longest_valid_parentheses' \
    --name 'rustc -O longest_valid_parentheses.rs' --cmd 'rustc -O longest_valid_parentheses.rs -o target/longest_valid_parentheses'
ce_cmd --lang c --approach longest_valid_parentheses --mode native \
    --prepare 'rm -f target/longest_valid_parentheses_c' \
    --name 'clang -O3 longest_valid_parentheses.c' --cmd 'clang -O3 longest_valid_parentheses.c -o target/longest_valid_parentheses_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach longest_valid_parentheses --lane seq --mode codegen --path target/longest_valid_parentheses_kara_seq
size_put --lang rust --approach longest_valid_parentheses --lane seq --mode native  --path target/longest_valid_parentheses
size_put --lang c    --approach longest_valid_parentheses --lane seq --mode native  --path target/longest_valid_parentheses_c
size_put --lang go   --approach longest_valid_parentheses --lane seq --mode native  --path target/longest_valid_parentheses_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach longest_valid_parentheses --lane seq --mode codegen --bytes "$(mem_peak ./target/longest_valid_parentheses_kara_seq)"
mem_put --lang rust --approach longest_valid_parentheses --lane seq --mode native  --bytes "$(mem_peak ./target/longest_valid_parentheses)"
mem_put --lang c    --approach longest_valid_parentheses --lane seq --mode native  --bytes "$(mem_peak ./target/longest_valid_parentheses_c)"
mem_put --lang go   --approach longest_valid_parentheses --lane seq --mode native  --bytes "$(mem_peak ./target/longest_valid_parentheses_go_seq)"
mem_put --lang python --approach longest_valid_parentheses --lane seq --mode interp --bytes "$(mem_peak python3 longest_valid_parentheses.py)"

echo
echo "=== compile memory (cold) ==="
for src in longest_valid_parentheses.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in longest_valid_parentheses.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in longest_valid_parentheses.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
