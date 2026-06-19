"""LeetCode #44 bench mirror — Python, the greedy two-pointer matcher (★).

Mirrors bench/wildcard_matching.kara: one cursor in each of s and p, with star/matched
scalars for O(1) backtracking. Build s and a multi-star pattern p once, punch one s slot per
iteration, fold the boolean into a rolling checksum. Same workload + sink as every other
mirror. The slow interpreted baseline (long-workload lane).
"""


def is_match(s: bytes, p: bytes, n: int, m: int) -> bool:
    i = j = 0
    star = -1
    matched = 0
    while i < n:
        if j < m and (p[j] == 0x3F or p[j] == s[i]):  # '?'
            i += 1
            j += 1
        elif j < m and p[j] == 0x2A:  # '*'
            star = j
            matched = i
            j += 1
        elif star != -1:
            matched += 1
            i = matched
            j = star + 1
        else:
            return False
    while j < m and p[j] == 0x2A:
        j += 1
    return j == m


def main() -> None:
    total = 300000
    modulus = 1000000007
    n = 240

    s = bytearray((ord("a") + (a % 3)) for a in range(n))
    p = bytearray()
    for _ in range(8):
        p += b"*abc"
    p += b"*"
    m = len(p)

    acc = 0
    for k in range(total):
        s[k % n] = ord("a") + (k % 4)
        bit = 1 if is_match(s, p, n, m) else 0
        acc = (acc * 131 + bit) % modulus

    print(acc)


if __name__ == "__main__":
    main()
