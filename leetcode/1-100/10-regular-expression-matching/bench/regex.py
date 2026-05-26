# Benchmark workload — recursive Regular Expression Matching (LeetCode #10).
# Python mirror of bench/regex.kara. Same N, K, same input set, same sink
# formula — see that file's header for the workload rationale.
#
# CPython at K=10M takes multi-second per sample; bench.sh runs this
# at K=1M (scale = 10×) and reports the projected K=10M wall in the
# README for the ergonomic-foil comparison.


def is_match_at(s: bytes, i: int, p: bytes, j: int) -> bool:
    n = len(s)
    m = len(p)

    if j == m:
        return i == n

    first_match = i < n and (p[j] == s[i] or p[j] == ord('.'))

    if j + 1 < m and p[j + 1] == ord('*'):
        return is_match_at(s, i, p, j + 2) or (
            first_match and is_match_at(s, i + 1, p, j)
        )

    return first_match and is_match_at(s, i + 1, p, j + 1)


def is_match(s: str, p: str) -> bool:
    return is_match_at(s.encode("utf-8"), 0, p.encode("utf-8"), 0)


def main() -> None:
    n = 8
    k_iters = 1_000_000  # 10× scaled down vs the compiled mirrors

    strs = [
        "aa",
        "ab",
        "aab",
        "mississippi",
        "aaaaaaaaaab",
        "aaa",
        "abc",
        "aaab",
    ]
    pats = [
        "a*",
        ".*",
        "c*a*b",
        "mis*is*p*.",
        "a*a*a*a*a*b",
        "ab*a",
        "...",
        "a*b",
    ]
    # Pre-encode to bytes once so the timed loop only pays Python's
    # recursive-call overhead, not bytes() conversion per iter.
    strs_b = [s.encode("utf-8") for s in strs]
    pats_b = [p.encode("utf-8") for p in pats]

    total = 0
    for k in range(k_iters):
        idx = k % n
        if is_match_at(strs_b[idx], 0, pats_b[idx], 0):
            total += 1
    print(total)


if __name__ == "__main__":
    main()
