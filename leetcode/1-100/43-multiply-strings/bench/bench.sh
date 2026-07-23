#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #43.
# See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the digit-grid multiply + digit-table render (the ★
# style), run as a SEQUENTIAL string-building workload — the lexer's real shape:
# concatenate the product-string of TOTAL=300K distinct multiplications (a fixed
# 38-digit operand × decimal(k)) into one growing output buffer, then byte-checksum
# it. Persisting the output is what keeps the measurement honest: a per-result
# byte-sum would let an optimizing comparator (rustc/clang/go) elide the heap
# String and fold the work to arithmetic, but a buffer that is built up and then
# observed cannot be elided. The build carries a loop-borne dependency on the
# buffer, so it does not auto-parallelize — this is a single-lane (seq) bench by
# construction (the kara binary's only reduction is the negligible trailing
# checksum, so the auto-par and KARAC_AUTO_PAR=0 binaries are equivalent here;
# the seq binary is benched for the clean single-threaded number).
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

# Equal-safety Rust twin: rustc with overflow checks ON, matching kāra's
# default-checked arithmetic. The runtime-only `rust_ovf` lane overlays this on
# the chart so the safety tax that `rust -O`'s silent wrapping hides is visible.
build_rust_ovf() {
    local src="$1"
    local out="target/$(basename "$src" .rs)_ovf"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src (overflow-checks=on, equal-safety) ..." >&2
        rustc -O -C overflow-checks=on "$src" -o "$out"
    fi
}

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
# `rustc -O` alone silently WRAPS on overflow; this `-C overflow-checks=on`
# variant traps like Kāra. The grid partial products (`d1·d2` ≤ 81, slot sums
# bounded) never overflow, so the safety tax isolates allocation throughput.
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
    local out="target/multiply_strings_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust         multiply_strings.rs
build_rust_ovf         multiply_strings.rs
build_rust_checked multiply_strings.rs
build_c            multiply_strings.c
build_kara         multiply_strings.kara
build_kara_seq     multiply_strings.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="742591719"
mismatch=""
for pair in \
    'kara:./target/multiply_strings_kara' \
    'kara_seq:./target/multiply_strings_kara_seq' \
    'rust:./target/multiply_strings' \
    'rust_ovf:./target/multiply_strings_ovf' \
    'rust_chk:./target/multiply_strings_rschk' \
    'c:./target/multiply_strings_c' \
    'go:./target/multiply_strings_go_seq'; do
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
    py_out=$(python3 multiply_strings.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=43 slug=multiply-strings group=1-100 \
    title="Multiply Strings" \
    workload="TOTAL=300K product-strings (38-digit operand × decimal(k)) concatenated + byte-checksum" \
    sink="$expected"

echo "=== runtime — seq lane (single-threaded string build) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach multiply_strings --lane seq --mode codegen \
    --name 'kara multiply_strings (seq, KARAC_AUTO_PAR=0)' --cmd './target/multiply_strings_kara_seq'
rt_cmd --lang rust --approach multiply_strings --lane seq --mode native \
    --name 'rust multiply_strings' --cmd './target/multiply_strings'
rt_cmd --lang rust_ovf --approach multiply_strings --lane seq --mode native \
    --name 'rust multiply_strings (overflow-checks=on, equal-safety)' --cmd './target/multiply_strings_ovf'
rt_cmd --lang rust --approach multiply_strings_rschk --lane seq --mode native \
    --name 'rust multiply_strings (overflow-checks=on, =Kara safety)' --cmd './target/multiply_strings_rschk'
rt_cmd --lang c --approach multiply_strings --lane seq --mode native \
    --name 'c    multiply_strings' --cmd './target/multiply_strings_c'
rt_cmd --lang go --approach multiply_strings --lane seq --mode native \
    --name 'go   multiply_strings' --cmd './target/multiply_strings_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 1 --runs 3
rt_cmd --lang python --approach multiply_strings --lane seq --mode interp \
    --name 'py   multiply_strings' --cmd 'python3 multiply_strings.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach multiply_strings --mode codegen \
    --prepare 'rm -f target/multiply_strings_kara multiply_strings' \
    --name 'karac build multiply_strings.kara' \
    --cmd 'sh -c "karac build multiply_strings.kara >/dev/null && mv multiply_strings target/multiply_strings_kara"'
ce_cmd --lang rust --approach multiply_strings --mode native \
    --prepare 'rm -f target/multiply_strings' \
    --name 'rustc -O multiply_strings.rs' --cmd 'rustc -O multiply_strings.rs -o target/multiply_strings'
ce_cmd --lang c --approach multiply_strings --mode native \
    --prepare 'rm -f target/multiply_strings_c' \
    --name 'clang -O3 multiply_strings.c' --cmd 'clang -O3 multiply_strings.c -o target/multiply_strings_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach multiply_strings --lane seq --mode codegen --path target/multiply_strings_kara_seq
size_put --lang rust --approach multiply_strings --lane seq --mode native  --path target/multiply_strings
size_put --lang c    --approach multiply_strings --lane seq --mode native  --path target/multiply_strings_c
size_put --lang go   --approach multiply_strings --lane seq --mode native  --path target/multiply_strings_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach multiply_strings --lane seq --mode codegen --bytes "$(mem_peak ./target/multiply_strings_kara_seq)"
mem_put --lang rust --approach multiply_strings --lane seq --mode native  --bytes "$(mem_peak ./target/multiply_strings)"
mem_put --lang c    --approach multiply_strings --lane seq --mode native  --bytes "$(mem_peak ./target/multiply_strings_c)"
mem_put --lang go   --approach multiply_strings --lane seq --mode native  --bytes "$(mem_peak ./target/multiply_strings_go_seq)"
mem_put --lang python --approach multiply_strings --lane seq --mode interp --bytes "$(mem_peak python3 multiply_strings.py)"

echo
echo "=== compile memory (cold) ==="
for src in multiply_strings.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in multiply_strings.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in multiply_strings.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
