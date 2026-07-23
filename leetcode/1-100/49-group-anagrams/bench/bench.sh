#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #49 (Group
# Anagrams). See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata: the workload groups N=20_000 fixed words by their sorted-key
# (`sorted()` per word + one Map lookup/insert), K=40 outer iterations. The
# per-word work is a sort + hash — no cross-word parallel structure the auto-
# par cost model engages, so the kara binary is built KARAC_AUTO_PAR=0 and the
# seq-codegen row is directly comparable to rustc -O / clang -O3 / go build on
# a per-core codegen-quality basis (BENCH.md two-lane protocol).
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup), clang, go,
# karac (with --features llvm for the codegen path).

set -euo pipefail
cd "$(dirname "$0")"

STEM=group_anagrams

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
require karac     "cargo install --path . --features llvm  (from kara checkout)"

# Structured-JSON emission (writes bench/results.json). Set BENCH_JSON=0 to
# skip — the human-readable console output below is unaffected either way.
if [ "${BENCH_JSON:-1}" = "1" ]; then
    require jq      "brew install jq"
    require python3 "python3 ships with macOS; or 'brew install python'"
fi
ROOT="$(cd ../../../.. && pwd)"
. "$ROOT/scripts/bench-lib.sh"

# /usr/bin/time -l (macOS BSD time) prints a "peak memory footprint" line on
# stderr; capture it through a brace-group redirect and parse the bytes column.

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

# Seq twin — KARAC_AUTO_PAR=0 short-circuits codegen's auto-par gate back to
# plain sequential compile_block, the row directly comparable to the native
# single-file compilers.
build_kara() {
    local src="$1"
    local stem="$(basename "$src" .kara)"
    local out="target/${stem}_kara"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling $src (seq twin, KARAC_AUTO_PAR=0) ..." >&2
        KARAC_AUTO_PAR=0 karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

build_go_seq() {
    local out="target/${STEM}_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust "${STEM}.rs"
build_c    "${STEM}.c"
build_kara "${STEM}.kara"
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
# N=20_000 words in 26 anagram classes, K=40 → sink = 40 * 26 = 1040. Python
# skipped from the sink check by default (it's timed at the same K but runs
# slower); set KARA_BENCH_INCLUDE_PY=1 to opt it in.
expected="1040"
mismatch=""
for pair in \
    "kara:./target/${STEM}_kara" \
    "rust:./target/${STEM}" \
    "c:./target/${STEM}_c" \
    "go:./target/${STEM}_go_seq"; do
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
echo "sink (kara/rust/c/go): $expected"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_out=$(python3 "${STEM}.py")
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=49 slug=group-anagrams group=1-100 \
    title="Group Anagrams" \
    workload="sorted-key grouping: N=20_000 words (L=8), 26 classes, K=40 outer iters" \
    sink="$expected"

echo "=== runtime — compiled (single-threaded) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach group_anagrams --lane seq --mode codegen \
    --name 'kara group_anagrams (seq, KARAC_AUTO_PAR=0)' --cmd "./target/${STEM}_kara"
rt_cmd --lang rust --approach group_anagrams --lane seq --mode native \
    --name 'rust group_anagrams' --cmd "./target/${STEM}"
rt_cmd --lang c --approach group_anagrams --lane seq --mode native \
    --name 'c    group_anagrams' --cmd "./target/${STEM}_c"
rt_cmd --lang go --approach group_anagrams --lane seq --mode native \
    --name 'go   group_anagrams' --cmd "./target/${STEM}_go_seq"
rt_end

echo
echo "=== runtime — Python (same K=40) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach group_anagrams --lane seq --mode interp \
    --name 'py   group_anagrams' --cmd "python3 ${STEM}.py"
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach group_anagrams --mode codegen \
    --prepare "rm -f target/${STEM}_kara ${STEM}" \
    --name "karac build ${STEM}.kara" \
    --cmd "sh -c \"KARAC_AUTO_PAR=0 karac build ${STEM}.kara >/dev/null && mv ${STEM} target/${STEM}_kara\""
ce_cmd --lang rust --approach group_anagrams --mode native \
    --prepare "rm -f target/${STEM}" \
    --name "rustc -O ${STEM}.rs" --cmd "rustc -O ${STEM}.rs -o target/${STEM}"
ce_cmd --lang c --approach group_anagrams --mode native \
    --prepare "rm -f target/${STEM}_c" \
    --name "clang -O3 ${STEM}.c" --cmd "clang -O3 ${STEM}.c -o target/${STEM}_c"
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach group_anagrams --lane seq --mode codegen --path "target/${STEM}_kara"
size_put --lang rust --approach group_anagrams --lane seq --mode native  --path "target/${STEM}"
size_put --lang c    --approach group_anagrams --lane seq --mode native  --path "target/${STEM}_c"
size_put --lang go   --approach group_anagrams --lane seq --mode native  --path "target/${STEM}_go_seq"

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach group_anagrams --lane seq --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara)"
mem_put --lang rust --approach group_anagrams --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM})"
mem_put --lang c    --approach group_anagrams --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_c)"
mem_put --lang go   --approach group_anagrams --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_go_seq)"
mem_put --lang python --approach group_anagrams --lane seq --mode interp --bytes "$(mem_peak python3 ${STEM}.py)"

echo
echo "=== compile memory (cold) ==="
for src in "${STEM}.kara"; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak env KARAC_AUTO_PAR=0 karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in "${STEM}.rs"; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in "${STEM}.c"; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
