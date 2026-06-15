#!/usr/bin/env bash
# Wall-clock comparison across implementations of the bespoke utf8-codepoints
# kata. See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the ★ byte-indexed manual UTF-8 decoder run as a
# SEQUENTIAL scan-and-accumulate: build a multilingual base string (all four
# UTF-8 byte-lengths) once, repeat it to a ~330 KB buffer, then decode every
# codepoint ITERS=400 times, folding each Unicode scalar into a modular running
# sink. The decode loop carries a data dependency on `sink`, so it does not
# auto-parallelize — a single-lane (seq) bench by construction (the kara auto-par
# and KARAC_AUTO_PAR=0 binaries are equivalent here; the seq binary is benched).
#
# Classification is deliberately NOT in the sink: the Unicode letter/number
# tables don't agree byte-for-byte across C/Go, so the sink is pure decode
# arithmetic (== Python `ord`-sum), keeping all six binaries' stdout identical.
#
# `rustc -O` const-folds the whole deterministic computation away (it can prove
# the answer at compile time); `std::hint::black_box` around the buffer + outputs
# makes the input opaque so Rust does the same work C/Go/kara already do — a
# leveling, not a handicap.
#
# Requires: hyperfine, rustc, clang, go, karac (--features llvm).

set -euo pipefail
cd "$(dirname "$0")"

require() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "$1 not found — install with: $2" >&2
        exit 1
    fi
}

require hyperfine "brew install hyperfine"
require rustc     "rustup (https://rustup.rs)"
require clang     "xcode-select --install"
require go        "brew install go"
require karac     "cargo install --path . --features llvm"

if [ "${BENCH_JSON:-1}" = "1" ]; then
    require jq      "brew install jq"
    require python3 "python3 ships with macOS"
fi
ROOT="$(cd ../../.. && pwd)"
. "$ROOT/scripts/bench-lib.sh"

mem_peak() {
    { /usr/bin/time -l "$@" >/dev/null; } 2>&1 \
        | awk '/peak memory footprint/ {print $1}'
}

mkdir -p target

