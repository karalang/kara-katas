"""LeetCode 270 — differential harness (Python mirror / oracle).

Mirrors differential.kara draw-for-draw: the same LCG, the same order of seed
advances, the same BST construction and the same five target families, so the
printed digest must match byte for byte.
"""

MASK = 2147483647
DIGEST_MOD = 1000000007


def descent(val, left, right, root, target):
    best = val[root]
    best_diff = abs(val[root] - target)
    cur = root
    while cur >= 0:
        v = val[cur]
        d = abs(v - target)
        if d < best_diff or (d == best_diff and v < best):
            best = v
            best_diff = d
        cur = right[cur] if v < target else left[cur]
    return best


def scan(val, left, right, root, target):
    stack = [root]
    best = val[root]
    best_diff = abs(val[root] - target)
    while stack:
        cur = stack.pop()
        v = val[cur]
        d = abs(v - target)
        if d < best_diff or (d == best_diff and v < best):
            best = v
            best_diff = d
        if left[cur] >= 0:
            stack.append(left[cur])
        if right[cur] >= 0:
            stack.append(right[cur])
    return best


def bounds(val, left, right, root, target):
    has_floor = has_ceil = False
    floor_v = ceil_v = 0
    cur = root
    while cur >= 0:
        v = val[cur]
        if v <= target:
            if not has_floor or v > floor_v:
                has_floor, floor_v = True, v
            cur = right[cur]
        else:
            if not has_ceil or v < ceil_v:
                has_ceil, ceil_v = True, v
            cur = left[cur]
    if not has_floor:
        return ceil_v
    if not has_ceil:
        return floor_v
    return floor_v if abs(floor_v - target) <= abs(ceil_v - target) else ceil_v


def main():
    cases = 4000
    seed = 270270

    mismatches = ties = open_side = nodes_total = digest = 0

    for _ in range(cases):
        seed = (seed * 1103515245 + 12345) & MASK
        n = (seed // 65536) % 14 + 1

        val, left, right = [], [], []
        used = [False] * 60

        inserted = tries = 0
        while inserted < n and tries < 200:
            seed = (seed * 1103515245 + 12345) & MASK
            v = (seed // 65536) % 40
            tries += 1
            if used[v]:
                continue
            used[v] = True
            if not val:
                val.append(v)
                left.append(-1)
                right.append(-1)
            else:
                cur = 0
                while True:
                    if v < val[cur]:
                        if left[cur] < 0:
                            val.append(v)
                            left.append(-1)
                            right.append(-1)
                            left[cur] = len(val) - 1
                            break
                        cur = left[cur]
                    else:
                        if right[cur] < 0:
                            val.append(v)
                            left.append(-1)
                            right.append(-1)
                            right[cur] = len(val) - 1
                            break
                        cur = right[cur]
            inserted += 1
        if not val:
            continue

        sorted_vals = [s for s in range(40) if used[s]]

        seed = (seed * 1103515245 + 12345) & MASK
        family = (seed // 65536) % 5
        target = 0.0

        if family == 0 and len(sorted_vals) >= 2:
            seed = (seed * 1103515245 + 12345) & MASK
            at = (seed // 65536) % (len(sorted_vals) - 1)
            target = (sorted_vals[at] + sorted_vals[at + 1]) / 2.0
        if family == 1 and len(sorted_vals) >= 2:
            seed = (seed * 1103515245 + 12345) & MASK
            at = (seed // 65536) % (len(sorted_vals) - 1)
            mid = (sorted_vals[at] + sorted_vals[at + 1]) / 2.0
            seed = (seed * 1103515245 + 12345) & MASK
            target = mid - 0.125 if (seed // 65536) % 2 == 0 else mid + 0.125
        if family == 2:
            seed = (seed * 1103515245 + 12345) & MASK
            target = float(sorted_vals[(seed // 65536) % len(sorted_vals)])
        if family == 3:
            seed = (seed * 1103515245 + 12345) & MASK
            if (seed // 65536) % 2 == 0:
                target = sorted_vals[0] - 7.5
            else:
                target = sorted_vals[-1] + 7.5
        if family == 4 or (family <= 1 and len(sorted_vals) < 2):
            seed = (seed * 1103515245 + 12345) & MASK
            target = ((seed // 65536) % 4800) / 100.0 - 4.0

        a = descent(val, left, right, 0, target)
        b = scan(val, left, right, 0, target)
        d = bounds(val, left, right, 0, target)
        if a != b or a != d:
            mismatches += 1

        best_d = min(abs(s - target) for s in sorted_vals)
        at_best = sum(1 for s in sorted_vals if abs(s - target) == best_d)
        if at_best > 1:
            ties += 1
        if target < sorted_vals[0] or target > sorted_vals[-1]:
            open_side += 1

        nodes_total += len(val)
        digest = (digest * 131 + a + len(val)) % DIGEST_MOD

    print(f"cases {cases}")
    print(f"nodes built {nodes_total}")
    print(f"targets that TIE two values {ties}")
    print(f"targets outside the value range {open_side}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


main()
