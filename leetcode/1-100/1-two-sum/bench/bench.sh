#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #1.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Two lanes. brute_force runs K=100 independent O(n²) two_sum calls: heavy
# enough per call that karac's auto-par-on-reduction clears the runtime gate and
# parallelizes the `for _ in 0..100` reduction with NO parallel source (unblocked
# by B-2026-06-12-7, the for-_ wildcard fix) — so it gets a PAR LANE vs hand-tuned
# C-pthreads / rayon / goroutines. hash_map's per-call work (~5K inserts) is too
# light; the runtime correctly keeps it serial, so it stays seq-only. At
# brute_force's original K=10 the runtime also (correctly) declined par — the
# par lane needs the K=100 workload.
#
# Requires: hyperfine (`brew install hyperfine`), rustc + cargo (rustup), clang,
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
require cargo     "rustup (https://rustup.rs)  — needed for the rayon par-lane variant"
require clang     "xcode-select --install (macOS) or your distro's clang package"
require go        "brew install go  or your distro's golang package"
require karac     "cargo install --path . --features llvm  (from karac-rust checkout)"

# Structured-JSON emission (writes bench/results.json). Set BENCH_JSON=0 to
# skip — the human-readable console output below is unaffected either way.
if [ "${BENCH_JSON:-1}" = "1" ]; then
    require jq      "brew install jq"
    require python3 "python3 ships with macOS; or 'brew install python'"
fi
ROOT="$(cd ../../../.. && pwd)"
. "$ROOT/scripts/bench-lib.sh"

# /usr/bin/time -l (macOS BSD time) prints a "peak memory footprint" line on
# stderr. We capture its stderr through a brace-group redirect, discard the
# wrapped command's own stdout, and parse the bytes column. Memory is much
# more stable run-to-run than wall-time (no scheduling/cache variance), so a
# single sample is honest — no hyperfine-style averaging needed.
print_mem() {
    local label="$1" bytes="$2"
    local mib
    mib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1048576}')
    printf '  %-34s %12s bytes (%6s MiB)\n' "$label" "$bytes" "$mib"
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

# Two-sum has two algorithmic approaches, so we keep a single go module
# (bench/go-seq/) with two main packages (./brute_force, ./hash_map).
# Each builds into target/<approach>_go_seq.
build_go_seq() {
    local pkg="$1"           # subpackage name (e.g. brute_force)
    local out="target/${pkg}_go_seq"
    local src="go-seq/${pkg}/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq/${pkg} ..." >&2
        ( cd go-seq && go build -o "../$out" "./${pkg}" )
    fi
}

# brute_force auto-pars (its O(n²) per-call work clears the runtime gate at
# K=100 calls); build a KARAC_AUTO_PAR=0 seq twin for the apples-to-apples seq
# lane. hash_map stays seq-only (per-call work too light — runtime declines).
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

# Par-lane comparators for brute_force — hand-tuned parallelism vs Kāra auto-par.
build_rayon() {
    local out="target/two_sum_rayon"
    local src="rayon/src/main.rs"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "building rayon variant (cargo) ..." >&2
        ( cd rayon && cargo build --release --quiet )
        cp -f rayon/target/release/two_sum_rayon "$out"
    fi
}
build_go_par() {
    local out="target/two_sum_go_par"
    local src="go-par/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-par ..." >&2
        ( cd go-par && go build -o "../$out" . )
    fi
}
# C pthreads — the par-lane bare-metal FLOOR (raw OS threads, no runtime).
build_c_par() {
    local out="target/brute_force_c_par"
    local src="brute_force_par.c"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling c-par (pthreads) ..." >&2
        clang -O3 "$src" -o "$out" -lpthread
    fi
}

build_rust brute_force.rs
build_rust hash_map.rs
build_c    brute_force.c
build_c    hash_map.c
build_kara brute_force.kara
build_kara hash_map.kara
build_kara_seq brute_force.kara
build_go_seq brute_force
build_go_seq hash_map
build_rayon
build_go_par
build_c_par

