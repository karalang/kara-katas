# LeetCode #1297: Maximum Number of Occurrences of a Substring -- Python
# mirror of the ★ arm: one window of minSize letters slid along the string,
# each with few enough distinct letters counted by its text.


def max_freq(s, max_letters, min_size, max_size):
    n = len(s)
    letters = [0] * 26
    distinct = 0
    seen = {}
    best = 0
    for i in range(n):
        add = ord(s[i]) - 97
        if letters[add] == 0:
            distinct += 1
        letters[add] += 1
        if i >= min_size:
            gone = ord(s[i - min_size]) - 97
            letters[gone] -= 1
            if letters[gone] == 0:
                distinct -= 1
        if i + 1 >= min_size and distinct <= max_letters:
            window = s[i + 1 - min_size:i + 1]
            times = seen.get(window, 0) + 1
            seen[window] = times
            best = max(best, times)
    return best


def main():
    seed = 1297

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    print(f"{max_freq('aababcaab', 2, 3, 4)} {max_freq('aaaa', 1, 3, 3)} {max_freq('abcde', 5, 5, 5)} {max_freq('abcde', 1, 2, 3)} {max_freq('zzzzzzzzzz', 1, 1, 10)}")
    total = 0
    check = 0
    for _ in range(200):
        length = 1 + next_random() % 600
        alphabet = 2 + next_random() % 25
        s = "".join(chr(97 + next_random() % alphabet) for _ in range(length))
        top = min(length, 26)
        min_size = 1 + next_random() % min(top, 6)
        max_size = min_size + next_random() % (top - min_size + 1)
        max_letters = 1 + next_random() % 26
        best = max_freq(s, max_letters, min_size, max_size)
        total += best
        check = (check * 131 + best) % 1000000007
    print(f"200 random strings: occurrences total {total}, checksum {check}")


main()
