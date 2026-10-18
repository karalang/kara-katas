# LeetCode #691: Stickers to Spell Word -- bench program, Python mirror of the ★ arm.


def min_stickers(stickers, target):
    t = target.encode()
    m = len(t)
    full = (1 << m) - 1
    counts = []
    for s in stickers:
        c = [0] * 26
        for b in s.encode():
            c[b - 97] += 1
        counts.append(c)
    dp = [-1] * (full + 1)
    dp[0] = 0
    left = [0] * 26
    for mask in range(full + 1):
        if dp[mask] < 0:
            continue
        for c in counts:
            for k in range(26):
                left[k] = c[k]
            nxt = mask
            for i in range(m):
                k = t[i] - 97
                if nxt & (1 << i) == 0 and left[k] > 0:
                    left[k] -= 1
                    nxt = nxt | (1 << i)
            if nxt != mask and (dp[nxt] < 0 or dp[mask] + 1 < dp[nxt]):
                dp[nxt] = dp[mask] + 1
    return dp[full]


seed = 691


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, alphabet):
    return "".join(chr(97 + next_random() % alphabet) for _ in range(length))


def main():
    problems = 160
    total = 0
    checksum = 0
    for _ in range(problems):
        stickers = [random_word(10, 12) for _ in range(50)]
        target = random_word(15, 12)
        r = min_stickers(stickers, target)
        total += r
        checksum = (checksum * 31 + r + 2) % 1000000007
    print(f"{problems} problems of 50 stickers and a 15-letter target: {total} stickers in all, checksum {checksum}")


main()
