#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #37.
# See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the bitmask-backtracking solver (★): solve a 9×9 board by
# depth-first search with three nine-element bitmask arrays (rows / cols / boxes),
# linear cell order, ascending digit order, XOR undo. Recursion + branchy mask
# arithmetic over a fixed-size grid, NO heap allocation in the hot path (board + masks
# are all stack storage), so this measures backtracking-search codegen rather than the
# allocator.
# Workload: the template is Arto Inkala's 2012 "world's hardest sudoku". TOTAL=500
# times, copy it into a fresh working board, CLEAR cell k%81 (removing a clue keeps it
# solvable), solve, and fold a position-weighted signature of the solved grid
# (sum board[i]*(i+1) — an unweighted sum is 405 for any complete board) into a
# checksum. The cleared cell varies with the loop index (no hoisting), and the checksum
# carries a loop-borne dependency, so this is a single-lane (seq) bench by construction.
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
    local out="target/sudoku_solver_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust         sudoku_solver.rs
build_rust_checked sudoku_solver.rs
build_c            sudoku_solver.c
build_kara         sudoku_solver.kara
build_kara_seq     sudoku_solver.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="667470979"
mismatch=""
for pair in \
    'kara:./target/sudoku_solver_kara' \
    'kara_seq:./target/sudoku_solver_kara_seq' \
    'rust:./target/sudoku_solver' \
    'rust_chk:./target/sudoku_solver_rschk' \
    'c:./target/sudoku_solver_c' \
    'go:./target/sudoku_solver_go_seq'; do
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
    py_out=$(python3 sudoku_solver.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=37 slug=sudoku-solver group=1-100 \
    title="Sudoku Solver" \
    workload="TOTAL=500 bitmask-backtracking solves of the world's hardest sudoku (Inkala 2012) with cell k%81 cleared per iteration, solved grid folded into a position-weighted checksum" \
    sink="$expected"

echo "=== runtime — seq lane (single-threaded bitmask-backtracking solve) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach sudoku_solver --lane seq --mode codegen \
    --name 'kara sudoku_solver (seq, KARAC_AUTO_PAR=0)' --cmd './target/sudoku_solver_kara_seq'
rt_cmd --lang rust --approach sudoku_solver --lane seq --mode native \
    --name 'rust sudoku_solver' --cmd './target/sudoku_solver'
rt_cmd --lang rust --approach sudoku_solver_rschk --lane seq --mode native \
    --name 'rust sudoku_solver (overflow-checks=on, =Kara safety)' --cmd './target/sudoku_solver_rschk'
rt_cmd --lang c --approach sudoku_solver --lane seq --mode native \
    --name 'c    sudoku_solver' --cmd './target/sudoku_solver_c'
rt_cmd --lang go --approach sudoku_solver --lane seq --mode native \
    --name 'go   sudoku_solver' --cmd './target/sudoku_solver_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 1 --runs 3
rt_cmd --lang python --approach sudoku_solver --lane seq --mode interp \
    --name 'py   sudoku_solver' --cmd 'python3 sudoku_solver.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach sudoku_solver --mode codegen \
    --prepare 'rm -f target/sudoku_solver_kara sudoku_solver' \
    --name 'karac build sudoku_solver.kara' \
    --cmd 'sh -c "karac build sudoku_solver.kara >/dev/null && mv sudoku_solver target/sudoku_solver_kara"'
ce_cmd --lang rust --approach sudoku_solver --mode native \
    --prepare 'rm -f target/sudoku_solver' \
    --name 'rustc -O sudoku_solver.rs' --cmd 'rustc -O sudoku_solver.rs -o target/sudoku_solver'
ce_cmd --lang c --approach sudoku_solver --mode native \
    --prepare 'rm -f target/sudoku_solver_c' \
    --name 'clang -O3 sudoku_solver.c' --cmd 'clang -O3 sudoku_solver.c -o target/sudoku_solver_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach sudoku_solver --lane seq --mode codegen --path target/sudoku_solver_kara_seq
size_put --lang rust --approach sudoku_solver --lane seq --mode native  --path target/sudoku_solver
size_put --lang c    --approach sudoku_solver --lane seq --mode native  --path target/sudoku_solver_c
size_put --lang go   --approach sudoku_solver --lane seq --mode native  --path target/sudoku_solver_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach sudoku_solver --lane seq --mode codegen --bytes "$(mem_peak ./target/sudoku_solver_kara_seq)"
mem_put --lang rust --approach sudoku_solver --lane seq --mode native  --bytes "$(mem_peak ./target/sudoku_solver)"
mem_put --lang c    --approach sudoku_solver --lane seq --mode native  --bytes "$(mem_peak ./target/sudoku_solver_c)"
mem_put --lang go   --approach sudoku_solver --lane seq --mode native  --bytes "$(mem_peak ./target/sudoku_solver_go_seq)"
mem_put --lang python --approach sudoku_solver --lane seq --mode interp --bytes "$(mem_peak python3 sudoku_solver.py)"

echo
echo "=== compile memory (cold) ==="
for src in sudoku_solver.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in sudoku_solver.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in sudoku_solver.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
