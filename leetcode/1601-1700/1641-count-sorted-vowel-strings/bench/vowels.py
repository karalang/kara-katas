# LeetCode #1641: Count Sorted Vowel Strings -- the bench's Python mirror:
# the ★ arm on 4000000 random n from 1 to 50, all drawn first.


def count_vowel_strings(n):
    ending = [1] * 5
    for _ in range(1, n):
        for v in range(1, 5):
            ending[v] += ending[v - 1]
    return sum(ending)


seed = 1641


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    ns = [next_random() % 50 + 1 for _ in range(4000000)]
    check = 0
    total = 0
    for n in ns:
        count = count_vowel_strings(n)
        total += count
        check = (check * 31 + count) % 1000000007
    print(f"4000000 random n: counts sum to {total}, checksum {check}")


main()
