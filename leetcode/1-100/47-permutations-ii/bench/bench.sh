#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #47.
# See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the sorted used-array adjacent-skip backtracker (★): a DFS that at each
# level picks any still-unused element (tracked by a `Vec[bool]` `used` marker) with the input
# SORTED up front and a same-level adjacent-duplicate skip (`nums[i] == nums[i-1] and not
# used[i-1]`), so a duplicate-laden input yields each UNIQUE ordering once. The path is a mutable
# Vec with push/pop + flag flip/unflip, snapshotted (`path.clone()`) into a `Vec[Vec[i64]]` at each
# leaf (`path.len() == n`). Like #46/#40 this is a `Vec[Vec]`-ALLOCATION workload: recursion +
# per-node push/pop + a leaf clone + nested-Vec heap growth, here the unique permutation
# enumeration of a duplicate-bearing multiset rather than #46's distinct-input one.
# Workload: a fixed-size n=8 multiset drawn from {1,2,3,4}. TOTAL=600 times, punch one slot
# (`nums[k%n] = 1 + k%4`, not reverted so the multiset state carries forward), sort a working copy,
# solve, and fold a position-weighted signature of every permutation plus the count into a rolling
# checksum. The punched values vary with the loop index (no hoisting of a constant result) and the
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
    local out="target/permutations_ii_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust         permutations_ii.rs
build_rust_checked permutations_ii.rs
build_c            permutations_ii.c
build_kara         permutations_ii.kara
build_kara_seq     permutations_ii.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="863540794"
mismatch=""
for pair in \
    'kara:./target/permutations_ii_kara' \
    'kara_seq:./target/permutations_ii_kara_seq' \
    'rust:./target/permutations_ii' \
    'rust_chk:./target/permutations_ii_rschk' \
    'c:./target/permutations_ii_c' \
    'go:./target/permutations_ii_go_seq'; do
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
    py_out=$(python3 permutations_ii.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=47 slug=permutations-ii group=1-100 \
    title="Permutations II" \
    workload="TOTAL=600 unique-permutation enumerations of a fixed n=8 multiset from {1,2,3,4} (one slot punched per iteration nums[k%n]=1+k%4, not reverted), sorted used-array adjacent-skip backtracking with a leaf path.clone() into Vec[Vec[i64]], every permutation folded into a position-weighted checksum" \
    sink="$expected"

echo "=== runtime — seq lane (single-threaded sorted adjacent-skip backtracking) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach permutations_ii --lane seq --mode codegen \
    --name 'kara permutations_ii (seq, KARAC_AUTO_PAR=0)' --cmd './target/permutations_ii_kara_seq'
rt_cmd --lang rust --approach permutations_ii --lane seq --mode native \
    --name 'rust permutations_ii' --cmd './target/permutations_ii'
rt_cmd --lang rust --approach permutations_ii_rschk --lane seq --mode native \
    --name 'rust permutations_ii (overflow-checks=on, =Kara safety)' --cmd './target/permutations_ii_rschk'
rt_cmd --lang c --approach permutations_ii --lane seq --mode native \
    --name 'c    permutations_ii' --cmd './target/permutations_ii_c'
rt_cmd --lang go --approach permutations_ii --lane seq --mode native \
    --name 'go   permutations_ii' --cmd './target/permutations_ii_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 1 --runs 3
rt_cmd --lang python --approach permutations_ii --lane seq --mode interp \
    --name 'py   permutations_ii' --cmd 'python3 permutations_ii.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach permutations_ii --mode codegen \
    --prepare 'rm -f target/permutations_ii_kara permutations_ii' \
    --name 'karac build permutations_ii.kara' \
    --cmd 'sh -c "karac build permutations_ii.kara >/dev/null && mv permutations_ii target/permutations_ii_kara"'
ce_cmd --lang rust --approach permutations_ii --mode native \
    --prepare 'rm -f target/permutations_ii' \
    --name 'rustc -O permutations_ii.rs' --cmd 'rustc -O permutations_ii.rs -o target/permutations_ii'
ce_cmd --lang c --approach permutations_ii --mode native \
    --prepare 'rm -f target/permutations_ii_c' \
    --name 'clang -O3 permutations_ii.c' --cmd 'clang -O3 permutations_ii.c -o target/permutations_ii_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach permutations_ii --lane seq --mode codegen --path target/permutations_ii_kara_seq
size_put --lang rust --approach permutations_ii --lane seq --mode native  --path target/permutations_ii
size_put --lang c    --approach permutations_ii --lane seq --mode native  --path target/permutations_ii_c
size_put --lang go   --approach permutations_ii --lane seq --mode native  --path target/permutations_ii_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach permutations_ii --lane seq --mode codegen --bytes "$(mem_peak ./target/permutations_ii_kara_seq)"
mem_put --lang rust --approach permutations_ii --lane seq --mode native  --bytes "$(mem_peak ./target/permutations_ii)"
mem_put --lang c    --approach permutations_ii --lane seq --mode native  --bytes "$(mem_peak ./target/permutations_ii_c)"
mem_put --lang go   --approach permutations_ii --lane seq --mode native  --bytes "$(mem_peak ./target/permutations_ii_go_seq)"
mem_put --lang python --approach permutations_ii --lane seq --mode interp --bytes "$(mem_peak python3 permutations_ii.py)"

echo
echo "=== compile memory (cold) ==="
for src in permutations_ii.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in permutations_ii.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in permutations_ii.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
