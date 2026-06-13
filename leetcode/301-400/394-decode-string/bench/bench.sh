#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #394.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata at the algorithm level — the decode is one sequential pass with
# a nesting stack whose state carries through the scan, so a single decode has no
# parallel lane. BUT the bench's OUTER reduction `sum = sum + pass_len(encoded)`
# over ITERS independent decodes is recognized by karac's auto-par-on-reduction
# pass, which emits a karac_par_reduce dispatch. Per BENCH.md's two-lane
# discipline the auto-par regime would mask the per-core codegen-vs-rustc
# comparison the corpus is built around, so we ship a second kara binary built
# with KARAC_AUTO_PAR=0 (codegen.rs Slice 6 gate — short-circuits auto-par
# dispatch back to plain sequential compile_block). The default binary is still
# built so the auto-par number stays reported as the production regime.
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
    local out="target/decode_string_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

# Par-lane comparators — hand-tuned parallelism a programmer writes by hand,
# against which Kara's auto-par (no parallel source at all) is measured.
build_rayon() {
    local out="target/decode_rayon"
    local src="rayon/src/main.rs"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "building rayon variant (cargo) ..." >&2
        ( cd rayon && cargo build --release --quiet )
        cp -f rayon/target/release/decode_rayon "$out"
    fi
}

build_go_par() {
    local out="target/decode_string_go_par"
    local src="go-par/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-par ..." >&2
        ( cd go-par && go build -o "../$out" . )
    fi
}

build_rust     decode_string.rs
build_c        decode_string.c
build_kara     decode_string.kara
build_kara_seq decode_string.kara
build_go_seq
build_rayon
build_go_par

# Sink agreement — every mirror's stdout must be byte-identical before timing.
# Python skipped from the sink check by default (at ITERS=4000 the py run takes
# ~1.7s and would block bench.sh). Set KARA_BENCH_INCLUDE_PY=1 to opt in.
expected="41600000"
mismatch=""
for pair in \
    'kara:./target/decode_string_kara' \
    'kara_seq:./target/decode_string_kara_seq' \
    'rust:./target/decode_string' \
    'c:./target/decode_string_c' \
    'go:./target/decode_string_go_seq' \
    'rayon:./target/decode_rayon' \
    'go_par:./target/decode_string_go_par'; do
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
echo "sink (kara/kara_seq/rust/c/go/rayon/go-par): $expected"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_out=$(python3 decode_string.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=394 slug=decode-string group=301-400 \
    title="Decode String" workload="ENCODED nest, ITERS=800k decode reduction" \
    sink="$expected"

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
# All four comparators run single-threaded. The kara binary built with
# KARAC_AUTO_PAR=0 short-circuits auto-par dispatch back to plain sequential
# codegen — the row directly comparable to rustc -O / clang -O3 / go build on
# a per-core codegen-quality basis.
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach decode_string --lane seq --mode codegen \
    --name 'kara decode_string (seq, KARAC_AUTO_PAR=0)' --cmd './target/decode_string_kara_seq'
rt_cmd --lang rust --approach decode_string --lane seq --mode native \
    --name 'rust decode_string' --cmd './target/decode_string'
rt_cmd --lang c --approach decode_string --lane seq --mode native \
    --name 'c    decode_string' --cmd './target/decode_string_c'
rt_cmd --lang go --approach decode_string --lane seq --mode native \
    --name 'go   decode_string' --cmd './target/decode_string_go_seq'
rt_end

echo
echo "=== runtime — PAR LANE (multi-core: auto-par vs hand-tuned) ==="
# THE differentiator row. All three parallelize the SAME ITERS reduction across
# the machine's cores — but Kara's default `karac build` output got there with
# NO parallel source (the auto-par-on-reduction pass recognized `sum += pass_len`
# and emitted a karac_par_reduce dispatch), while Rust needed the `rayon` crate +
# `.into_par_iter()` and Go needed hand-written goroutine chunking + WaitGroup +
# partial-merge. Apples-to-apples WITHIN the par lane (all multi-core); per
# BENCH.md's two-lane discipline this is NOT comparable to the single-thread seq
# rows above. Heavier warmup absorbs worker-pool init noise.
rt_begin --warmup 10 --runs 50
rt_cmd --lang kara --approach decode_string --lane par --mode codegen \
    --name 'kara  decode_string (auto-par, NO parallel code)' --cmd './target/decode_string_kara'
rt_cmd --lang rust --approach decode_string --lane par --mode native \
    --name 'rust  decode_string (rayon par_iter)' --cmd './target/decode_rayon'
rt_cmd --lang go --approach decode_string --lane par --mode native \
    --name 'go    decode_string (goroutines + WaitGroup)' --cmd './target/decode_string_go_par'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach decode_string --lane seq --mode interp \
    --name 'py   decode_string' --cmd 'python3 decode_string.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach decode_string --mode codegen \
    --prepare 'rm -f target/decode_string_kara decode_string' \
    --name 'karac build decode_string.kara' \
    --cmd 'sh -c "karac build decode_string.kara >/dev/null && mv decode_string target/decode_string_kara"'
ce_cmd --lang rust --approach decode_string --mode native \
    --prepare 'rm -f target/decode_string' \
    --name 'rustc -O decode_string.rs' --cmd 'rustc -O decode_string.rs -o target/decode_string'
ce_cmd --lang c --approach decode_string --mode native \
    --prepare 'rm -f target/decode_string_c' \
    --name 'clang -O3 decode_string.c' --cmd 'clang -O3 decode_string.c -o target/decode_string_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach decode_string --lane seq --mode codegen --path target/decode_string_kara_seq
size_put --lang kara --approach decode_string --lane par --mode codegen --path target/decode_string_kara
size_put --lang rust --approach decode_string --lane seq --mode native  --path target/decode_string
size_put --lang c    --approach decode_string --lane seq --mode native  --path target/decode_string_c
size_put --lang go   --approach decode_string --lane seq --mode native  --path target/decode_string_go_seq
size_put --lang rust --approach decode_string --lane par --mode native  --path target/decode_rayon
size_put --lang go   --approach decode_string --lane par --mode native  --path target/decode_string_go_par

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach decode_string --lane seq --mode codegen --bytes "$(mem_peak ./target/decode_string_kara_seq)"
mem_put --lang kara --approach decode_string --lane par --mode codegen --bytes "$(mem_peak ./target/decode_string_kara)"
mem_put --lang rust --approach decode_string --lane seq --mode native  --bytes "$(mem_peak ./target/decode_string)"
mem_put --lang c    --approach decode_string --lane seq --mode native  --bytes "$(mem_peak ./target/decode_string_c)"
mem_put --lang go   --approach decode_string --lane seq --mode native  --bytes "$(mem_peak ./target/decode_string_go_seq)"
mem_put --lang rust --approach decode_string --lane par --mode native  --bytes "$(mem_peak ./target/decode_rayon)"
mem_put --lang go   --approach decode_string --lane par --mode native  --bytes "$(mem_peak ./target/decode_string_go_par)"
mem_put --lang python --approach decode_string --lane seq --mode interp --bytes "$(mem_peak python3 decode_string.py)"

echo
echo "=== compile memory (cold) ==="
for src in decode_string.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in decode_string.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in decode_string.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
