# LeetCode #1147: Longest Chunked Palindrome Decomposition -- the Python
# mirror of the ★ arm: from both ends at once, the shortest chunk at the
# front that equals the chunk at the back is taken off both, two chunks;
# what is left in the middle, if anything, is one more.


def longest_decomposition(text):
    i, j, k = 0, len(text), 0
    while i < j:
        size = 1
        while 2 * size <= j - i and text[i:i + size] != text[j - size:j]:
            size += 1
        if 2 * size > j - i:
            return k + 1
        k += 2
        i += size
        j -= size
    return k


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(size, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(size))


def chunked(count, letters):
    # `count` chunks of 1 to 3 letters, then the same chunks in the
    # reverse order, with a middle of 0 to 3 letters between
    chunks = [word(1 + next_random() % 3, letters) for _ in range(count)]
    middle = word(next_random() % 4, letters)
    return "".join(chunks) + middle + "".join(reversed(chunks))


def main():
    global seed
    for text in ["ghiabcdefhelloadamhelloabcdefghi", "merchant", "antaprezatepzapreanta",
                 "a", "aa", "ab", "aba", "abab", "ababa", "elvtoelvto"]:
        print(f"{text} -> {longest_decomposition(text)}")
    seed = 1147
    total = check = 0
    for t in range(2000):
        letters = [1, 2, 3, 26][next_random() % 4]
        if t % 2 == 0:
            text = word(1 + next_random() % 60, letters)
        else:
            text = chunked(1 + next_random() % 10, letters)
        k = longest_decomposition(text)
        total += k
        check = (check * 31 + k + len(text)) % 1000000007
    print(f"2000 random texts: chunks total {total}, checksum {check}")
    print(f"1000 a's: {longest_decomposition('a' * 1000)}")
    print(f"ab 500 times: {longest_decomposition('ab' * 500)}")
    print(f"999 a's and a b: {longest_decomposition('a' * 999 + 'b')}")
    big = chunked(240, 2)
    print(f"240 chunks of 1 to 3 letters mirrored, {len(big)} letters: {longest_decomposition(big)}")


main()