build_rust() {
    local out="target/utf8_codepoints"
    if [ ! -x "$out" ] || [ utf8_codepoints.rs -nt "$out" ]; then
        echo "compiling utf8_codepoints.rs ..." >&2
        rustc -O utf8_codepoints.rs -o "$out"
    fi
}
build_rust_checked() {
    local out="target/utf8_codepoints_rschk"
    if [ ! -x "$out" ] || [ utf8_codepoints.rs -nt "$out" ]; then
        echo "compiling utf8_codepoints.rs (overflow-checks=on) ..." >&2
        rustc -O -C overflow-checks=on utf8_codepoints.rs -o "$out"
    fi
}
build_c() {
    local out="target/utf8_codepoints_c"
    if [ ! -x "$out" ] || [ utf8_codepoints.c -nt "$out" ]; then
        echo "compiling utf8_codepoints.c ..." >&2
        clang -O3 utf8_codepoints.c -o "$out"
    fi
}
build_kara() {
    local out="target/utf8_codepoints_kara"
    if [ ! -x "$out" ] || [ utf8_codepoints.kara -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling utf8_codepoints.kara (auto-par default) ..." >&2
        karac build utf8_codepoints.kara >/dev/null
        mv utf8_codepoints "$out"
    fi
}
build_kara_seq() {
    local out="target/utf8_codepoints_kara_seq"
    if [ ! -x "$out" ] || [ utf8_codepoints.kara -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling utf8_codepoints.kara (KARAC_AUTO_PAR=0, seq lane) ..." >&2
        KARAC_AUTO_PAR=0 karac build utf8_codepoints.kara >/dev/null
        mv utf8_codepoints "$out"
    fi
}
build_go_seq() {
    local out="target/utf8_codepoints_go_seq"
    if [ ! -x "$out" ] || [ go-seq/main.go -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust
build_rust_checked
build_c
build_kara
build_kara_seq
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="72374800 744704645"
mismatch=""
for pair in \
    'kara:./target/utf8_codepoints_kara' \
    'kara_seq:./target/utf8_codepoints_kara_seq' \
    'rust:./target/utf8_codepoints' \
    'rust_chk:./target/utf8_codepoints_rschk' \
    'c:./target/utf8_codepoints_c' \
    'go:./target/utf8_codepoints_go_seq'; do
    name="${pair%%:*}"; cmd="${pair#*:}"
    out=$("$cmd")
    if [ "$out" != "$expected" ]; then mismatch="$mismatch ${name}=[${out}]"; fi
done
if [ -n "$mismatch" ]; then
    echo "sink mismatch (expected=[$expected]):$mismatch" >&2
    exit 1
fi
echo "sink (kara/kara_seq/rust/c/go): $expected"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_out=$(python3 utf8_codepoints.py)
    [ "$py_out" = "$expected" ] || { echo "python sink mismatch: py=[$py_out]" >&2; exit 1; }
    echo "python: matches"
fi
echo

bench_begin id=utf8-codepoints slug=utf8-codepoints group=bespoke \
    title="UTF-8 Codepoints" \
    workload="~330 KB multilingual buffer, decode every codepoint ITERS=400× + modular scalar-sum sink" \
    sink="$expected"

echo "=== runtime — seq lane (single-threaded decode scan) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach utf8_codepoints --lane seq --mode codegen \
    --name 'kara utf8_codepoints (seq, KARAC_AUTO_PAR=0)' --cmd './target/utf8_codepoints_kara_seq'
rt_cmd --lang rust --approach utf8_codepoints --lane seq --mode native \
    --name 'rust utf8_codepoints' --cmd './target/utf8_codepoints'
rt_cmd --lang rust --approach utf8_codepoints_rschk --lane seq --mode native \
    --name 'rust utf8_codepoints (overflow-checks=on, =Kara safety)' --cmd './target/utf8_codepoints_rschk'
rt_cmd --lang c --approach utf8_codepoints --lane seq --mode native \
    --name 'c    utf8_codepoints' --cmd './target/utf8_codepoints_c'
rt_cmd --lang go --approach utf8_codepoints --lane seq --mode native \
    --name 'go   utf8_codepoints' --cmd './target/utf8_codepoints_go_seq'
rt_end

echo
echo "=== runtime — long workload (py) ==="
rt_begin --warmup 1 --runs 3
rt_cmd --lang python --approach utf8_codepoints --lane seq --mode interp \
    --name 'py   utf8_codepoints' --cmd 'python3 utf8_codepoints.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach utf8_codepoints --mode codegen \
    --prepare 'rm -f target/utf8_codepoints_kara utf8_codepoints' \
    --name 'karac build utf8_codepoints.kara' \
    --cmd 'sh -c "karac build utf8_codepoints.kara >/dev/null && mv utf8_codepoints target/utf8_codepoints_kara"'
ce_cmd --lang rust --approach utf8_codepoints --mode native \
    --prepare 'rm -f target/utf8_codepoints' \
    --name 'rustc -O utf8_codepoints.rs' --cmd 'rustc -O utf8_codepoints.rs -o target/utf8_codepoints'
ce_cmd --lang c --approach utf8_codepoints --mode native \
    --prepare 'rm -f target/utf8_codepoints_c' \
    --name 'clang -O3 utf8_codepoints.c' --cmd 'clang -O3 utf8_codepoints.c -o target/utf8_codepoints_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach utf8_codepoints --lane seq --mode codegen --path target/utf8_codepoints_kara_seq
size_put --lang rust --approach utf8_codepoints --lane seq --mode native  --path target/utf8_codepoints
size_put --lang c    --approach utf8_codepoints --lane seq --mode native  --path target/utf8_codepoints_c
size_put --lang go   --approach utf8_codepoints --lane seq --mode native  --path target/utf8_codepoints_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach utf8_codepoints --lane seq --mode codegen --bytes "$(mem_peak ./target/utf8_codepoints_kara_seq)"
mem_put --lang rust --approach utf8_codepoints --lane seq --mode native  --bytes "$(mem_peak ./target/utf8_codepoints)"
mem_put --lang c    --approach utf8_codepoints --lane seq --mode native  --bytes "$(mem_peak ./target/utf8_codepoints_c)"
mem_put --lang go   --approach utf8_codepoints --lane seq --mode native  --bytes "$(mem_peak ./target/utf8_codepoints_go_seq)"
mem_put --lang python --approach utf8_codepoints --lane seq --mode interp --bytes "$(mem_peak python3 utf8_codepoints.py)"

echo
echo "=== compile memory (cold) ==="
rm -f target/utf8_codepoints_kara utf8_codepoints
bytes=$(mem_peak karac build utf8_codepoints.kara); mv utf8_codepoints target/utf8_codepoints_kara 2>/dev/null || true
cmem_put --lang kara --approach utf8_codepoints --mode codegen --bytes "$bytes"
rm -f target/utf8_codepoints
cmem_put --lang rust --approach utf8_codepoints --mode native --bytes "$(mem_peak rustc -O utf8_codepoints.rs -o target/utf8_codepoints)"
rm -f target/utf8_codepoints_c
cmem_put --lang c --approach utf8_codepoints --mode native --bytes "$(mem_peak clang -O3 utf8_codepoints.c -o target/utf8_codepoints_c)"

echo
bench_emit
