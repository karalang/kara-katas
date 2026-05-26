# LeetCode #10: Regular Expression Matching — Python mirror of regex.kara.
#
# Same recursive structure: at each step decide whether the
# next-after-current pattern char is `*`, and branch on the two `*`
# subproblems (skip / consume-and-keep) accordingly. Indices over the
# byte view rather than subslicing — keeps the structure identical to
# the Kara version.


def is_match_at(s: bytes, i: int, p: bytes, j: int) -> bool:
    n = len(s)
    m = len(p)

    if j == m:
        return i == n

    first_match = i < n and (p[j] == s[i] or p[j] == ord('.'))

    if j + 1 < m and p[j + 1] == ord('*'):
        # Either consume the entire `x*` with zero s chars, or eat one
        # s char and keep `x*` for a possible further match.
        return is_match_at(s, i, p, j + 2) or (
            first_match and is_match_at(s, i + 1, p, j)
        )

    return first_match and is_match_at(s, i + 1, p, j + 1)


def is_match(s: str, p: str) -> bool:
    return is_match_at(s.encode("utf-8"), 0, p.encode("utf-8"), 0)


def report(s: str, p: str) -> None:
    r = is_match(s, p)
    print(f'is_match("{s}", "{p}"): {"true" if r else "false"}')


def main() -> None:
    report("aa", "a")
    report("aa", "a*")
    report("ab", ".*")
    report("aab", "c*a*b")
    report("mississippi", "mis*is*p*.")
    report("", "")
    report("", "a*")
    report("", "a*b*c*")
    report("", "a")
    report("a", "")
    report("aaa", "a*a")
    report("aaa", "ab*a*c*a")
    report("aaa", "ab*a")
    report("ab", ".*c")
    report("a", "a*a")
    report("a", "ab*")
    report("abcd", "d*")
    report("abc", "..")
    report("abc", "...")
    report("abc", "....")
    report("aaab", "a*b")
    report("aaaaaaaaaaaaab", "a*a*a*a*a*b")


if __name__ == "__main__":
    main()
