"""LeetCode 255 - differential harness. Python oracle.

Mirrors differential.kara exactly: same LCG, same three case families, the same
three deciders, and the same fresh-copy-per-decider discipline (the in-place one
destroys its input).

The uniform family draws DISTINCT values deliberately. LeetCode specifies
distinct integers, and a duplicate makes the question ill-posed rather than hard
-- the divide-and-conquer rejects a duplicate because its bounds are exclusive
while the two stack forms accept it. See the README.
"""

I64_MIN = -(2**63)


def build_valid(seed, n, out):
    state = seed
    val, left, right = [], [], []
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        v = (state // 65536) % 1000
        if not val:
            val.append(v); left.append(-1); right.append(-1)
        else:
            cur = 0
            placed = False
            while not placed:
                if v == val[cur]:
                    placed = True
                elif v < val[cur]:
                    if left[cur] == -1:
                        val.append(v); left.append(-1); right.append(-1)
                        left[cur] = len(val) - 1
                        placed = True
                    else:
                        cur = left[cur]
                else:
                    if right[cur] == -1:
                        val.append(v); left.append(-1); right.append(-1)
                        right[cur] = len(val) - 1
                        placed = True
                    else:
                        cur = right[cur]
    if not val:
        return
    stack = [0]
    while stack:
        node = stack.pop()
        if node != -1:
            out.append(val[node])
            if right[node] != -1:
                stack.append(right[node])
            if left[node] != -1:
                stack.append(left[node])


def make_case(seed):
    state = seed
    out = []
    state = (state * 1103515245 + 12345) & 2147483647
    n = (state // 65536) % 12
    state = (state * 1103515245 + 12345) & 2147483647
    family = (state // 65536) % 4

    if family <= 1:
        build_valid(seed + 7, n, out)
    elif family == 2:
        build_valid(seed + 7, n, out)
        if len(out) >= 2:
            state = (state * 1103515245 + 12345) & 2147483647
            p = (state // 65536) % len(out)
            state = (state * 1103515245 + 12345) & 2147483647
            q = (state // 65536) % len(out)
            out[p], out[q] = out[q], out[p]
    else:
        k = 0
        guard = 0
        while k < n and guard < 400:
            state = (state * 1103515245 + 12345) & 2147483647
            v = (state // 65536) % 1000
            if v not in out:
                out.append(v)
                k += 1
            guard += 1
    return out


def decide_stack(preorder):
    stack = []
    lower = I64_MIN
    for x in preorder:
        if x < lower:
            return False
        while stack and stack[-1] < x:
            lower = stack.pop()
        stack.append(x)
    return True


def decide_inplace(scratch):
    top = 0
    lower = I64_MIN
    for i in range(len(scratch)):
        x = scratch[i]
        if x < lower:
            return False
        while top > 0 and scratch[top - 1] < x:
            lower = scratch[top - 1]
            top -= 1
        scratch[top] = x
        top += 1
    return True


def check(p, lo, hi, has_min, mn, has_max, mx):
    if lo > hi:
        return True
    root = p[lo]
    if has_min and root <= mn:
        return False
    if has_max and root >= mx:
        return False
    split = lo + 1
    while split <= hi and p[split] < root:
        split += 1
    return (check(p, lo + 1, split - 1, has_min, mn, True, root)
            and check(p, split, hi, True, root, has_max, mx))


def decide_divide(p):
    if not p:
        return True
    return check(p, 0, len(p) - 1, False, 0, False, 0)


def main():
    cases = 6000
    seed = 255255
    accepted = rejected = mismatches = total_len = digest = 0

    for _ in range(cases):
        seed = (seed * 1103515245 + 12345) & 2147483647
        a_in = make_case(seed)
        b_in = make_case(seed)
        c_in = make_case(seed)

        a = decide_stack(a_in)
        b = decide_inplace(b_in)
        d = decide_divide(c_in)

        if a != b or a != d:
            mismatches += 1
        if a:
            accepted += 1
            digest = (digest * 131 + 1) % 1000000007
        else:
            rejected += 1
            digest = (digest * 131) % 1000000007
        total_len += len(a_in)

    print(f"cases {cases}")
    print(f"accepted {accepted}")
    print(f"rejected {rejected}")
    print(f"total elements {total_len}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


if __name__ == "__main__":
    main()
