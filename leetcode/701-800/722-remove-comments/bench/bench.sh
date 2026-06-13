#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #722.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata at the algorithm level — the block-comment `in_block` flag
# carries across lines, so the per-document scan has a cross-line data
# dependency and does not admit a per-line parallel lane. BUT the bench's
# OUTER reduction `sum = sum + pass_len(lines)` over ITERS independent passes
# is recognized by karac's auto-par-on-reduction pass, which emits a
# karac_par_reduce dispatch (binary grows ~83 KiB -> ~369 KiB, the par
# machinery). Per BENCH.md's two-lane discipline the auto-par regime would
# mask the per-core codegen-vs-rustc comparison the corpus is built around,
# so we ship a second kara binary built with KARAC_AUTO_PAR=0 (codegen.rs
# Slice 6 gate — short-circuits auto-par dispatch back to plain sequential
# compile_block). The default binary is still built so the auto-par number
# stays reported as the production regime.
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
    local out="target/remove_comments_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

# Par-lane comparators — hand-tuned parallelism a programmer writes by hand,
# against which Kara's auto-par (no parallel source at all) is measured.
build_rayon() {
    local out="target/remove_comments_rayon"
    local src="rayon/src/main.rs"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "building rayon variant (cargo) ..." >&2
        ( cd rayon && cargo build --release --quiet )
        cp -f rayon/target/release/remove_comments_rayon "$out"
    fi
}

build_go_par() {
    local out="target/remove_comments_go_par"
    local src="go-par/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-par ..." >&2
        ( cd go-par && go build -o "../$out" . )
    fi
}

build_rust     remove_comments.rs
build_c        remove_comments.c
build_kara     remove_comments.kara
build_kara_seq remove_comments.kara
build_go_seq
build_rayon
build_go_par

# Sink agreement — every mirror's stdout must be byte-identical before timing.
# Python skipped from the sink check by default (at ITERS=4000 the py run takes
# ~1.7s and would block bench.sh). Set KARA_BENCH_INCLUDE_PY=1 to opt in.
expected="30960000"
mismatch=""
for pair in \
    'kara:./target/remove_comments_kara' \
    'kara_seq:./target/remove_comments_kara_seq' \
    'rust:./target/remove_comments' \
    'c:./target/remove_comments_c' \
    'go:./target/remove_comments_go_seq' \
    'rayon:./target/remove_comments_rayon' \
    'go_par:./target/remove_comments_go_par'; do
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
    py_out=$(python3 remove_comments.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=722 slug=remove-comments group=701-800 \
    title="Remove Comments" workload="REPS=60 ITERS=4000 comment-strip reduction" \
    sink="$expected"

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
# All four comparators run single-threaded. The kara binary built with
# KARAC_AUTO_PAR=0 short-circuits auto-par dispatch back to plain sequential
# codegen — the row directly comparable to rustc -O / clang -O3 / go build on
# a per-core codegen-quality basis.
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach remove_comments --lane seq --mode codegen \
    --name 'kara remove_comments (seq, KARAC_AUTO_PAR=0)' --cmd './target/remove_comments_kara_seq'
rt_cmd --lang rust --approach remove_comments --lane seq --mode native \
    --name 'rust remove_comments' --cmd './target/remove_comments'
rt_cmd --lang c --approach remove_comments --lane seq --mode native \
    --name 'c    remove_comments' --cmd './target/remove_comments_c'
rt_cmd --lang go --approach remove_comments --lane seq --mode native \
    --name 'go   remove_comments' --cmd './target/remove_comments_go_seq'
rt_end

echo
echo "=== runtime — PAR LANE (multi-core: auto-par vs hand-tuned) ==="
# THE differentiator row. All three parallelize the SAME ITERS reduction across
# the machine's cores — but Kara's default `karac build` output got there with
# NO parallel source (auto-par-on-reduction recognized `sum += pass_len` and
# emitted a karac_par_reduce dispatch), while Rust needed the `rayon` crate +
# `.into_par_iter()` and Go needed hand-written goroutine chunking + WaitGroup +
# partial-merge. Apples-to-apples WITHIN the par lane (all multi-core); per
# BENCH.md's two-lane discipline this is NOT comparable to the single-thread seq
# rows above.
rt_begin --warmup 10 --runs 50
rt_cmd --lang kara --approach remove_comments --lane par --mode codegen \
    --name 'kara  remove_comments (auto-par, NO parallel code)' --cmd './target/remove_comments_kara'
rt_cmd --lang rust --approach remove_comments --lane par --mode native \
    --name 'rust  remove_comments (rayon par_iter)' --cmd './target/remove_comments_rayon'
rt_cmd --lang go --approach remove_comments --lane par --mode native \
    --name 'go    remove_comments (goroutines + WaitGroup)' --cmd './target/remove_comments_go_par'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach remove_comments --lane seq --mode interp \
    --name 'py   remove_comments' --cmd 'python3 remove_comments.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach remove_comments --mode codegen \
    --prepare 'rm -f target/remove_comments_kara remove_comments' \
    --name 'karac build remove_comments.kara' \
    --cmd 'sh -c "karac build remove_comments.kara >/dev/null && mv remove_comments target/remove_comments_kara"'
ce_cmd --lang rust --approach remove_comments --mode native \
    --prepare 'rm -f target/remove_comments' \
    --name 'rustc -O remove_comments.rs' --cmd 'rustc -O remove_comments.rs -o target/remove_comments'
ce_cmd --lang c --approach remove_comments --mode native \
    --prepare 'rm -f target/remove_comments_c' \
    --name 'clang -O3 remove_comments.c' --cmd 'clang -O3 remove_comments.c -o target/remove_comments_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach remove_comments --lane seq --mode codegen --path target/remove_comments_kara_seq
size_put --lang kara --approach remove_comments --lane par --mode codegen --path target/remove_comments_kara
size_put --lang rust --approach remove_comments --lane seq --mode native  --path target/remove_comments
size_put --lang c    --approach remove_comments --lane seq --mode native  --path target/remove_comments_c
size_put --lang go   --approach remove_comments --lane seq --mode native  --path target/remove_comments_go_seq
size_put --lang rust --approach remove_comments --lane par --mode native  --path target/remove_comments_rayon
size_put --lang go   --approach remove_comments --lane par --mode native  --path target/remove_comments_go_par

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach remove_comments --lane seq --mode codegen --bytes "$(mem_peak ./target/remove_comments_kara_seq)"
mem_put --lang kara --approach remove_comments --lane par --mode codegen --bytes "$(mem_peak ./target/remove_comments_kara)"
mem_put --lang rust --approach remove_comments --lane seq --mode native  --bytes "$(mem_peak ./target/remove_comments)"
mem_put --lang c    --approach remove_comments --lane seq --mode native  --bytes "$(mem_peak ./target/remove_comments_c)"
mem_put --lang go   --approach remove_comments --lane seq --mode native  --bytes "$(mem_peak ./target/remove_comments_go_seq)"
mem_put --lang rust --approach remove_comments --lane par --mode native  --bytes "$(mem_peak ./target/remove_comments_rayon)"
mem_put --lang go   --approach remove_comments --lane par --mode native  --bytes "$(mem_peak ./target/remove_comments_go_par)"
mem_put --lang python --approach remove_comments --lane seq --mode interp --bytes "$(mem_peak python3 remove_comments.py)"

echo
echo "=== compile memory (cold) ==="
for src in remove_comments.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in remove_comments.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in remove_comments.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
