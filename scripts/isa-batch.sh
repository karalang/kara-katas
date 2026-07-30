#!/usr/bin/env bash
# isa-batch.sh — run the x86 ISA sweep in resumable batches.
#
# Why batches: a full 245-kata sweep takes ~10h, and an ephemeral cloud
# container gets reclaimed well inside that window (it happened 3x during the
# first sweep). Losing the container mid-sweep used to lose the run, because
# progress lived in a scratchpad log the container owned.
#
# This driver makes progress a property of the COMMITTED DATA instead. Each
# results file records `env.karac_build` (the karac binary's content hash +
# mtime — see bench-lib.sh), so "which katas still need re-running" is
# computable by comparing that stamp against the karac on PATH. A batch runs N
# stale katas, then commits and pushes. A reclaim therefore costs at most one
# batch, and recovery is just: re-run this script.
#
#   ./scripts/isa-batch.sh              # next 25 stale katas, then commit+push
#   ./scripts/isa-batch.sh 10           # next 10
#   ./scripts/isa-batch.sh --list       # show what's stale, run nothing
#   ./scripts/isa-batch.sh --all        # every stale kata in one batch (~10h)
#   ./scripts/isa-batch.sh --only 28,163 # just these kata ids (still stale-filtered)
#   ./scripts/isa-batch.sh --only @file  # ids from a file, one per line
#
# `--only` exists because a full re-sweep is usually NOT worth its wall-clock.
# Measured over the first 18 katas of the single-build re-sweep, refreshing a
# stale kata moved the corpus medians ~1% (kara/rust 1.054 -> 1.041): the large
# stale deficits that motivated the sweep (#191 12.77x -> 1.30x, #28 kmp 6.66x
# -> 1.00x) were two shapes hit by two specific landed fixes, not a corpus-wide
# effect. So the decision-relevant subset is the handful of katas whose recorded
# ratio is bad enough to act on -- refresh those, not all 246.
#
# Staleness is deliberately defined against the LIVE karac, not against a
# pinned id: the point of the re-sweep is a corpus measured by ONE compiler, so
# rebuilding karac mid-sweep re-stales everything already done. Don't rebuild
# karac until the sweep reports 0 stale.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
LOG_DIR="$ROOT/scripts/bench-logs-isa"
mkdir -p "$LOG_DIR"

export BENCH_OUT="${BENCH_OUT:-results.container-x86.json}"

# Same guard as isa-sweep.sh: off x86 every isa_* helper returns early, so the
# sweep would "succeed" having recorded none of the v3 rows it exists to record.
case "$(uname -m)" in
    x86_64 | amd64) ;;
    *)
        echo "isa-batch: host is $(uname -m), not x86 — the ISA lane is a no-op here." >&2
        echo "isa-batch: refusing to run; this sweep would record zero v3 rows." >&2
        exit 2
        ;;
esac

KARAC="$(command -v karac 2>/dev/null)" || KARAC=""
if [ -z "$KARAC" ]; then
    echo "isa-batch: no karac on PATH." >&2
    exit 2
fi
CUR="$(shasum -a 256 "$KARAC" 2>/dev/null | cut -c1-12)"
if [ -z "$CUR" ]; then
    echo "isa-batch: could not fingerprint $KARAC." >&2
    exit 2
fi

n=25
mode=run
ONLY=""
# Parsed as a LOOP, not a case on $1 alone: `--only 28 --list` must list rather
# than silently run the benches, which is what a $1-only parse did.
while [ $# -gt 0 ]; do
    case "$1" in
        --list) mode=list ;;
        --all)  n=100000 ;;
        --only)
            if [ -z "${2:-}" ]; then
                echo "isa-batch: --only needs a comma-separated id list or @file" >&2
                exit 2
            fi
            case "$2" in
                @*)
                    f="${2#@}"
                    [ -r "$f" ] || { echo "isa-batch: cannot read $f" >&2; exit 2; }
                    ONLY="$(tr '\n' ',' <"$f")"
                    ;;
                *) ONLY="$2" ;;
            esac
            n=100000
            shift
            ;;
        *[!0-9]* | '')
            echo "isa-batch: expected a batch size, --list, --all, or --only; got '$1'" >&2
            exit 2
            ;;
        *) n="$1" ;;
    esac
    shift
done

