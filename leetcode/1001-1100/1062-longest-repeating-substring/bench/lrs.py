# LeetCode #1062: Longest Repeating Substring -- the benchmark, the same
# binary search and rolling hash as lrs.kara.

MOD = 1000000007
BASE = 131


# Whether two starts in `s` hold the same `length` bytes.
def twice(s, length):
    if length == 0:
        return True
    top = 1
    for _ in range(1, length):
        top = top * BASE % MOD
    h = 0
    seen = {}
    for i in range(len(s)):
        if i >= length:
            h = (h - s[i - length] * top % MOD + MOD) % MOD
        h = (h * BASE + s[i]) % MOD
        if i + 1 >= length:
            start = i + 1 - length
            starts = seen.setdefault(h, [])
            for other in starts:
                if s[other:other + length] == s[start:start + length]:
                    return True
            starts.append(start)
    return False


def longest_repeating(s):
    b = s.encode()
    # twice(lo) and not twice(hi)
    lo, hi = 0, len(b)
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2
        if twice(b, mid):
            lo = mid
        else:
            hi = mid
    return lo


seed = 1062


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, k):
    return "".join(chr(ord("a") + next_random() % k) for _ in range(n))


def main():
    # 60 strings of 20000 letters over 2 to 26 of them, built once, then
    # each answered
    words = [random_word(20000, 2 + w % 25) for w in range(60)]
    calls = total = check = 0
    for w in words:
        answer = longest_repeating(w)
        total += answer
        check = (check * 31 + answer) % 1000000007
        calls += 1
    print(f"{calls} calls: answers sum {total}, checksum {check}")


main()