# Sink agreement — every mirror's stdout must be byte-identical before
# timing. Python skipped from sink check by default — at N=5000 the
# brute-force py run takes ~1.5s and bench.sh would block on it.
# Set `KARA_BENCH_INCLUDE_PY=1` to opt in.
#
# Plain "name:command" pairs (no associative arrays — macOS bash is 3.2).
# Per-approach sink: brute_force scaled to K=100 calls (-200) so its O(n²) work
# clears the runtime auto-par gate; hash_map stays K=10 (-20). Triples are
# name:command:expected.
mismatch=""
for triple in \
    'bf_kara:./target/brute_force_kara:-200' \
    'bf_kara_seq:./target/brute_force_kara_seq:-200' \
    'bf_rust:./target/brute_force:-200' \
    'bf_c:./target/brute_force_c:-200' \
    'bf_go:./target/brute_force_go_seq:-200' \
    'bf_rayon:./target/two_sum_rayon:-200' \
    'bf_go_par:./target/two_sum_go_par:-200' \
    'bf_c_par:./target/brute_force_c_par:-200' \
    'hm_kara:./target/hash_map_kara:-20' \
    'hm_rust:./target/hash_map:-20' \
    'hm_c:./target/hash_map_c:-20' \
    'hm_go:./target/hash_map_go_seq:-20'; do
    name="${triple%%:*}"
    rest="${triple#*:}"
    cmd="${rest%:*}"
    exp="${rest##*:}"
    out=$("$cmd")
    if [ "$out" != "$exp" ]; then
        mismatch="$mismatch ${name}=${out}(want ${exp})"
    fi
done
if [ -n "$mismatch" ]; then
    echo "sink mismatch:$mismatch" >&2
    exit 1
fi
echo "sink ok (brute_force=-200 ×8, hash_map=-20 ×4)"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_bf=$(python3 brute_force.py)
    py_hm=$(python3 hash_map.py)
    if [ "$py_bf" != "-200" ] || [ "$py_hm" != "-20" ]; then
        echo "python sink mismatch: py_bf=$py_bf(want -200) py_hm=$py_hm(want -20)" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=1 slug=two-sum group=1-100 \
    title="Two Sum" workload="brute_force N=5000 K=100 / hash_map N=5000 K=10" \
    sink="-200"

# Two runtime batches because the workloads span ~5 orders of magnitude:
#   - short workloads (<50ms): hash_map across all langs, brute_force in
#     compiled languages. Need 30 runs to drown startup jitter.
#   - long workloads (>1s): kara interp on both approaches, py brute_force.
#     Already <2% RSD at 10 runs; bumping runs adds wall without info.
# Both batches feed one cumulative runtime export (rt_end merges per batch).
echo "=== runtime — short workloads ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach brute_force --lane seq --mode codegen \
    --name 'kara brute_force (seq, KARAC_AUTO_PAR=0)' --cmd './target/brute_force_kara_seq'
rt_cmd --lang rust --approach brute_force --lane seq --mode native \
    --name 'rust brute_force' --cmd './target/brute_force'
rt_cmd --lang c --approach brute_force --lane seq --mode native \
    --name 'c    brute_force' --cmd './target/brute_force_c'
rt_cmd --lang go --approach brute_force --lane seq --mode native \
    --name 'go   brute_force' --cmd './target/brute_force_go_seq'
rt_cmd --lang kara --approach hash_map --lane seq --mode codegen \
    --name 'kara hash_map (codegen)' --cmd './target/hash_map_kara'
rt_cmd --lang rust --approach hash_map --lane seq --mode native \
    --name 'rust hash_map' --cmd './target/hash_map'
rt_cmd --lang c --approach hash_map --lane seq --mode native \
    --name 'c    hash_map' --cmd './target/hash_map_c'
rt_cmd --lang go --approach hash_map --lane seq --mode native \
    --name 'go   hash_map' --cmd './target/hash_map_go_seq'
