#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #171.
# See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the Horner-fold bijective base-26 PARSE (the ★ style):
# `n = n*26 + (b - 'A' + 1)` over a title's bytes. It is compute-bound (no
# per-parse allocation) — a clean measure of tight-loop codegen. A LEN=50000
# distinct-title corpus (built once via to_title) is parsed round-robin K_ITERS
# times; the large distinct set keeps an optimizing comparator from tabulating
# the parse results, and `corpus[k % LEN]` varies the input so each parse is
# genuinely recomputed. The `sum += to_number(...)` reduction over k is
# embarrassingly parallel — recognized by karac's auto-par-on-reduction pass
# (karac_par_reduce dispatch). Per BENCH.md's two-lane discipline a second kara
# binary is built with KARAC_AUTO_PAR=0 for the apples-to-apples seq comparison;
# the default auto-par binary headlines the par lane.
#
# No Python lane: the native parse is so cheap that the workload needed to
# measure it (K_ITERS = 10^8) is intractable for CPython at a matched sink.
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
require cargo     "rustup (https://rustup.rs)  — needed for the rayon par-lane variant"
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
# variant traps like Kāra, isolating codegen quality from the safety tax.
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
    local out="target/column_number_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

# Par-lane comparators — hand-tuned parallelism a programmer writes by hand,
# against which Kāra's auto-par (no parallel source at all) is measured.
build_rayon() {
    local out="target/column_number_rayon"
    local src="rayon/src/main.rs"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "building rayon variant (cargo) ..." >&2
        ( cd rayon && cargo build --release --quiet )
        cp -f rayon/target/release/column_number_rayon "$out"
    fi
}

build_go_par() {
    local out="target/column_number_go_par"
    local src="go-par/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-par ..." >&2
        ( cd go-par && go build -o "../$out" . )
    fi
}

# C pthreads — the par-lane bare-metal FLOOR (raw OS threads, no runtime). NOT a
# competitor row: it calibrates how much auto-par leaves on the table vs metal.
build_c_par() {
    local out="target/column_number_c_par"
    local src="column_number_par.c"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling c-par (pthreads) ..." >&2
        clang -O3 "$src" -o "$out" -lpthread
    fi
}

build_rust     column_number.rs
build_rust_ovf     column_number.rs
build_rust_checked column_number.rs
build_c        column_number.c
build_kara     column_number.kara
build_kara_seq column_number.kara
build_go_seq
build_rayon
build_go_par
build_c_par

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="2500050000000"
mismatch=""
for pair in \
    'kara:./target/column_number_kara' \
    'kara_seq:./target/column_number_kara_seq' \
    'rust:./target/column_number' \
    'rust_ovf:./target/column_number_ovf' \
    'rust_chk:./target/column_number_rschk' \
    'c:./target/column_number_c' \
    'go:./target/column_number_go_seq' \
    'rayon:./target/column_number_rayon' \
    'go_par:./target/column_number_go_par' \
    'c_par:./target/column_number_c_par'; do
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
echo "sink (kara/kara_seq/rust/c/go/rayon/go-par/c-par): $expected"
echo

bench_begin id=171 slug=excel-sheet-column-number group=101-200 \
    title="Excel Sheet Column Number" \
    workload="LEN=50000 distinct titles, base-26 parse, K_ITERS=10^8 reduction" \
    sink="$expected"

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach column_number --lane seq --mode codegen \
    --name 'kara column_number (seq, KARAC_AUTO_PAR=0)' --cmd './target/column_number_kara_seq'
rt_cmd --lang rust --approach column_number --lane seq --mode native \
    --name 'rust column_number' --cmd './target/column_number'
rt_cmd --lang rust_ovf --approach column_number --lane seq --mode native \
    --name 'rust column_number (overflow-checks=on, equal-safety)' --cmd './target/column_number_ovf'
rt_cmd --lang rust --approach column_number_rschk --lane seq --mode native \
    --name 'rust column_number (overflow-checks=on, =Kara safety)' --cmd './target/column_number_rschk'
rt_cmd --lang c --approach column_number --lane seq --mode native \
    --name 'c    column_number' --cmd './target/column_number_c'
rt_cmd --lang go --approach column_number --lane seq --mode native \
    --name 'go   column_number' --cmd './target/column_number_go_seq'
rt_end

echo
echo "=== runtime — PAR LANE (multi-core: auto-par vs hand-tuned vs metal floor) ==="
rt_begin --warmup 10 --runs 50
rt_cmd --lang kara --approach column_number --lane par --mode codegen \
    --name 'kara  column_number (auto-par, NO parallel code)' --cmd './target/column_number_kara'
rt_cmd --lang c --approach column_number --lane par --mode native \
    --name 'c     column_number (pthreads — metal floor)' --cmd './target/column_number_c_par'
rt_cmd --lang rust --approach column_number --lane par --mode native \
    --name 'rust  column_number (rayon par_iter)' --cmd './target/column_number_rayon'
rt_cmd --lang go --approach column_number --lane par --mode native \
    --name 'go    column_number (goroutines + WaitGroup)' --cmd './target/column_number_go_par'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach column_number --mode codegen \
    --prepare 'rm -f target/column_number_kara column_number' \
    --name 'karac build column_number.kara' \
    --cmd 'sh -c "karac build column_number.kara >/dev/null && mv column_number target/column_number_kara"'
ce_cmd --lang rust --approach column_number --mode native \
    --prepare 'rm -f target/column_number' \
    --name 'rustc -O column_number.rs' --cmd 'rustc -O column_number.rs -o target/column_number'
ce_cmd --lang c --approach column_number --mode native \
    --prepare 'rm -f target/column_number_c' \
    --name 'clang -O3 column_number.c' --cmd 'clang -O3 column_number.c -o target/column_number_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach column_number --lane seq --mode codegen --path target/column_number_kara_seq
size_put --lang kara --approach column_number --lane par --mode codegen --path target/column_number_kara
size_put --lang rust --approach column_number --lane seq --mode native  --path target/column_number
size_put --lang c    --approach column_number --lane seq --mode native  --path target/column_number_c
size_put --lang go   --approach column_number --lane seq --mode native  --path target/column_number_go_seq
size_put --lang rust --approach column_number --lane par --mode native  --path target/column_number_rayon
size_put --lang go   --approach column_number --lane par --mode native  --path target/column_number_go_par
size_put --lang c    --approach column_number --lane par --mode native  --path target/column_number_c_par

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach column_number --lane seq --mode codegen --bytes "$(mem_peak ./target/column_number_kara_seq)"
mem_put --lang kara --approach column_number --lane par --mode codegen --bytes "$(mem_peak ./target/column_number_kara)"
mem_put --lang rust --approach column_number --lane seq --mode native  --bytes "$(mem_peak ./target/column_number)"
mem_put --lang c    --approach column_number --lane seq --mode native  --bytes "$(mem_peak ./target/column_number_c)"
mem_put --lang go   --approach column_number --lane seq --mode native  --bytes "$(mem_peak ./target/column_number_go_seq)"
mem_put --lang rust --approach column_number --lane par --mode native  --bytes "$(mem_peak ./target/column_number_rayon)"
mem_put --lang go   --approach column_number --lane par --mode native  --bytes "$(mem_peak ./target/column_number_go_par)"
mem_put --lang c    --approach column_number --lane par --mode native  --bytes "$(mem_peak ./target/column_number_c_par)"

echo
echo "=== compile memory (cold) ==="
for src in column_number.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in column_number.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in column_number.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
