# LeetCode #1400 bench -- Python: at least k letters, and at most k
# letters that appear an odd number of times, the letters counted in a
# list of 26.


def can_construct(s, k):
    if len(s) < k:
        return False
    count = [0] * 26
    for b in s.encode():
        count[b - 97] += 1
    odd = sum(1 for c in count if c % 2 == 1)
    return odd <= k


def main():
    n = 100000
    seed = 1400

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    letters = bytearray(97 + next_random() % 26 for _ in range(n))
    check = 0
    for _ in range(3000):
        seed = (seed + check) % 2147483648
        at = next_random() % n
        letters[at] = 97 + next_random() % 26
        k = 1 + next_random() % 30
        got = can_construct(letters.decode(), k)
        check = (check * 131 + (k if got else 0) + at) % 1000000007
    print(f"3000 rounds over 10^5 letters: checksum {check}")


main()
