# Benchmark workload — Longest Common Prefix (LeetCode #14).
# Python mirror of bench/vertical.kara. K=100k (10x scaled-down vs the
# compiled mirrors); the README quotes the projected K=1M time so the
# comparison stays in scale.


def nth_letter(n: int) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return alphabet[n % 26]


def make_string(prefix_len: int, suffix_id: int) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    out = []
    for i in range(prefix_len):
        out.append(alphabet[i])
    sig = nth_letter(suffix_id)
    for _ in range(6):
        out.append(sig)
    return "".join(out)


def build_case(prefix_len: int, count: int) -> list[str]:
    return [make_string(prefix_len, s) for s in range(count)]


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
        stop = False
        while s < n:
            other = strs[s]
            if col >= len(other) or other[col] != c:
                stop = True
                break
            s += 1
        if stop:
            break
        col += 1
    return first[:col]


def main() -> None:
    m_cases = 8
    n_strings = 16
    k_iters = 100_000
    prefixes = [0, 2, 4, 7, 10, 13, 16, 20]

    sets = [build_case(prefixes[m], n_strings) for m in range(m_cases)]

    total = 0
    for k in range(k_iters):
        idx = k % m_cases
        r = longest_common_prefix(sets[idx])
        total += len(r)
    print(total)


if __name__ == "__main__":
    main()
