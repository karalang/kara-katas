"""LeetCode #22: Generate Parentheses — closure-number DP (bottom-up).

Mirror of closure_number.kara: same unique "(" A ")" B decomposition,
same bottom-up table indexed by pair count, same enclosed-size-ascending
enumeration order, same per-case header + one-string-per-line + "---"
output format so `diff <(./bin) <(python3 …)` matches line-for-line
across all five test cases.
"""


def generate_parenthesis(n: int) -> list[str]:
    # table[m] = all well-formed strings of m pairs; f(0) = [""].
    table: list[list[str]] = [[""]]
    for m in range(1, n + 1):
        row: list[str] = []
        for i in range(m):
            # Split: A (enclosed) has i pairs, B (trailing) has m-1-i.
            j = m - 1 - i
            for a in table[i]:
                for b in table[j]:
                    row.append("(" + a + ")" + b)
        if m == n:
            return row
        table.append(row)
    return table[0]  # n == 0 — outside LeetCode's bounds, kept total


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
