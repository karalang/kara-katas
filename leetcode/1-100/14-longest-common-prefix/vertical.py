# LeetCode #14: Longest Common Prefix — vertical scanning.
# Mirror of vertical.kara — see that file's header for the rationale.


def longest_common_prefix(strs: list[str]) -> str:
    n = len(strs)
    if n == 0:
        return ""

    first = strs[0]
    first_len = len(first)

    col = 0
    while col < first_len:
        c = first[col]
        s = 1
        while s < n:
            other = strs[s]
            if col >= len(other) or other[col] != c:
                return first[:col]
            s += 1
        col += 1
    return first


def report(strs: list[str]) -> None:
    print(f'"{longest_common_prefix(strs)}"')


def main() -> None:
    report(["flower", "flow", "flight"])   # "fl"
    report(["dog", "racecar", "car"])      # ""
    report(["alone"])                      # "alone"
    report(["", "anything"])               # ""
    report(["same", "same", "same"])       # "same"
    report(["abab", "ab", "abc"])          # "ab"
    report(["a", "a", "ab"])               # "a"


if __name__ == "__main__":
    main()
