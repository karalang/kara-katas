"""Benchmark workload — Letter Combinations of a Phone Number (LeetCode #17).

Mirror of bench/letter_combinations.kara. Same M/N/K, generator, BFS shape,
and sink — see that file's header for the workload rationale.
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


def main() -> None:
    m_cases = 8
    k_iters = 10_000  # 10× smaller than the compiled mirrors per BENCH.md

    cases = ["", "2", "7", "23", "79", "234", "279", "2349"]

    total = 0
    for k in range(k_iters):
        idx = k % m_cases
        r = letter_combinations(cases[idx])
        total += len(r)
    print(total)


if __name__ == "__main__":
    main()
