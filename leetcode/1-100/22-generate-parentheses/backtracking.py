"""LeetCode #22: Generate Parentheses — recursive backtracking.

Mirror of backtracking.kara: same two-counter invariant (extend with '('
while open < n, with ')' while close < open), same owned-snapshot string
concat per child call, same per-case header + one-string-per-line +
"---" output format so `diff <(./bin) <(python3 …)` matches
line-for-line across all five test cases.
"""


def generate_parenthesis(n: int) -> list[str]:
    out: list[str] = []

    def backtrack(cur: str, open_: int, close: int) -> None:
        if close == n:
            # close <= open <= n throughout, so close == n forces
            # open == n: all n pairs placed, cur is complete.
            out.append(cur)
            return
        if open_ < n:
            backtrack(cur + "(", open_ + 1, close)
        if close < open_:
            backtrack(cur + ")", open_, close + 1)

    backtrack("", 0, 0)
    return out


def report(n: int) -> None:
    combos = generate_parenthesis(n)
    print(f"n={n} -> {len(combos)}")
    for c in combos:
        print(c)
    print("---")


def main() -> None:
    report(1)  # 1
    report(2)  # 2
    report(3)  # 5
    report(4)  # 14
    report(8)  # 1430

if __name__ == "__main__":
    main()
