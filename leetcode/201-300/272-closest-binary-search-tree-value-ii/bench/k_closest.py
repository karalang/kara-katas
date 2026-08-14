#!/usr/bin/env python3
"""Benchmark workload for LeetCode #272 — Closest Binary Search Tree Value II.

Algorithm-for-algorithm mirror of k_closest.kara. Kept as a CORRECTNESS ORACLE,
not a timed lane: Python is excluded from the measured comparison
(KARA_BENCH_INCLUDE_PY defaults to 0 in scripts/bench-lib.sh).
"""

NODE_COUNT = 30000
TARGET_COUNT = 100000
K = 8
ROUNDS = 10
SPAN = 1000000


def main() -> None:
    val, left, right = [], [], []
    state = 272272
    placed = tries = 0
    while placed < NODE_COUNT and tries < NODE_COUNT * 4:
        state = (state * 1103515245 + 12345) & 2147483647
        v = (state // 256) % SPAN
        tries += 1
        if not val:
            val.append(v); left.append(-1); right.append(-1)
            placed += 1
        else:
            cur, dup, done = 0, False, False
            while not done:
                if v == val[cur]:
                    dup = True
                    done = True
                elif v < val[cur]:
                    if left[cur] < 0:
                        val.append(v); left.append(-1); right.append(-1)
                        left[cur] = len(val) - 1
                        done = True
                    else:
                        cur = left[cur]
                else:
                    if right[cur] < 0:
                        val.append(v); left.append(-1); right.append(-1)
                        right[cur] = len(val) - 1
                        done = True
                    else:
                        cur = right[cur]
            if not dup:
                placed += 1
    n = len(val)

    targets = []
    tmin = tmax = 0.0
    for t in range(TARGET_COUNT):
        state = (state * 1103515245 + 12345) & 2147483647
        whole = (state // 256) % SPAN
        state = (state * 1103515245 + 12345) & 2147483647
        frac = ((state // 256) % 1000) / 1000.0
        x = whole + frac
        if t == 0:
            tmin = tmax = x
        if x < tmin:
            tmin = x
        if x > tmax:
            tmax = x
        targets.append(x)

    depth_cap = 256
    pred = [0] * depth_cap
    succ = [0] * depth_cap
    lower = [0] * K
    upper = [0] * K
    outv = [0] * K

    sink = 0
    for _ in range(ROUNDS):
        for q in range(TARGET_COUNT):
            target = targets[q]

            pt = st = 0
            cur = 0
            while cur >= 0:
                if val[cur] < target:
                    pred[pt] = cur
                    pt += 1
                    cur = right[cur]
                else:
                    succ[st] = cur
                    st += 1
                    cur = left[cur]

            nl = nu = taken = 0
            while taken < K and (pt > 0 or st > 0):
                take_pred = pt > 0
                if pt > 0 and st > 0:
                    dp = abs(val[pred[pt - 1]] - target)
                    ds = abs(val[succ[st - 1]] - target)
                    take_pred = dp <= ds
                if take_pred:
                    pt -= 1
                    node = pred[pt]
                    c = left[node]
                    while c >= 0:
                        pred[pt] = c
                        pt += 1
                        c = right[c]
                    lower[nl] = val[node]
                    nl += 1
                else:
                    st -= 1
                    node = succ[st]
                    c = right[node]
                    while c >= 0:
                        succ[st] = c
                        st += 1
                        c = left[c]
                    upper[nu] = val[node]
                    nu += 1
                taken += 1

            w = 0
            for i in range(nl - 1, -1, -1):
                outv[w] = lower[i]
                w += 1
            for j in range(nu):
                outv[w] = upper[j]
                w += 1

            acc = 0
            for p in range(w):
                acc = (acc * 31 + outv[p]) % 1000000007
            sink = (sink * 131 + acc) % 1000000007

    vlo = vhi = val[0]
    for m in range(1, n):
        if val[m] < vlo:
            vlo = val[m]
        if val[m] > vhi:
            vhi = val[m]
    print(sink)
    print(f"nodes {n} values {vlo}..{vhi} targets {int(tmin)}..{int(tmax)}")


main()
