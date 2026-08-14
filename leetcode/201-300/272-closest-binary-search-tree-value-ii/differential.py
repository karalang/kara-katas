#!/usr/bin/env python3
"""LeetCode 272 — differential harness. Mirror of differential.kara.

Three solvers over 4,000 randomized BSTs: the two-stack merge, the sorted-array
window, and the explicit (distance, value) ranking. Same generator, same
counters, same digest — line-for-line with the Kāra version so a divergence is
a compiler question, not a translation question.
"""


def advance_pred(val, left, right, pred):
    node = pred.pop()
    cur = left[node]
    while cur >= 0:
        pred.append(cur)
        cur = right[cur]
    return val[node]


def advance_succ(val, left, right, succ):
    node = succ.pop()
    cur = right[node]
    while cur >= 0:
        succ.append(cur)
        cur = left[cur]
    return val[node]


def merge_k(val, left, right, root, target, k):
    pred, succ = [], []
    cur = root
    while cur >= 0:
        if val[cur] < target:
            pred.append(cur)
            cur = right[cur]
        else:
            succ.append(cur)
            cur = left[cur]
    lower, upper = [], []
    taken = 0
    while taken < k:
        have_p, have_s = len(pred) > 0, len(succ) > 0
        if not have_p and not have_s:
            break
        take_pred = have_p
        if have_p and have_s:
            dp = abs(val[pred[-1]] - target)
            ds = abs(val[succ[-1]] - target)
            take_pred = dp <= ds
        if take_pred:
            lower.append(advance_pred(val, left, right, pred))
        else:
            upper.append(advance_succ(val, left, right, succ))
        taken += 1
    return lower[::-1] + upper


def collect(val, left, right, root):
    """DFS order — deliberately NOT the in-order array.

    Handing the ranking solver `sorted` would quietly disable the check it
    exists to perform: a selection sort scanning an ascending array with a
    strict `<` already keeps the first minimum it meets, which is the smaller
    value, so the explicit (distance, value) key becomes redundant. Measured on
    the Kāra side: with sorted input, deleting the tie-break scored ZERO
    mismatches out of 4,000; with this order it scores 97.
    """
    out, stack = [], [root]
    while stack:
        node = stack.pop()
        out.append(val[node])
        if left[node] >= 0:
            stack.append(left[node])
        if right[node] >= 0:
            stack.append(right[node])
    return out


def inorder(val, left, right, root):
    out, stack, cur = [], [], root
    while cur >= 0 or stack:
        while cur >= 0:
            stack.append(cur)
            cur = left[cur]
        node = stack.pop()
        out.append(val[node])
        cur = right[node]
    return out


def lower_bound(sorted_vals, target):
    a, b = 0, len(sorted_vals)
    while a < b:
        mid = a + (b - a) // 2
        if sorted_vals[mid] < target:
            a = mid + 1
        else:
            b = mid
    return a


def window_k(sorted_vals, target, k):
    n = len(sorted_vals)
    hi = lower_bound(sorted_vals, target)
    lo = hi - 1
    taken = 0
    while taken < k:
        if lo < 0 and hi >= n:
            break
        take_lo = hi >= n
        if lo >= 0 and hi < n:
            dl = abs(sorted_vals[lo] - target)
            dh = abs(sorted_vals[hi] - target)
            take_lo = dl <= dh
        if take_lo:
            lo -= 1
        else:
            hi += 1
        taken += 1
    return sorted_vals[lo + 1:hi]


def window_had_tie_step(sorted_vals, target, k):
    n = len(sorted_vals)
    hi = lower_bound(sorted_vals, target)
    lo = hi - 1
    taken, saw = 0, False
    while taken < k:
        if lo < 0 and hi >= n:
            break
        take_lo = hi >= n
        if lo >= 0 and hi < n:
            dl = abs(sorted_vals[lo] - target)
            dh = abs(sorted_vals[hi] - target)
            if dl == dh:
                saw = True
            take_lo = dl <= dh
        if take_lo:
            lo -= 1
        else:
            hi += 1
        taken += 1
    return saw


def rank_k(vals_in, target, k):
    vals = list(vals_in)
    n = len(vals)
    want = min(k, n)
    for i in range(want):
        best = i
        best_d = abs(vals[i] - target)
        for j in range(i + 1, n):
            d = abs(vals[j] - target)
            if d < best_d or (d == best_d and vals[j] < vals[best]):
                best = j
                best_d = d
        vals[i], vals[best] = vals[best], vals[i]
    return sorted(vals[:want])


def main():
    cases = 4000
    seed = 272272
    mismatches = tie_steps = open_side = k_over_n = nodes_total = digest = 0

    for _ in range(cases):
        seed = (seed * 1103515245 + 12345) & 2147483647
        want_n = 1 + (seed // 256) % 40
        val, left, right = [], [], []
        placed = tries = 0
        while placed < want_n and tries < want_n * 4:
            seed = (seed * 1103515245 + 12345) & 2147483647
            v = (seed // 256) % 400
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

        srt = inorder(val, left, right, 0)
        n = len(srt)

        seed = (seed * 1103515245 + 12345) & 2147483647
        family = (seed // 256) % 5
        target = 0.0
        if family == 0 and n >= 2:
            seed = (seed * 1103515245 + 12345) & 2147483647
            at = (seed // 256) % (n - 1)
            target = (srt[at] + srt[at + 1]) / 2.0
        if family == 1 and n >= 2:
            seed = (seed * 1103515245 + 12345) & 2147483647
            at = (seed // 256) % (n - 1)
            mid = (srt[at] + srt[at + 1]) / 2.0
            seed = (seed * 1103515245 + 12345) & 2147483647
            target = mid - 0.125 if (seed // 256) % 2 == 0 else mid + 0.125
        if family == 2:
            seed = (seed * 1103515245 + 12345) & 2147483647
            target = float(srt[(seed // 256) % n])
        if family == 3:
            seed = (seed * 1103515245 + 12345) & 2147483647
            target = srt[0] - 7.5 if (seed // 256) % 2 == 0 else srt[n - 1] + 7.5
        if family == 4 or (family <= 1 and n < 2):
            seed = (seed * 1103515245 + 12345) & 2147483647
            target = ((seed // 256) % 48000) / 100.0 - 40.0

        seed = (seed * 1103515245 + 12345) & 2147483647
        kfam = (seed // 256) % 5
        k = 1
        if kfam == 1:
            seed = (seed * 1103515245 + 12345) & 2147483647
            k = 1 + (seed // 256) % 4
        if kfam == 2:
            k = n // 2 + 1
        if kfam == 3:
            k = n
        if kfam == 4:
            k = n + 2

        a = merge_k(val, left, right, 0, target, k)
        b = window_k(srt, target, k)
        d = rank_k(collect(val, left, right, 0), target, k)
        if a != b or a != d:
            mismatches += 1

        if window_had_tie_step(srt, target, k):
            tie_steps += 1
        if target < srt[0] or target > srt[n - 1]:
            open_side += 1
        if k > n:
            k_over_n += 1

        nodes_total += n
        for e in a:
            digest = (digest * 131 + e) % 1000000007
        digest = (digest * 131 + len(a) + n) % 1000000007

    print(f"cases {cases}")
    print(f"nodes built {nodes_total}")
    print(f"cases where a DECISION STEP saw a tie {tie_steps}")
    print(f"targets outside the value range {open_side}")
    print(f"cases with k > n {k_over_n}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


main()
