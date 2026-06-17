#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #36.
# See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the single-pass bitmask style (★): validate a 9×9 board
# in one pass with three nine-element bitmask arrays (rows / cols / boxes), early
# returning on the first duplicate. Pure branchy integer compute over a fixed-size
# grid, NO heap allocation in the hot path (board + masks are all stack storage),
# so this measures validation codegen rather than the allocator.
# Workload: build one fixed fully-solved (valid) board as a flat 81-int array, then
# TOTAL=5M times perturb cell `k % 81` to digit `(k % 9) + 1`, validate, fold the
# boolean verdict into a checksum, and restore the cell. The perturbation varies
# with the loop index (no hoisting), ~half introduce a duplicate (early-return path)
# and ~half leave a valid board (full 81-cell scan). The accumulator carries a
# loop-borne dependency, so this is a single-lane (seq) bench by construction.
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
    local out="target/valid_sudoku_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust         valid_sudoku.rs
build_rust_checked valid_sudoku.rs
build_c            valid_sudoku.c
build_kara         valid_sudoku.kara
build_kara_seq     valid_sudoku.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="291807572"
mismatch=""
for pair in \
    'kara:./target/valid_sudoku_kara' \
    'kara_seq:./target/valid_sudoku_kara_seq' \
    'rust:./target/valid_sudoku' \
    'rust_chk:./target/valid_sudoku_rschk' \
    'c:./target/valid_sudoku_c' \
    'go:./target/valid_sudoku_go_seq'; do
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
    py_out=$(python3 valid_sudoku.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=36 slug=valid-sudoku group=1-100 \
    title="Valid Sudoku" \
    workload="TOTAL=5M single-pass bitmask validations of a perturbed fully-solved 9x9 board (perturb-validate-restore), verdict folded into a checksum" \
    sink="$expected"

echo "=== runtime — seq lane (single-threaded single-pass bitmask validation) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach valid_sudoku --lane seq --mode codegen \
    --name 'kara valid_sudoku (seq, KARAC_AUTO_PAR=0)' --cmd './target/valid_sudoku_kara_seq'
rt_cmd --lang rust --approach valid_sudoku --lane seq --mode native \
    --name 'rust valid_sudoku' --cmd './target/valid_sudoku'
rt_cmd --lang rust --approach valid_sudoku_rschk --lane seq --mode native \
    --name 'rust valid_sudoku (overflow-checks=on, =Kara safety)' --cmd './target/valid_sudoku_rschk'
rt_cmd --lang c --approach valid_sudoku --lane seq --mode native \
    --name 'c    valid_sudoku' --cmd './target/valid_sudoku_c'
rt_cmd --lang go --approach valid_sudoku --lane seq --mode native \
    --name 'go   valid_sudoku' --cmd './target/valid_sudoku_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 1 --runs 3
rt_cmd --lang python --approach valid_sudoku --lane seq --mode interp \
    --name 'py   valid_sudoku' --cmd 'python3 valid_sudoku.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach valid_sudoku --mode codegen \
    --prepare 'rm -f target/valid_sudoku_kara valid_sudoku' \
    --name 'karac build valid_sudoku.kara' \
    --cmd 'sh -c "karac build valid_sudoku.kara >/dev/null && mv valid_sudoku target/valid_sudoku_kara"'
ce_cmd --lang rust --approach valid_sudoku --mode native \
    --prepare 'rm -f target/valid_sudoku' \
    --name 'rustc -O valid_sudoku.rs' --cmd 'rustc -O valid_sudoku.rs -o target/valid_sudoku'
ce_cmd --lang c --approach valid_sudoku --mode native \
    --prepare 'rm -f target/valid_sudoku_c' \
    --name 'clang -O3 valid_sudoku.c' --cmd 'clang -O3 valid_sudoku.c -o target/valid_sudoku_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach valid_sudoku --lane seq --mode codegen --path target/valid_sudoku_kara_seq
size_put --lang rust --approach valid_sudoku --lane seq --mode native  --path target/valid_sudoku
size_put --lang c    --approach valid_sudoku --lane seq --mode native  --path target/valid_sudoku_c
size_put --lang go   --approach valid_sudoku --lane seq --mode native  --path target/valid_sudoku_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach valid_sudoku --lane seq --mode codegen --bytes "$(mem_peak ./target/valid_sudoku_kara_seq)"
mem_put --lang rust --approach valid_sudoku --lane seq --mode native  --bytes "$(mem_peak ./target/valid_sudoku)"
mem_put --lang c    --approach valid_sudoku --lane seq --mode native  --bytes "$(mem_peak ./target/valid_sudoku_c)"
mem_put --lang go   --approach valid_sudoku --lane seq --mode native  --bytes "$(mem_peak ./target/valid_sudoku_go_seq)"
mem_put --lang python --approach valid_sudoku --lane seq --mode interp --bytes "$(mem_peak python3 valid_sudoku.py)"

echo
echo "=== compile memory (cold) ==="
for src in valid_sudoku.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in valid_sudoku.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in valid_sudoku.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
