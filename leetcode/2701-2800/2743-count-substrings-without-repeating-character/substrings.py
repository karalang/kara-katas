# LeetCode #2743: Count Substrings Without Repeating Character -- Python
# mirror of substrings.kara (the ★ arm): a window with each letter's last
# place, each i adding the window's length.


def number_of_special_substrings(s):
    last = [-1] * 26
    start = count = 0
    for i, ch in enumerate(s):
        letter = ord(ch) - ord("a")
        start = max(start, last[letter] + 1)
        last[letter] = i
        count += i - start + 1
    return count


seed = 2743


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, k):
    return "".join(chr(ord("a") + next_random() % k) for _ in range(n))


def main():
    print(number_of_special_substrings("abcd"))
    print(number_of_special_substrings("ooo"))
    print(number_of_special_substrings("a"))
    print(number_of_special_substrings("abab"))
    print(number_of_special_substrings("abcdefghijklmnopqrstuvwxyz"))
    total = check = 0
    for c in range(2020):
        if c < 2000:
            n = next_random() % 30 + 1
            k = next_random() % 26 + 1
        else:
            n, k = 100000, next_random() % 26 + 1
        count = number_of_special_substrings(random_word(n, k))
        total += count
        check = (check * 31 + count) % 1000000007
        if c == 1999:
            print(f"2000 small words: counts sum to {total}, checksum {check}")
            total = check = 0
    print(f"20 words of 100000 letters: counts sum to {total}, checksum {check}")


main()
