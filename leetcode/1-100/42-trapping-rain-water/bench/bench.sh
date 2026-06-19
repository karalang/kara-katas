#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #42.
# See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the converging two-pointer solver (★): advance the pointer on the
# shorter outer wall, settling each column with that side's running max (no far-side
# lookahead). This is ALLOCATION-FREE O(1)-space integer compute on a reused buffer — no Vec
# growth, no clone — the same in-place-scan footing as #41's cyclic sort.
# Workload: build a jagged length-N=1000 terrain ((i*37)%100) ONCE, then TOTAL=200000 times
# punch a single slot (height[k%n] = (k*19)%100 — an O(1) tweak that shifts the basins so the
# answer changes with k), run the two-pointer solve, and fold the answer into a rolling
# checksum. The per-iteration cost is the non-vectorizable converging scan itself, not an O(n)
# refill; the hot loop allocates nothing, the answer varies with the loop index (no hoisting),
# and the checksum carries a loop-borne dependency, so this is a single-lane (seq) bench by
# construction. NOTE: clang -O3 / rustc -O lower the scan's lone branch as a branchless `csel`
# chain that serializes the pointer updates (latency-bound, ~3× slower here, terrain-
# independent); Kāra and `rustc -C overflow-checks=on` keep the predicted branch and tie. See
# ../README.md § Benchmarks.
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
    local out="target/trapping_rain_water_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust         trapping_rain_water.rs
build_rust_checked trapping_rain_water.rs
build_c            trapping_rain_water.c
build_kara         trapping_rain_water.kara
build_kara_seq     trapping_rain_water.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="111821755"
mismatch=""
for pair in \
    'kara:./target/trapping_rain_water_kara' \
    'kara_seq:./target/trapping_rain_water_kara_seq' \
    'rust:./target/trapping_rain_water' \
    'rust_chk:./target/trapping_rain_water_rschk' \
    'c:./target/trapping_rain_water_c' \
    'go:./target/trapping_rain_water_go_seq'; do
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
    py_out=$(python3 trapping_rain_water.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=42 slug=trapping-rain-water group=1-100 \
    title="Trapping Rain Water" \
    workload="TOTAL=200000 trapping-rain-water solves on a length-1000 terrain ((i*37)%100) built once, with one slot punched per iteration (height[k%n]=(k*19)%100) to shift the basins, converging two-pointer (advance the shorter outer wall, settle each column with its running max), each answer folded into a rolling checksum" \
    sink="$expected"

echo "=== runtime — seq lane (single-threaded converging two-pointer) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach trapping_rain_water --lane seq --mode codegen \
    --name 'kara trapping_rain_water (seq, KARAC_AUTO_PAR=0)' --cmd './target/trapping_rain_water_kara_seq'
rt_cmd --lang rust --approach trapping_rain_water --lane seq --mode native \
    --name 'rust trapping_rain_water' --cmd './target/trapping_rain_water'
rt_cmd --lang rust --approach trapping_rain_water_rschk --lane seq --mode native \
    --name 'rust trapping_rain_water (overflow-checks=on, =Kara safety)' --cmd './target/trapping_rain_water_rschk'
rt_cmd --lang c --approach trapping_rain_water --lane seq --mode native \
    --name 'c    trapping_rain_water' --cmd './target/trapping_rain_water_c'
rt_cmd --lang go --approach trapping_rain_water --lane seq --mode native \
    --name 'go   trapping_rain_water' --cmd './target/trapping_rain_water_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 1 --runs 3
rt_cmd --lang python --approach trapping_rain_water --lane seq --mode interp \
    --name 'py   trapping_rain_water' --cmd 'python3 trapping_rain_water.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach trapping_rain_water --mode codegen \
    --prepare 'rm -f target/trapping_rain_water_kara trapping_rain_water' \
    --name 'karac build trapping_rain_water.kara' \
    --cmd 'sh -c "karac build trapping_rain_water.kara >/dev/null && mv trapping_rain_water target/trapping_rain_water_kara"'
ce_cmd --lang rust --approach trapping_rain_water --mode native \
    --prepare 'rm -f target/trapping_rain_water' \
    --name 'rustc -O trapping_rain_water.rs' --cmd 'rustc -O trapping_rain_water.rs -o target/trapping_rain_water'
ce_cmd --lang c --approach trapping_rain_water --mode native \
    --prepare 'rm -f target/trapping_rain_water_c' \
    --name 'clang -O3 trapping_rain_water.c' --cmd 'clang -O3 trapping_rain_water.c -o target/trapping_rain_water_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach trapping_rain_water --lane seq --mode codegen --path target/trapping_rain_water_kara_seq
size_put --lang rust --approach trapping_rain_water --lane seq --mode native  --path target/trapping_rain_water
size_put --lang c    --approach trapping_rain_water --lane seq --mode native  --path target/trapping_rain_water_c
size_put --lang go   --approach trapping_rain_water --lane seq --mode native  --path target/trapping_rain_water_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach trapping_rain_water --lane seq --mode codegen --bytes "$(mem_peak ./target/trapping_rain_water_kara_seq)"
mem_put --lang rust --approach trapping_rain_water --lane seq --mode native  --bytes "$(mem_peak ./target/trapping_rain_water)"
mem_put --lang c    --approach trapping_rain_water --lane seq --mode native  --bytes "$(mem_peak ./target/trapping_rain_water_c)"
mem_put --lang go   --approach trapping_rain_water --lane seq --mode native  --bytes "$(mem_peak ./target/trapping_rain_water_go_seq)"
mem_put --lang python --approach trapping_rain_water --lane seq --mode interp --bytes "$(mem_peak python3 trapping_rain_water.py)"

echo
echo "=== compile memory (cold) ==="
for src in trapping_rain_water.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in trapping_rain_water.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in trapping_rain_water.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