rt_cmd --lang python --approach hash_map --lane seq --mode interp \
    --name 'py   hash_map' --cmd 'python3 hash_map.py'
rt_end

echo
echo "=== runtime — PAR LANE: brute_force (multi-core: auto-par vs hand-tuned vs metal floor) ==="
# brute_force only — its O(n²) per-call work clears the runtime auto-par gate at
# K=100 calls, so `karac build` emits a karac_par_reduce dispatch off the plain
# `for _ in 0..100` reduction with NO parallel source (unblocked by B-2026-06-12-7,
# the for-_ wildcard auto-par fix). C/rayon/go parallelize the SAME reduction by
# hand. The C row is the bare-metal FLOOR (raw pthreads, no runtime). hash_map is
# absent — its per-call work is too light, the runtime correctly keeps it serial.
# Apples-to-apples WITHIN the par lane; NOT comparable to the single-thread seq rows.
rt_begin --warmup 10 --runs 50
rt_cmd --lang kara --approach brute_force --lane par --mode codegen \
    --name 'kara  brute_force (auto-par, NO parallel code)' --cmd './target/brute_force_kara'
rt_cmd --lang c --approach brute_force --lane par --mode native \
    --name 'c     brute_force (pthreads — metal floor)' --cmd './target/brute_force_c_par'
rt_cmd --lang rust --approach brute_force --lane par --mode native \
    --name 'rust  brute_force (rayon par_iter)' --cmd './target/two_sum_rayon'
rt_cmd --lang go --approach brute_force --lane par --mode native \
    --name 'go    brute_force (goroutines + WaitGroup)' --cmd './target/two_sum_go_par'
rt_end

echo
echo "=== runtime — long workloads (interp + py brute_force) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang kara --approach hash_map --lane seq --mode interp \
    --name 'kara hash_map (interp)' --cmd 'karac run hash_map.kara'
rt_cmd --lang python --approach brute_force --lane seq --mode interp \
    --name 'py   brute_force' --cmd 'python3 brute_force.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
# Per BENCH.md: hyperfine --warmup 1 --runs 10 with --prepare deleting the
# build artifact so every invocation is a true cold compile. karac/rustc/clang
# are the single-file compilers; rayon (cargo) and go are excluded — their
# first invocation mixes dep resolution + link and isn't comparable to a
# single-file compile.
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach brute_force --mode codegen \
    --prepare 'rm -f target/brute_force_kara brute_force' \
    --name 'karac build brute_force.kara' \
    --cmd 'sh -c "karac build brute_force.kara >/dev/null && mv brute_force target/brute_force_kara"'
ce_cmd --lang kara --approach hash_map --mode codegen \
    --prepare 'rm -f target/hash_map_kara hash_map' \
    --name 'karac build hash_map.kara' \
    --cmd 'sh -c "karac build hash_map.kara >/dev/null && mv hash_map target/hash_map_kara"'
ce_cmd --lang rust --approach brute_force --mode native \
    --prepare 'rm -f target/brute_force' \
    --name 'rustc -O brute_force.rs' --cmd 'rustc -O brute_force.rs -o target/brute_force'
ce_cmd --lang rust --approach hash_map --mode native \
    --prepare 'rm -f target/hash_map' \
    --name 'rustc -O hash_map.rs' --cmd 'rustc -O hash_map.rs -o target/hash_map'
ce_cmd --lang c --approach brute_force --mode native \
    --prepare 'rm -f target/brute_force_c' \
    --name 'clang -O3 brute_force.c' --cmd 'clang -O3 brute_force.c -o target/brute_force_c'
ce_cmd --lang c --approach hash_map --mode native \
    --prepare 'rm -f target/hash_map_c' \
    --name 'clang -O3 hash_map.c' --cmd 'clang -O3 hash_map.c -o target/hash_map_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach brute_force --lane seq --mode codegen --path target/brute_force_kara_seq
