#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #125.
# See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the ALLOCATING filter-then-compare variant (build a
# normalized Vec[u8], then symmetric-index check), NOT the pure in-place two-
# pointer: the per-pass allocation is a side effect the optimizer won't hoist,
# so the ITERS reduction does real work every iteration (a pure two-pointer is
# loop-invariant over a fixed input and folds to one pass). Each pass is still
# independent, so the outer `sum += pass(input)` reduction is embarrassingly
# parallel — recognized by karac's auto-par-on-reduction pass (karac_par_reduce
# dispatch). Per BENCH.md's two-lane discipline a second kara binary is built
# with KARAC_AUTO_PAR=0 for the apples-to-apples seq comparison; the default
# auto-par binary is the production regime and headlines the par lane.
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup), clang,
# go, karac (with --features llvm for the codegen path).

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
    local out="target/valid_palindrome_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

# Par-lane comparators — hand-tuned parallelism a programmer writes by hand,
# against which Kāra's auto-par (no parallel source at all) is measured.
build_rayon() {
    local out="target/vp_rayon"
    local src="rayon/src/main.rs"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "building rayon variant (cargo) ..." >&2
        ( cd rayon && cargo build --release --quiet )
        cp -f rayon/target/release/vp_rayon "$out"
    fi
}

build_go_par() {
    local out="target/valid_palindrome_go_par"
    local src="go-par/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-par ..." >&2
        ( cd go-par && go build -o "../$out" . )
    fi
}

# C pthreads — the par-lane bare-metal FLOOR (raw OS threads, no runtime). NOT a
# competitor row: it calibrates how much auto-par leaves on the table vs metal.
build_c_par() {
    local out="target/valid_palindrome_c_par"
    local src="valid_palindrome_par.c"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling c-par (pthreads) ..." >&2
        clang -O3 "$src" -o "$out" -lpthread
    fi
}

build_rust     valid_palindrome.rs
build_c        valid_palindrome.c
build_kara     valid_palindrome.kara
build_kara_seq valid_palindrome.kara
build_go_seq
build_rayon
build_go_par
build_c_par

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="3000000"
mismatch=""
for pair in \
    'kara:./target/valid_palindrome_kara' \
    'kara_seq:./target/valid_palindrome_kara_seq' \
    'rust:./target/valid_palindrome' \
    'c:./target/valid_palindrome_c' \
    'go:./target/valid_palindrome_go_seq' \
    'rayon:./target/vp_rayon' \
    'go_par:./target/valid_palindrome_go_par' \
    'c_par:./target/valid_palindrome_c_par'; do
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
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_out=$(python3 valid_palindrome.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=125 slug=valid-palindrome group=101-200 \
    title="Valid Palindrome" workload="BASE*8 alnum/case-fold filter, ITERS=3M reduction" \
    sink="$expected"

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach valid_palindrome --lane seq --mode codegen \
    --name 'kara valid_palindrome (seq, KARAC_AUTO_PAR=0)' --cmd './target/valid_palindrome_kara_seq'
rt_cmd --lang rust --approach valid_palindrome --lane seq --mode native \
    --name 'rust valid_palindrome' --cmd './target/valid_palindrome'
rt_cmd --lang c --approach valid_palindrome --lane seq --mode native \
    --name 'c    valid_palindrome' --cmd './target/valid_palindrome_c'
rt_cmd --lang go --approach valid_palindrome --lane seq --mode native \
    --name 'go   valid_palindrome' --cmd './target/valid_palindrome_go_seq'
rt_end

echo
echo "=== runtime — PAR LANE (multi-core: auto-par vs hand-tuned vs metal floor) ==="
rt_begin --warmup 10 --runs 50
rt_cmd --lang kara --approach valid_palindrome --lane par --mode codegen \
    --name 'kara  valid_palindrome (auto-par, NO parallel code)' --cmd './target/valid_palindrome_kara'
rt_cmd --lang c --approach valid_palindrome --lane par --mode native \
    --name 'c     valid_palindrome (pthreads — metal floor)' --cmd './target/valid_palindrome_c_par'
rt_cmd --lang rust --approach valid_palindrome --lane par --mode native \
    --name 'rust  valid_palindrome (rayon par_iter)' --cmd './target/vp_rayon'
rt_cmd --lang go --approach valid_palindrome --lane par --mode native \
    --name 'go    valid_palindrome (goroutines + WaitGroup)' --cmd './target/valid_palindrome_go_par'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 1 --runs 3
rt_cmd --lang python --approach valid_palindrome --lane seq --mode interp \
    --name 'py   valid_palindrome' --cmd 'python3 valid_palindrome.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach valid_palindrome --mode codegen \
    --prepare 'rm -f target/valid_palindrome_kara valid_palindrome' \
    --name 'karac build valid_palindrome.kara' \
    --cmd 'sh -c "karac build valid_palindrome.kara >/dev/null && mv valid_palindrome target/valid_palindrome_kara"'
ce_cmd --lang rust --approach valid_palindrome --mode native \
    --prepare 'rm -f target/valid_palindrome' \
    --name 'rustc -O valid_palindrome.rs' --cmd 'rustc -O valid_palindrome.rs -o target/valid_palindrome'
ce_cmd --lang c --approach valid_palindrome --mode native \
    --prepare 'rm -f target/valid_palindrome_c' \
    --name 'clang -O3 valid_palindrome.c' --cmd 'clang -O3 valid_palindrome.c -o target/valid_palindrome_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach valid_palindrome --lane seq --mode codegen --path target/valid_palindrome_kara_seq
size_put --lang kara --approach valid_palindrome --lane par --mode codegen --path target/valid_palindrome_kara
size_put --lang rust --approach valid_palindrome --lane seq --mode native  --path target/valid_palindrome
size_put --lang c    --approach valid_palindrome --lane seq --mode native  --path target/valid_palindrome_c
size_put --lang go   --approach valid_palindrome --lane seq --mode native  --path target/valid_palindrome_go_seq
size_put --lang rust --approach valid_palindrome --lane par --mode native  --path target/vp_rayon
size_put --lang go   --approach valid_palindrome --lane par --mode native  --path target/valid_palindrome_go_par
size_put --lang c    --approach valid_palindrome --lane par --mode native  --path target/valid_palindrome_c_par

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach valid_palindrome --lane seq --mode codegen --bytes "$(mem_peak ./target/valid_palindrome_kara_seq)"
mem_put --lang kara --approach valid_palindrome --lane par --mode codegen --bytes "$(mem_peak ./target/valid_palindrome_kara)"
mem_put --lang rust --approach valid_palindrome --lane seq --mode native  --bytes "$(mem_peak ./target/valid_palindrome)"
mem_put --lang c    --approach valid_palindrome --lane seq --mode native  --bytes "$(mem_peak ./target/valid_palindrome_c)"
mem_put --lang go   --approach valid_palindrome --lane seq --mode native  --bytes "$(mem_peak ./target/valid_palindrome_go_seq)"
mem_put --lang rust --approach valid_palindrome --lane par --mode native  --bytes "$(mem_peak ./target/vp_rayon)"
mem_put --lang go   --approach valid_palindrome --lane par --mode native  --bytes "$(mem_peak ./target/valid_palindrome_go_par)"
mem_put --lang c    --approach valid_palindrome --lane par --mode native  --bytes "$(mem_peak ./target/valid_palindrome_c_par)"
mem_put --lang python --approach valid_palindrome --lane seq --mode interp --bytes "$(mem_peak python3 valid_palindrome.py)"

echo
echo "=== compile memory (cold) ==="
for src in valid_palindrome.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in valid_palindrome.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in valid_palindrome.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
