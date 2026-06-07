"""Bench mirror of backtracking.kara — same owned-snapshot recursive
backtracking, same total-bytes sink. Unlike most of the corpus, Python
runs the FULL K=150 here: the workload is allocation/copy-bound (string
concat is C-level memcpy in CPython), so the interpreter gap is narrow
enough that no scale-down is needed.
"""


def generate_parenthesis(n: int) -> list[str]:
    out: list[str] = []

    def backtrack(cur: str, open_: int, close: int) -> None:
        if close == n:
            out.append(cur)
            return
        if open_ < n:
            backtrack(cur + "(", open_ + 1, close)
        if close < open_:
            backtrack(cur + ")", open_, close + 1)

    backtrack("", 0, 0)
    return out


def main() -> None:
    n = 10
    iters = 150  # same scale as the compiled mirrors
    total = 0
    for _ in range(iters):
        combos = generate_parenthesis(n)
        total += sum(len(c) for c in combos)
    print(total)  # 150 * 16796 * 20 = 50,388,000


if __name__ == "__main__":
    main()