size_put --lang kara --approach brute_force --lane par --mode codegen --path target/brute_force_kara
size_put --lang c    --approach brute_force --lane par --mode native  --path target/brute_force_c_par
size_put --lang rust --approach brute_force --lane par --mode native  --path target/two_sum_rayon
size_put --lang go   --approach brute_force --lane par --mode native  --path target/two_sum_go_par
size_put --lang kara --approach hash_map    --lane seq --mode codegen --path target/hash_map_kara
size_put --lang rust --approach brute_force --lane seq --mode native  --path target/brute_force
size_put --lang rust --approach hash_map    --lane seq --mode native  --path target/hash_map
size_put --lang c    --approach brute_force --lane seq --mode native  --path target/brute_force_c
size_put --lang c    --approach hash_map    --lane seq --mode native  --path target/hash_map_c
size_put --lang go   --approach brute_force --lane seq --mode native  --path target/brute_force_go_seq
size_put --lang go   --approach hash_map    --lane seq --mode native  --path target/hash_map_go_seq

echo
echo "=== runtime memory (peak) ==="
# python's number includes ~7 MB CPython runtime baseline regardless of N.
# `interp` rows include the karac binary itself (~7 MB with --features llvm)
# plus the AST/value heap karac walks at runtime — `karac run` re-runs
# lex → … → ownership → tree-walk every invocation, so the number measures
# interpreter overhead + algorithm working set, not algorithm alone.
mem_put --lang kara --approach brute_force --lane seq --mode codegen --bytes "$(mem_peak ./target/brute_force_kara_seq)"
mem_put --lang kara --approach brute_force --lane par --mode codegen --bytes "$(mem_peak ./target/brute_force_kara)"
mem_put --lang c    --approach brute_force --lane par --mode native  --bytes "$(mem_peak ./target/brute_force_c_par)"
mem_put --lang rust --approach brute_force --lane par --mode native  --bytes "$(mem_peak ./target/two_sum_rayon)"
mem_put --lang go   --approach brute_force --lane par --mode native  --bytes "$(mem_peak ./target/two_sum_go_par)"
mem_put --lang kara --approach hash_map    --lane seq --mode codegen --bytes "$(mem_peak ./target/hash_map_kara)"
mem_put --lang kara --approach hash_map    --lane seq --mode interp  --bytes "$(mem_peak karac run hash_map.kara)"
mem_put --lang rust --approach brute_force --lane seq --mode native  --bytes "$(mem_peak ./target/brute_force)"
mem_put --lang rust --approach hash_map    --lane seq --mode native  --bytes "$(mem_peak ./target/hash_map)"
mem_put --lang c    --approach brute_force --lane seq --mode native  --bytes "$(mem_peak ./target/brute_force_c)"
mem_put --lang c    --approach hash_map    --lane seq --mode native  --bytes "$(mem_peak ./target/hash_map_c)"
mem_put --lang go   --approach brute_force --lane seq --mode native  --bytes "$(mem_peak ./target/brute_force_go_seq)"
mem_put --lang go   --approach hash_map    --lane seq --mode native  --bytes "$(mem_peak ./target/hash_map_go_seq)"
mem_put --lang python --approach brute_force --lane seq --mode interp --bytes "$(mem_peak python3 brute_force.py)"
mem_put --lang python --approach hash_map    --lane seq --mode interp --bytes "$(mem_peak python3 hash_map.py)"

echo
echo "=== compile memory (cold) ==="
# Artifact deleted before each measurement so the karac/rustc/clang invocation
# is a full cold compile. karac's number covers lex → … → ownership → codegen IR
# build → LLVM optimization passes. Regression detection: a sudden 10× spike
# on `karac build` here is the signature of an algorithmic blowup in a
# frontend phase. Go is omitted from the compile-memory row per BENCH.md —
# `go build`'s first run mixes module resolution + std-lib link and is not
# comparable to a single-file rustc/clang/karac invocation.
for src in brute_force.kara hash_map.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in brute_force.rs hash_map.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in brute_force.c hash_map.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
