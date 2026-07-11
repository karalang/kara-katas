#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #87.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Two lanes over ONE workload: a batch of K=60000 INDEPENDENT memoized scramble
# decisions (the kata's memoized ★). Each iteration builds a length-12 string and a
# per-iteration coprime-step permutation of it (s2[j] = s1[(j*5 + iter) % 12], so no
# call hoists), runs the O(n^4) top-down memoized scramble, and folds the FILLED MEMO
# STATE into a work-sensitive per-iteration checksum; the K checksums are combined
# through a plain associative SUM (order-independent, so parallel == sequential). This
# is a COMPUTE-BOUND recursion (the memo is the only allocation), so it parallel-scales
# well — the clean auto-par case in contrast to #86's allocation-bound list workload.
# Every mirror uses 1D heap arrays (kara Vec, rust Vec, c malloc, go slice).
#
#   - SEQ lane: the batch run single-threaded — kara (KARAC_AUTO_PAR=0) vs
#     rustc -O / clang -O3 / go build per-core.
#   - PAR lane: the SAME batch, parallel — the default `karac build` AUTO-
#     PARALLELIZES the `for i in 0..K` sum reduction with NO hand-written parallel
#     code, raced against hand-tuned C-pthreads / rayon / goroutines. Same auto-par-
#     vs-hand-tuned framing as kata #1.
#
# EQUAL-SAFETY: karac checks integer overflow by default while `rustc -O` wraps, so
# a `rustc -O -C overflow-checks=on` row is included in the seq lane (kata #69's
# discipline). Python runs a smaller K (pure-Python is slow at full scale) — timed
# separately, NOT cross-checked.
#
# Requires: hyperfine, rustc, cargo (rayon), clang, go, karac (with --features llvm).

set -euo pipefail
cd "$(dirname "$0")"

STEM=scramble_string

require() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "$1 not found — install with: $2" >&2
        exit 1
    fi
}

require hyperfine "brew install hyperfine"
require rustc     "rustup (https://rustup.rs) or 'brew install rustup-init'"
require cargo     "rustup (https://rustup.rs)  — needed for the rayon par-lane variant"
require clang     "xcode-select --install (macOS) or your distro's clang package"
require go        "brew install go  or your distro's golang package"
require karac     "cargo install --path . --features llvm  (from kara checkout)"

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
print_mem() {
    local label="$1" bytes="$2"
    local mib
    mib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1048576}')
    printf '  %-30s %12s bytes (%6s MiB)\n' "$label" "$bytes" "$mib"
}

mkdir -p target

