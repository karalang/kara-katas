#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #45.
# See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the greedy range-expansion matcher (★): one cursor with
# farthest/current_end/jumps scalars collapsing the layered BFS into a single left-to-right
# scan. O(1) space; O(n) time.
# Workload: build a reachable array nums (length 1000, each entry in 1..4 so every index can
# always step at least one forward) ONCE, then TOTAL=200000 times punch a single slot
# (nums[k%n] = 1 + k%9 — a bigger reach that shortens some jumps), run the greedy min-jumps
# scan, and fold the jump count into a rolling checksum. The punches are NOT reverted, so the
# array state carries forward and the answer varies with the loop index (no hoisting); the
# checksum carries a loop-borne dependency, so this is a single-lane (seq) bench by construction.
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
    local out="target/jump_game_ii_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust         jump_game_ii.rs
build_rust_checked jump_game_ii.rs
build_c            jump_game_ii.c
build_kara         jump_game_ii.kara
build_kara_seq     jump_game_ii.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="92502267"
mismatch=""
for pair in \
    'kara:./target/jump_game_ii_kara' \
    'kara_seq:./target/jump_game_ii_kara_seq' \
    'rust:./target/jump_game_ii' \
    'rust_chk:./target/jump_game_ii_rschk' \
    'c:./target/jump_game_ii_c' \
    'go:./target/jump_game_ii_go_seq'; do
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
    py_out=$(python3 jump_game_ii.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=45 slug=jump-game-ii group=1-100 \
    title="Jump Game II" \
    workload="TOTAL=200000 minimum-jumps solves on a length-1000 reachable array (entries 1..4, built once) with one slot punched per iteration (nums[k%n]=1+k%9) to widen a reach and shift the jump count, greedy range expansion (one cursor; farthest = running max of i+nums[i], spend a jump and extend current_end on reaching the layer boundary), each answer folded into a rolling checksum" \
    sink="$expected"

echo "=== runtime — seq lane (single-threaded greedy range expansion) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach jump_game_ii --lane seq --mode codegen \
    --name 'kara jump_game_ii (seq, KARAC_AUTO_PAR=0)' --cmd './target/jump_game_ii_kara_seq'
rt_cmd --lang rust --approach jump_game_ii --lane seq --mode native \
    --name 'rust jump_game_ii' --cmd './target/jump_game_ii'
rt_cmd --lang rust --approach jump_game_ii_rschk --lane seq --mode native \
    --name 'rust jump_game_ii (overflow-checks=on, =Kara safety)' --cmd './target/jump_game_ii_rschk'
rt_cmd --lang c --approach jump_game_ii --lane seq --mode native \
    --name 'c    jump_game_ii' --cmd './target/jump_game_ii_c'
rt_cmd --lang go --approach jump_game_ii --lane seq --mode native \
    --name 'go   jump_game_ii' --cmd './target/jump_game_ii_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 1 --runs 3
rt_cmd --lang python --approach jump_game_ii --lane seq --mode interp \
    --name 'py   jump_game_ii' --cmd 'python3 jump_game_ii.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach jump_game_ii --mode codegen \
    --prepare 'rm -f target/jump_game_ii_kara jump_game_ii' \
    --name 'karac build jump_game_ii.kara' \
    --cmd 'sh -c "karac build jump_game_ii.kara >/dev/null && mv jump_game_ii target/jump_game_ii_kara"'
ce_cmd --lang rust --approach jump_game_ii --mode native \
    --prepare 'rm -f target/jump_game_ii' \
    --name 'rustc -O jump_game_ii.rs' --cmd 'rustc -O jump_game_ii.rs -o target/jump_game_ii'
ce_cmd --lang c --approach jump_game_ii --mode native \
    --prepare 'rm -f target/jump_game_ii_c' \
    --name 'clang -O3 jump_game_ii.c' --cmd 'clang -O3 jump_game_ii.c -o target/jump_game_ii_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach jump_game_ii --lane seq --mode codegen --path target/jump_game_ii_kara_seq
size_put --lang rust --approach jump_game_ii --lane seq --mode native  --path target/jump_game_ii
size_put --lang c    --approach jump_game_ii --lane seq --mode native  --path target/jump_game_ii_c
size_put --lang go   --approach jump_game_ii --lane seq --mode native  --path target/jump_game_ii_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach jump_game_ii --lane seq --mode codegen --bytes "$(mem_peak ./target/jump_game_ii_kara_seq)"
mem_put --lang rust --approach jump_game_ii --lane seq --mode native  --bytes "$(mem_peak ./target/jump_game_ii)"
mem_put --lang c    --approach jump_game_ii --lane seq --mode native  --bytes "$(mem_peak ./target/jump_game_ii_c)"
mem_put --lang go   --approach jump_game_ii --lane seq --mode native  --bytes "$(mem_peak ./target/jump_game_ii_go_seq)"
mem_put --lang python --approach jump_game_ii --lane seq --mode interp --bytes "$(mem_peak python3 jump_game_ii.py)"

echo
echo "=== compile memory (cold) ==="
for src in jump_game_ii.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in jump_game_ii.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in jump_game_ii.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
