# LeetCode #1316: Distinct Echo Substrings -- Python mirror of the ★ Kāra
# arm: how far the suffixes from every two places agree, in a table filled
# from the back; a piece of length 2h from i is an echo when the suffixes
# from i and i + h agree for h letters, and it is counted at the first
# place it starts. O(n^2) time and space, no set.


def distinct_echo_substrings(text):
    s = text.encode()
    n = len(s)
    agree = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        row, below = agree[i], agree[i + 1]
        for j in range(n - 1, i, -1):
            if s[i] == s[j]:
                row[j] = below[j + 1] + 1
    earlier = [0] * n
    for i in range(n):
        row = agree[i]
        for j in range(i + 1, n):
            if row[j] > earlier[j]:
                earlier[j] = row[j]
    count = 0
    for i in range(n):
        for h in range(1, (n - i) // 2 + 1):
            if agree[i][i + h] >= h and 2 * h > earlier[i]:
                count += 1
    return count


def next_random(seed):
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed, seed // 65536


def main():
    ask = distinct_echo_substrings
    print(f"{ask('abcabcabc')} {ask('leetcodeleetcode')} {ask('a')} {ask('aaaa')} {ask('ababxabab')} {ask('a' * 300)}")
    letters = "abcdefghijklmnopqrstuvwxyz"
    seed = 1316
    total = 0
    check = 0
    for t in range(400):
        seed, r = next_random(seed)
        n = 1 + r % 300
        k = 1 if t % 4 == 0 else 2 if t % 4 == 1 else 3 if t % 4 == 2 else 26
        chars = []
        if t % 2 == 0:
            seed, r = next_random(seed)
            b = 1 + r % 6
            block = []
            for _ in range(b):
                seed, r = next_random(seed)
                block.append(letters[r % 26])
            for i in range(n):
                chars.append(block[i % b])
            seed, r = next_random(seed)
            changes = r % 4
            for _ in range(changes):
                seed, r = next_random(seed)
                at = r % n
                seed, r = next_random(seed)
                chars[at] = letters[r % 26]
        else:
            for _ in range(n):
                seed, r = next_random(seed)
                chars.append(letters[r % k])
        got = distinct_echo_substrings("".join(chars))
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"400 random strings: echoes total {total}, checksum {check}")


main()
