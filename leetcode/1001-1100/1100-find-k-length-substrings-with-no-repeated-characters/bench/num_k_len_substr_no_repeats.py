# Benchmark: LeetCode #1100 Find K-Length Substrings With No Repeated
# Characters -- the sliding window with a count of each letter, as the
# Kāra ★ arm. Mirrors num_k_len_substr_no_repeats.kara.


def num_k_len_substr_no_repeats(s, k):
    b = s.encode()
    if k > 26 or k > len(b):
        return 0
    count = [0] * 26
    repeated = 0
    found = 0
    for i in range(len(b)):
        c = b[i] - 97
        count[c] += 1
        if count[c] == 2:
            repeated += 1
        if i >= k:
            out = b[i - k] - 97
            count[out] -= 1
            if count[out] == 1:
                repeated -= 1
        if i >= k - 1 and repeated == 0:
            found += 1
    return found


def main():
    seed = 1100

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    texts = []
    for j in range(64):
        alphabet = 8 + j % 19
        texts.append([chr(97 + next_random() % alphabet) for _ in range(10000)])
    total = 0
    check = 0
    for rnd in range(10):
        for j in range(len(texts)):
            at = (rnd * 7919 + j * 104729) % 10000
            texts[j][at] = chr(97 + (rnd + j) % 26)
            s = "".join(texts[j])
            for q in range(4):
                k = (rnd * 7 + j * 3 + q * 11) % 30 + 1
                count = num_k_len_substr_no_repeats(s, k)
                total += count
                check = (check * 31 + count + 1) % 1000000007
    print(f"10 rounds over 64 texts of 10^4 letters: {total} substrings, checksum {check}")


main()
