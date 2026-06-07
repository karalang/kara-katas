#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #28.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata: strStr is a read-only scan with a loop-carried needle
# cursor — no auto-par surface. Two approaches share one adversarial input
# (haystack = N-1 'a' + 'b', needle = M-1 'a' + 'b', match only at the end):
# brute_force runs it in O(N·M), kmp in O(N+M). The gap between them on this
# input is the reason both are carried.
#
# python is benched on kmp only — pure-Python brute_force at O(N·M) = 320M
# byte compares is minutes per run, not a useful data point. kara interp
# lanes are omitted (tree-walk over the adversarial scan is impractical;
# interp parity is covered by the kata-root `diff` test on the String form).
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup), clang,
# go, karac.

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
require karac     "cargo install --path . --features llvm  (from karac-rust checkout)"

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
        echo "compiling $src ..." >&2
        karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

# One go module (bench/go-seq/) with two main packages (./brute_force, ./kmp).
build_go_seq() {
    local pkg="$1"
    local out="target/${pkg}_go_seq"
    local src="go-seq/${pkg}/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq/${pkg} ..." >&2
        ( cd go-seq && go build -o "../$out" "./${pkg}" )
    fi
}

build_rust brute_force.rs
build_rust kmp.rs
build_c    brute_force.c
build_c    kmp.c
build_kara brute_force.kara
build_kara kmp.kara
build_kara kmp_unchecked.kara
build_go_seq brute_force
build_go_seq kmp

# Sink agreement — every compiled mirror's stdout must be byte-identical
# before timing. python excluded by default (brute_force py is minutes);
# set KARA_BENCH_INCLUDE_PY=1 to check the kmp py sink.
expected="19999840"
mismatch=""
for pair in \
    'bf_kara:./target/brute_force_kara' \
    'bf_rust:./target/brute_force' \
    'bf_c:./target/brute_force_c' \
    'bf_go:./target/brute_force_go_seq' \
    'kmp_kara:./target/kmp_kara' \
    'kmpu_kara:./target/kmp_unchecked_kara' \
    'kmp_rust:./target/kmp' \
    'kmp_c:./target/kmp_c' \
    'kmp_go:./target/kmp_go_seq'; do
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
echo "sink (all eight: kara/rust/c/go × brute_force/kmp): $expected"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_kmp=$(python3 kmp.py)
    if [ "$py_kmp" != "$expected" ]; then
        echo "python kmp sink mismatch: py_kmp=$py_kmp" >&2
        exit 1
    fi
    echo "python kmp: matches"
fi
echo

bench_begin id=28 slug=find-the-index-of-the-first-occurrence-in-a-string group=1-100 \
    title="Find the Index of the First Occurrence in a String" \
    workload="adversarial N=2M M=16, K=10; brute O(N·M) vs kmp O(N+M)" \
    sink="$expected"

echo "=== runtime — compiled (both approaches) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach brute_force --lane seq --mode codegen \
    --name 'kara brute_force (codegen)' --cmd './target/brute_force_kara'
rt_cmd --lang rust --approach brute_force --lane seq --mode native \
    --name 'rust brute_force' --cmd './target/brute_force'
rt_cmd --lang c --approach brute_force --lane seq --mode native \
    --name 'c    brute_force' --cmd './target/brute_force_c'
rt_cmd --lang go --approach brute_force --lane seq --mode native \
    --name 'go   brute_force' --cmd './target/brute_force_go_seq'
rt_cmd --lang kara --approach kmp --lane seq --mode codegen \
    --name 'kara kmp (codegen)' --cmd './target/kmp_kara'
rt_cmd --lang kara --approach kmp_unchecked --lane seq --mode codegen \
    --name 'kara kmp_unchecked (codegen)' --cmd './target/kmp_unchecked_kara'
rt_cmd --lang rust --approach kmp --lane seq --mode native \
    --name 'rust kmp' --cmd './target/kmp'
rt_cmd --lang c --approach kmp --lane seq --mode native \
    --name 'c    kmp' --cmd './target/kmp_c'
rt_cmd --lang go --approach kmp --lane seq --mode native \
    --name 'go   kmp' --cmd './target/kmp_go_seq'
rt_end