# Stale = results file absent, unreadable, or stamped by a different karac.
# Emitted as "<bench-dir>\t<kata-id>\t<stamp>" so the caller keeps the id for
# logging without re-deriving it from the path.
# ONLY is matched against the kata id's leading number (or the whole directory
# name for non-numeric ids like `utf8-codepoints`), so `--only 28` selects
# 28-find-the-index-of-the-first-occurrence-in-a-string without needing the slug.
stale_list() {
    ISA_ONLY="$ONLY" python3 - "$CUR" <<'PY'
import glob, json, sys, os
cur = sys.argv[1]
only = [t.strip() for t in os.environ.get('ISA_ONLY', '').split(',') if t.strip()]
files = sorted(glob.glob('leetcode/*/*/bench/bench.sh') +
               glob.glob('bespoke/*/bench/bench.sh') +
               glob.glob('backend/*/bench/bench.sh'))
out = os.environ.get('BENCH_OUT', 'results.container-x86.json')
for b in files:
    d = os.path.dirname(b)
    kata = os.path.basename(os.path.dirname(d))
    if only and kata not in only and kata.split('-')[0] not in only:
        continue
    res = os.path.join(d, out)
    try:
        stamp = json.load(open(res)).get('env', {}).get('karac_build', '').split()
        stamp = stamp[0] if stamp else 'missing'
    except FileNotFoundError:
        stamp = 'absent'
    except Exception:
        stamp = 'unreadable'
    if stamp != cur:
        print(f"{d}\t{os.path.basename(os.path.dirname(d))}\t{stamp}")
PY
}

mapfile -t STALE < <(stale_list)
total=${#STALE[@]}

echo "isa-batch: karac=$CUR  stale=$total  batch=$([ "$n" -gt "$total" ] && echo "$total" || echo "$n")"

if [ "$mode" = list ]; then
    printf '%s\n' "${STALE[@]}" | awk -F'\t' '{printf "  %-14s %s\n", $3, $2}'
    exit 0
fi

if [ "$total" -eq 0 ]; then
    echo "SWEEP-COMPLETE all katas measured by karac=$CUR"
    exit 0
fi

ok=0 nov3=0 fail=0 done_ids=()
for row in "${STALE[@]:0:$n}"; do
    IFS=$'\t' read -r dir id _ <<<"$row"
    log="$LOG_DIR/${id}.log"

    if ( cd "$dir" && ./bench.sh ) >"$log" 2>&1; then
        read -r v3 langs < <(python3 - "$dir/$BENCH_OUT" <<'PY'
import json, sys
try:
    m = json.load(open(sys.argv[1]))["measurements"]
except Exception:
    print("0 <unreadable>"); raise SystemExit
langs = sorted({x.get("lang") for x in m if x.get("lang")})
print(sum(l.endswith("_v3") for l in langs), ",".join(langs))
PY
        )
        # NOV3 is distinct from FAIL because _isa_reg DROPS a twin whose output
        # disagrees with the kāra binary, and does so with a stderr warning and
        # exit 0 — a dropped lane is indistinguishable from a passing bench
        # unless the emitted rows are checked.
        if [ "${v3:-0}" -gt 0 ]; then
            echo "OK   $id v3=$v3 langs=$langs"; ok=$((ok + 1))
        else
            echo "NOV3 $id v3=0 langs=$langs"; nov3=$((nov3 + 1))
        fi
        done_ids+=("$id")
    else
        echo "FAIL $id $(tail -2 "$log" | tr '\n' ' ')"; fail=$((fail + 1))
    fi
done

echo "BATCH-DONE ok=$ok nov3=$nov3 fail=$fail"

if [ ${#done_ids[@]} -eq 0 ]; then
    echo "isa-batch: nothing measured, not committing."
    exit 1
fi

# Commit + push before returning, so the next batch starts from a state a
# container reclaim cannot take away. Rebase rather than force: other sessions
# and bots push to this repo.
git add -A -- '*/results.container-x86.json' >/dev/null 2>&1
if git diff --cached --quiet; then
    echo "isa-batch: no results-file changes staged; nothing to push."
    exit 0
fi

remaining=$((total - ok - nov3 - fail))
git commit -q -m "bench: re-measure ISA sweep batch on karac $CUR ($ok ok, $nov3 nov3, $fail fail)

Part of the single-build corpus re-sweep. The prior x86 feed spanned three
karac generations, and spot checks found large stale deficits that evaporated
on current karac (#191 12.77x -> 1.30x after the ctpop idiom; #28 kmp 6.66x ->
1.00x after an upstream perf fix), so per-kata rankings off the mixed feed were
not trustworthy.

Katas in this batch: ${done_ids[*]}

Stale remaining after this batch: $remaining"

for attempt in 1 2 3 4 5; do
    if git push -u origin main -q 2>/dev/null; then
        echo "isa-batch: pushed. stale remaining=$remaining"
        exit 0
    fi
    # A non-fast-forward means the remote moved (other sessions push here);
    # rebase onto it rather than forcing past commits we did not author.
    git fetch origin main -q 2>/dev/null && git rebase origin/main -q 2>/dev/null
    [ "$attempt" -lt 5 ] && sleep $((2 ** attempt))
done
echo "isa-batch: PUSH FAILED after 5 attempts — results are committed locally." >&2
exit 1
