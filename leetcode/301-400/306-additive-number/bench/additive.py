"""LeetCode 306 - Additive Number.

Mirror of additive.kara: the same O(n^3) scan over the same flat digit array,
with the same planted positives, perturbation and masked sink. Kept
algorithm-for-algorithm so the benchmark lane is honest.
"""


CASES = 220
WIDTH = 18
PASSES = 90
MASK = 1073741823
PLANTED = ["022461016264268110", "020204060100160260", "021214263105168273", "022224466110176286", "023234669115184299", "024244872120192312", "025255075125200325", "026265278130208338"]


def add_digits(a, b):
    rev = []
    i, j, carry = len(a) - 1, len(b) - 1, 0
    while i >= 0 or j >= 0 or carry > 0:
        s = carry
        if i >= 0:
            s += a[i]; i -= 1
        if j >= 0:
            s += b[j]; j -= 1
        rev.append(s % 10)
        carry = s // 10
    return rev[::-1]


def matches_at(flat, base, n, pos, num):
    if pos + len(num) > n:
        return False
    for k in range(len(num)):
        if flat[base + pos + k] != num[k]:
            return False
    return True


def no_lead_zero(flat, base, lo, hi):
    return hi - lo == 1 or flat[base + lo] != 0


def is_additive(flat, base, n):
    if n < 3:
        return False
    for len1 in range(1, n - 1):
        if not no_lead_zero(flat, base, 0, len1):
            break
        for len2 in range(1, n - len1):
            if not no_lead_zero(flat, base, len1, len1 + len2):
                break
            a = flat[base:base + len1]
            b = flat[base + len1:base + len1 + len2]
            pos, ok, steps = len1 + len2, True, 0
            while pos < n and ok:
                c = add_digits(a, b)
                if matches_at(flat, base, n, pos, c):
                    pos += len(c)
                    a, b = b, c
                    steps += 1
                else:
                    ok = False
            if ok and pos == n and steps > 0:
                return True
    return False


def main():
    flat = []
    seed = 7
    for c in range(CASES):
        if c % 25 == 0:
            p = PLANTED[(c // 25) % len(PLANTED)]
            for i in range(WIDTH):
                flat.append(ord(p[i]) - 48)
        else:
            for _ in range(WIDTH):
                seed = (seed * 1103515245 + 12345) % 2147483647
                flat.append(seed % 10)

    checksum = 1
    for p in range(PASSES):
        site = (checksum * 31 + p * 7919) % (CASES * WIDTH)
        flat[site] = (flat[site] + 1) % 10
        hits = 0
        for c in range(CASES):
            if is_additive(flat, c * WIDTH, WIDTH):
                hits += 1
        checksum = (checksum * 131 + hits * 7919 + site) & MASK
    print("checksum", checksum)


if __name__ == "__main__":
    main()