build_rust() {
    local out="target/${STEM}"
    if [ ! -x "$out" ] || [ "${STEM}.rs" -nt "$out" ]; then
        echo "compiling ${STEM}.rs ..." >&2
        rustc -O "${STEM}.rs" -o "$out"
    fi
}
build_rust_ovf() {
    local out="target/${STEM}_ovf"
    if [ ! -x "$out" ] || [ "${STEM}.rs" -nt "$out" ]; then
        echo "compiling ${STEM}.rs (overflow-checks=on) ..." >&2
        rustc -O -C overflow-checks=on "${STEM}.rs" -o "$out"
    fi
}
build_c() {
    local out="target/${STEM}_c"
    if [ ! -x "$out" ] || [ "${STEM}.c" -nt "$out" ]; then
        echo "compiling ${STEM}.c ..." >&2
        clang -O3 "${STEM}.c" -o "$out"
    fi
}
build_c_par() {
    local out="target/${STEM}_c_par"
    if [ ! -x "$out" ] || [ "${STEM}_par.c" -nt "$out" ]; then
        echo "compiling ${STEM}_par.c (pthreads) ..." >&2
        clang -O3 "${STEM}_par.c" -o "$out" -lpthread
    fi
}
build_kara() {          # default build → auto-par (PAR lane)
    local out="target/${STEM}_kara"
    if [ ! -x "$out" ] || [ "${STEM}.kara" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling ${STEM}.kara (default, auto-par) ..." >&2
        karac build "${STEM}.kara" >/dev/null
        mv "${STEM}" "$out"
    fi
}
build_kara_seq() {      # KARAC_AUTO_PAR=0 → single-threaded twin (SEQ lane)
    local out="target/${STEM}_kara_seq"
    if [ ! -x "$out" ] || [ "${STEM}.kara" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling ${STEM}.kara (KARAC_AUTO_PAR=0, seq) ..." >&2
        KARAC_AUTO_PAR=0 karac build "${STEM}.kara" >/dev/null
        mv "${STEM}" "$out"
    fi
}
build_go_seq() {
    local out="target/${STEM}_go_seq"
    if [ ! -x "$out" ] || [ "go-seq/main.go" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}
build_go_par() {
    local out="target/${STEM}_go_par"
    if [ ! -x "$out" ] || [ "go-par/main.go" -nt "$out" ]; then
        echo "compiling go-par ..." >&2
        ( cd go-par && go build -o "../$out" . )
    fi
}
build_rayon() {
    local out="target/${STEM}_rayon"
    if [ ! -x "$out" ] || [ "rayon/src/main.rs" -nt "$out" ]; then
        echo "building rayon variant (cargo) ..." >&2
        ( cd rayon && cargo build --release --quiet )
        cp -f rayon/target/release/${STEM}_rayon "$out"
    fi
}

build_rust
build_rust_ovf
build_c
build_c_par
build_kara
build_kara_seq
build_go_seq
build_go_par
build_rayon

# Sink agreement — every mirror in BOTH lanes must be byte-identical before
# timing (the associative sum is order-independent, so par == seq). Python runs a
# different (1/10) K and is intentionally excluded.
expected="27504985190000"
mismatch=""
for pair in \
    "kara_seq:./target/${STEM}_kara_seq" \
    "kara_par:./target/${STEM}_kara" \
    "rust:./target/${STEM}" \
    "rust_ovf:./target/${STEM}_ovf" \
    "c:./target/${STEM}_c" \
    "c_par:./target/${STEM}_c_par" \
    "go:./target/${STEM}_go_seq" \
    "go_par:./target/${STEM}_go_par" \
    "rayon:./target/${STEM}_rayon"; do
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
echo "sink (all seq+par mirrors): $expected"
echo

bench_begin id=87 slug=scramble_string group=1-100 \
    title="Scramble String" \
    workload="K=60000 independent length-12 memoized scramble decisions (O(n^4) recursion), associative-sum reduction of a work-sensitive memo checksum (auto-par vs hand-tuned), compute-bound / sink" \
    sink="$expected"

echo "=== runtime — SEQ lane (single-threaded) ==="
rt_begin --warmup 3 --runs 20
rt_cmd --lang kara --approach scramble_string --lane seq --mode codegen \
    --name "kara ${STEM} (KARAC_AUTO_PAR=0)" --cmd "./target/${STEM}_kara_seq"
rt_cmd --lang rust --approach scramble_string --lane seq --mode native \
    --name "rust ${STEM}" --cmd "./target/${STEM}"
rt_cmd --lang rust --approach scramble_string_ovf --lane seq --mode native \
    --name "rust ${STEM} (overflow-checks=on)" --cmd "./target/${STEM}_ovf"
rt_cmd --lang c --approach scramble_string --lane seq --mode native \
    --name "c    ${STEM}" --cmd "./target/${STEM}_c"
rt_cmd --lang go --approach scramble_string --lane seq --mode native \
    --name "go   ${STEM}" --cmd "./target/${STEM}_go_seq"
rt_end

echo
echo "=== runtime — PAR LANE: auto-par vs hand-tuned vs metal floor ==="
# kara's default build auto-parallelizes the `for i in 0..K` sum reduction with NO
# parallel source. C-pthreads is the bare-metal floor; rayon and goroutines are the
# hand-tuned comparators. NOT comparable to the single-thread seq rows above.
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach scramble_string --lane par --mode codegen \
    --name "kara ${STEM} (auto-par, NO parallel code)" --cmd "./target/${STEM}_kara"
rt_cmd --lang c --approach scramble_string --lane par --mode native \
    --name "c    ${STEM} (pthreads — metal floor)" --cmd "./target/${STEM}_c_par"
rt_cmd --lang rust --approach scramble_string --lane par --mode native \
    --name "rust ${STEM} (rayon par_iter)" --cmd "./target/${STEM}_rayon"
rt_cmd --lang go --approach scramble_string --lane par --mode native \
    --name "go   ${STEM} (goroutines + WaitGroup)" --cmd "./target/${STEM}_go_par"
rt_end

echo
echo "=== runtime — Python (1/10 K, timed separately, not cross-checked) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach scramble_string --lane seq --mode interp \
    --name "py   ${STEM} (K=4000)" --cmd "python3 ${STEM}.py"
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach scramble_string --mode codegen \
    --prepare "rm -f target/${STEM}_kara ${STEM}" \
    --name "karac build ${STEM}.kara" \
    --cmd "sh -c \"karac build ${STEM}.kara >/dev/null && mv ${STEM} target/${STEM}_kara\""
ce_cmd --lang rust --approach scramble_string --mode native \
    --prepare "rm -f target/${STEM}" \
    --name "rustc -O ${STEM}.rs" --cmd "rustc -O ${STEM}.rs -o target/${STEM}"
ce_cmd --lang c --approach scramble_string --mode native \
    --prepare "rm -f target/${STEM}_c" \
    --name "clang -O3 ${STEM}.c" --cmd "clang -O3 ${STEM}.c -o target/${STEM}_c"
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach scramble_string --lane seq --mode codegen --path "target/${STEM}_kara_seq"
size_put --lang kara --approach scramble_string --lane par --mode codegen --path "target/${STEM}_kara"
size_put --lang rust --approach scramble_string --lane seq --mode native  --path "target/${STEM}"
size_put --lang c    --approach scramble_string --lane seq --mode native  --path "target/${STEM}_c"
size_put --lang c    --approach scramble_string --lane par --mode native  --path "target/${STEM}_c_par"
size_put --lang go   --approach scramble_string --lane seq --mode native  --path "target/${STEM}_go_seq"

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach scramble_string --lane seq --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara_seq)"
mem_put --lang kara --approach scramble_string --lane par --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara)"
mem_put --lang rust --approach scramble_string --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM})"
mem_put --lang c    --approach scramble_string --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_c)"
mem_put --lang go   --approach scramble_string --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_go_seq)"

echo
echo "=== compile memory (cold) ==="
rm -f "target/${STEM}_kara" "${STEM}"
bytes=$(mem_peak karac build "${STEM}.kara")
mv "${STEM}" "target/${STEM}_kara" 2>/dev/null || true
cmem_put --lang kara --approach scramble_string --mode codegen --bytes "$bytes"
rm -f "target/${STEM}"
cmem_put --lang rust --approach scramble_string --mode native --bytes "$(mem_peak rustc -O "${STEM}.rs" -o "target/${STEM}")"
rm -f "target/${STEM}_c"
cmem_put --lang c --approach scramble_string --mode native --bytes "$(mem_peak clang -O3 "${STEM}.c" -o "target/${STEM}_c")"

echo
bench_emit
