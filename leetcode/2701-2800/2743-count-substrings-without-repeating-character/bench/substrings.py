# LeetCode #2743: Count Substrings Without Repeating Character -- the
# bench (substrings.kara in Python): a window with each letter's last
# place.


def number_of_special_substrings(s):
    last = [-1] * 26
    start = count = 0
    for i, b in enumerate(s):
        letter = b - 97
        start = max(start, last[letter] + 1)
        last[letter] = i
        count += i - start + 1
    return count


def main():
    count, n, rounds = 20, 100000, 300
    seed = 2743
    words = []
    for _ in range(count):
        seed = (seed * 1103515245 + 12345) % 2147483648
        k = seed // 65536 % 22 + 5
        out = bytearray()
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            out.append(97 + seed // 65536 % k)
        words.append(bytes(out))
    total = check = 0
    for r in range(rounds):
        for s in words:
            found = number_of_special_substrings(s)
            total += found
            check = (check * 31 + found + r) % 1000000007
    print(f"{count} words of {n} letters, {rounds} rounds: counts sum to {total}, checksum {check}")


main()
