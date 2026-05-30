"""LeetCode #17: Letter Combinations of a Phone Number — iterative BFS.

Mirror of letter_combinations.kara: same BFS expansion shape, same group
table, same empty-input sentinel, same per-case header + one-combo-per-
line + "---" output format so `diff <(./bin) <(python3 …)` matches
line-for-line across all ten test cases.
"""


GROUPS = ["abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"]


def letter_combinations(digits: str) -> list[str]:
    if not digits:
        return []
    out = [""]
    for d in digits:
        idx = ord(d) - ord("2")
        nxt = []
        for prefix in out:
            for letter in GROUPS[idx]:
                nxt.append(prefix + letter)
        out = nxt
    return out


def report(digits: str) -> None:
    combos = letter_combinations(digits)
    print(f'"{digits}" -> {len(combos)}')
    for c in combos:
        print(c)
    print("---")


def main() -> None:
    report("23")        # 9
    report("")          # 0
    report("2")         # 3
    report("7")         # 4
    report("9")         # 4
    report("27")        # 12
    report("79")        # 16
    report("234")       # 27
    report("2378")      # 108
    report("7799")      # 256


if __name__ == "__main__":
    main()
