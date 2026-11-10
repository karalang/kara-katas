# LeetCode #1100: Find K-Length Substrings With No Repeated Characters --
# Python mirror of the ★ arm: a sliding window of k letters with a count
# of each letter and of the letters repeated in it. Same cases and output
# as num_k_len_substr_no_repeats.kara.


def num_k_len_substr_no_repeats(s, k):
    b = s.encode()
    if k > 26 or k > len(b):
        return 0
    count = [0] * 26
    repeated = 0
    found = 0
    for i in range(len(b)):
        c = b[i] - ord("a")
        count[c] += 1
        if count[c] == 2:
            repeated += 1
        if i >= k:
            out = b[i - k] - ord("a")
            count[out] -= 1
            if count[out] == 1:
                repeated -= 1
        if i >= k - 1 and repeated == 0:
            found += 1
    return found


seed = 1100


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, alphabet):
    return "".join(chr(ord("a") + next_random() % alphabet) for _ in range(n))


def main():
    cases = [
        ("havefunonleetcode", 5),
        ("home", 5),
        ("a", 1),
        ("aaaa", 1),
        ("aaaa", 2),
        ("abcabc", 3),
        ("abcabc", 4),
        ("abcdefghijklmnopqrstuvwxyz", 26),
        ("abcdefghijklmnopqrstuvwxyza", 27),
        ("abab", 2),
        ("leetcode", 8),
        ("zyxwvutsrqponmlkjihgfedcbaz", 26),
    ]
    for s, k in cases:
        print(num_k_len_substr_no_repeats(s, k))
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 200 + 1
        alphabet = next_random() % 26 + 1
        text = random_text(n, alphabet)
        k = next_random() % 30 + 1
        count = num_k_len_substr_no_repeats(text, k)
        total += count
        check = (check * 31 + count + 1) % 1000000007
    print(f"2000 random texts: {total} substrings, checksum {check}")
    text = random_text(10000, 26)
    counts = [str(num_k_len_substr_no_repeats(text, k)) for k in range(1, 28)]
    print(f"10^4 letters, k from 1 to 27: {' '.join(counts)}")
    print(f"10^4 letters, k = 10^4: {num_k_len_substr_no_repeats(text, 10000)}")


main()