echo
echo "=== runtime — long workload (py kmp) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach kmp --lane seq --mode interp \
    --name 'py   kmp' --cmd 'python3 kmp.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach brute_force --mode codegen \
    --prepare 'rm -f target/brute_force_kara brute_force' \
    --name 'karac build brute_force.kara' \
    --cmd 'sh -c "karac build brute_force.kara >/dev/null && mv brute_force target/brute_force_kara"'
ce_cmd --lang kara --approach kmp --mode codegen \
    --prepare 'rm -f target/kmp_kara kmp' \
    --name 'karac build kmp.kara' \
    --cmd 'sh -c "karac build kmp.kara >/dev/null && mv kmp target/kmp_kara"'
ce_cmd --lang kara --approach kmp_unchecked --mode codegen \
    --prepare 'rm -f target/kmp_unchecked_kara kmp_unchecked' \
    --name 'karac build kmp_unchecked.kara' \
    --cmd 'sh -c "karac build kmp_unchecked.kara >/dev/null && mv kmp_unchecked target/kmp_unchecked_kara"'
ce_cmd --lang rust --approach brute_force --mode native \
    --prepare 'rm -f target/brute_force' \
    --name 'rustc -O brute_force.rs' --cmd 'rustc -O brute_force.rs -o target/brute_force'
ce_cmd --lang rust --approach kmp --mode native \
    --prepare 'rm -f target/kmp' \
    --name 'rustc -O kmp.rs' --cmd 'rustc -O kmp.rs -o target/kmp'
ce_cmd --lang c --approach brute_force --mode native \
    --prepare 'rm -f target/brute_force_c' \
    --name 'clang -O3 brute_force.c' --cmd 'clang -O3 brute_force.c -o target/brute_force_c'
ce_cmd --lang c --approach kmp --mode native \
    --prepare 'rm -f target/kmp_c' \
    --name 'clang -O3 kmp.c' --cmd 'clang -O3 kmp.c -o target/kmp_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach brute_force --lane seq --mode codegen --path target/brute_force_kara
size_put --lang kara --approach kmp         --lane seq --mode codegen --path target/kmp_kara
size_put --lang kara --approach kmp_unchecked --lane seq --mode codegen --path target/kmp_unchecked_kara
size_put --lang rust --approach brute_force --lane seq --mode native  --path target/brute_force
size_put --lang rust --approach kmp         --lane seq --mode native  --path target/kmp
size_put --lang c    --approach brute_force --lane seq --mode native  --path target/brute_force_c
size_put --lang c    --approach kmp         --lane seq --mode native  --path target/kmp_c
size_put --lang go   --approach brute_force --lane seq --mode native  --path target/brute_force_go_seq
size_put --lang go   --approach kmp         --lane seq --mode native  --path target/kmp_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach brute_force --lane seq --mode codegen --bytes "$(mem_peak ./target/brute_force_kara)"
mem_put --lang kara --approach kmp         --lane seq --mode codegen --bytes "$(mem_peak ./target/kmp_kara)"
mem_put --lang kara --approach kmp_unchecked --lane seq --mode codegen --bytes "$(mem_peak ./target/kmp_unchecked_kara)"
mem_put --lang rust --approach brute_force --lane seq --mode native  --bytes "$(mem_peak ./target/brute_force)"
mem_put --lang rust --approach kmp         --lane seq --mode native  --bytes "$(mem_peak ./target/kmp)"
mem_put --lang c    --approach brute_force --lane seq --mode native  --bytes "$(mem_peak ./target/brute_force_c)"
mem_put --lang c    --approach kmp         --lane seq --mode native  --bytes "$(mem_peak ./target/kmp_c)"
mem_put --lang go   --approach brute_force --lane seq --mode native  --bytes "$(mem_peak ./target/brute_force_go_seq)"
mem_put --lang go   --approach kmp         --lane seq --mode native  --bytes "$(mem_peak ./target/kmp_go_seq)"
mem_put --lang python --approach kmp       --lane seq --mode interp  --bytes "$(mem_peak python3 kmp.py)"

echo
echo "=== compile memory (cold) ==="
for src in brute_force.kara kmp.kara kmp_unchecked.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in brute_force.rs kmp.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in brute_force.c kmp.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
