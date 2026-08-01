#!/usr/bin/env bash
# park-screen.sh — which katas can the buf-cache fix possibly have moved?
#
# B-2026-07-30-4's fix (kara 507a446) only changes behaviour for a program that
# PARKS a >= 1 MiB buffer in the runtime's recycling cache: the compensating
# `malloc_trim` is gated on a park having happened. A kata that never parks is
# therefore PROVABLY unaffected and needs no re-bench.
#
# This turns "every number might have moved" into an exact list, for about the
# cost of one bench iteration instead of a full sweep. It builds each kata's
# bench binary and runs it ONCE with the cache counters enabled.
#
#   ./scripts/park-screen.sh [out.tsv]
#
# Output is TSV: kata <TAB> parked <TAB> take_hit <TAB> take_miss
# `parked` of 0 means unaffected; anything else is a re-bench candidate.
# Non-numeric parked values (no-src / build-fail / timeout) need a human look.
#
# Requires a karac built from a commit that INCLUDES 507a446 — the PUT_BYTES /
# stats plumbing it reports landed with that fix.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

OUT="${1:-$ROOT/scripts/park-screen.tsv}"
: > "$OUT"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

for b in leetcode/*/*/bench/bench.sh bespoke/*/bench/bench.sh backend/*/bench/bench.sh; do
    [ -f "$b" ] || continue
    dir="$(dirname "$b")"
    kata="$(basename "$(dirname "$dir")")"

    src="$(ls "$dir"/*.kara 2>/dev/null | head -1)"
    if [ -z "$src" ]; then
        printf '%s\tno-src\t-\t-\n' "$kata" >> "$OUT"
        continue
    fi

    stem="$(basename "$src" .kara)"
    # karac build writes the binary into the CWD, so build from $WORK with an
    # absolute source path (no reliance on OLDPWD inside the subshell).
    if ! ( cd "$WORK" && KARAC_AUTO_PAR=0 timeout 180 karac build "$ROOT/$src" ) >/dev/null 2>&1; then
        printf '%s\tbuild-fail\t-\t-\n' "$kata" >> "$OUT"
        continue
    fi
    bin="$WORK/$stem"
    if [ ! -x "$bin" ]; then
        printf '%s\tno-binary\t-\t-\n' "$kata" >> "$OUT"
        continue
    fi

    # Capture the run's real exit status: a command substitution whose pipeline
    # ends in `|| true` always reports 0, so grep separately from the run.
    run_out="$(KARAC_BUF_CACHE_STATS=1 timeout 600 "$bin" 2>&1 >/dev/null)"
    rc=$?
    stats="$(grep buf-cache <<<"$run_out" || true)"
    if [ -z "$stats" ]; then
        # No counter line at all: the cache was never touched (or the run died).
        if [ "$rc" -ge 124 ]; then
            printf '%s\ttimeout\t-\t-\n' "$kata" >> "$OUT"
        elif [ "$rc" -ne 0 ]; then
            printf '%s\trun-fail-%s\t-\t-\n' "$kata" "$rc" >> "$OUT"
        else
            printf '%s\t0\t0\t0\n' "$kata" >> "$OUT"
        fi
    else
        p=$(sed -n 's/.*parked=\([0-9]*\).*/\1/p' <<<"$stats")
        h=$(sed -n 's/.*hit=\([0-9]*\).*/\1/p' <<<"$stats")
        m=$(sed -n 's/.*miss=\([0-9]*\).*/\1/p' <<<"$stats")
        printf '%s\t%s\t%s\t%s\n' "$kata" "${p:-0}" "${h:-0}" "${m:-0}" >> "$OUT"
    fi

    rm -f "$bin" "$WORK"/*.o 2>/dev/null
done

affected=$(awk -F'\t' '$2 ~ /^[0-9]+$/ && $2 > 0' "$OUT" | wc -l | tr -d ' ')
clean=$(awk -F'\t' '$2 == "0"' "$OUT" | wc -l | tr -d ' ')
other=$(awk -F'\t' '$2 !~ /^[0-9]+$/' "$OUT" | wc -l | tr -d ' ')
echo "park-screen: $affected park (re-bench candidates), $clean clean, $other need-a-look -> $OUT"
