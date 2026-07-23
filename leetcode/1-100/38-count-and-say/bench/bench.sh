#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #38.
# See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the streaming run-length "say" (★): encode one count-and-say
# step in a single left-to-right pass with a (run_digit, run_len) state machine, building
# the next term as a growing digit String. Unlike #36/#37 (allocation-free fixed grids),
# this exercises String HEAP GROWTH + per-char iteration codegen.
# Workload: count-and-say generalized to an arbitrary digit seed. TOTAL=12000 times, seed
# the sequence with the decimal digits of k+1 (a per-iteration seed, so nothing hoists),
# apply STEPS=14 say-steps, and fold a position-weighted digit signature of the final term
# into a checksum. The seed varies with the loop index (no hoisting) and the checksum
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
    local out="target/count_and_say_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust         count_and_say.rs
build_rust_checked count_and_say.rs
build_c            count_and_say.c
build_kara         count_and_say.kara
build_kara_seq     count_and_say.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="994339104"
mismatch=""
for pair in \
    'kara:./target/count_and_say_kara' \
    'kara_seq:./target/count_and_say_kara_seq' \
    'rust:./target/count_and_say' \
    'rust_chk:./target/count_and_say_rschk' \
    'c:./target/count_and_say_c' \
    'go:./target/count_and_say_go_seq'; do
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
    py_out=$(python3 count_and_say.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=38 slug=count-and-say group=1-100 \
    title="Count and Say" \
    workload="TOTAL=12000 generalized count-and-say runs (seed = decimal of k+1, STEPS=14 streaming run-length say steps, single-digit run counts appended in place), final term folded into a position-weighted digit checksum" \
    sink="$expected"

echo "=== runtime — seq lane (single-threaded streaming run-length say) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach count_and_say --lane seq --mode codegen \
    --name 'kara count_and_say (seq, KARAC_AUTO_PAR=0)' --cmd './target/count_and_say_kara_seq'
rt_cmd --lang rust --approach count_and_say --lane seq --mode native \
    --name 'rust count_and_say' --cmd './target/count_and_say'
rt_cmd --lang rust --approach count_and_say_rschk --lane seq --mode native \
    --name 'rust count_and_say (overflow-checks=on, =Kara safety)' --cmd './target/count_and_say_rschk'
rt_cmd --lang c --approach count_and_say --lane seq --mode native \
    --name 'c    count_and_say' --cmd './target/count_and_say_c'
rt_cmd --lang go --approach count_and_say --lane seq --mode native \
    --name 'go   count_and_say' --cmd './target/count_and_say_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 1 --runs 3
rt_cmd --lang python --approach count_and_say --lane seq --mode interp \
    --name 'py   count_and_say' --cmd 'python3 count_and_say.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach count_and_say --mode codegen \
    --prepare 'rm -f target/count_and_say_kara count_and_say' \
    --name 'karac build count_and_say.kara' \
    --cmd 'sh -c "karac build count_and_say.kara >/dev/null && mv count_and_say target/count_and_say_kara"'
ce_cmd --lang rust --approach count_and_say --mode native \
    --prepare 'rm -f target/count_and_say' \
    --name 'rustc -O count_and_say.rs' --cmd 'rustc -O count_and_say.rs -o target/count_and_say'
ce_cmd --lang c --approach count_and_say --mode native \
    --prepare 'rm -f target/count_and_say_c' \
    --name 'clang -O3 count_and_say.c' --cmd 'clang -O3 count_and_say.c -o target/count_and_say_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach count_and_say --lane seq --mode codegen --path target/count_and_say_kara_seq
size_put --lang rust --approach count_and_say --lane seq --mode native  --path target/count_and_say
size_put --lang c    --approach count_and_say --lane seq --mode native  --path target/count_and_say_c
size_put --lang go   --approach count_and_say --lane seq --mode native  --path target/count_and_say_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach count_and_say --lane seq --mode codegen --bytes "$(mem_peak ./target/count_and_say_kara_seq)"
mem_put --lang rust --approach count_and_say --lane seq --mode native  --bytes "$(mem_peak ./target/count_and_say)"
mem_put --lang c    --approach count_and_say --lane seq --mode native  --bytes "$(mem_peak ./target/count_and_say_c)"
mem_put --lang go   --approach count_and_say --lane seq --mode native  --bytes "$(mem_peak ./target/count_and_say_go_seq)"
mem_put --lang python --approach count_and_say --lane seq --mode interp --bytes "$(mem_peak python3 count_and_say.py)"

echo
echo "=== compile memory (cold) ==="
for src in count_and_say.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in count_and_say.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in count_and_say.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
