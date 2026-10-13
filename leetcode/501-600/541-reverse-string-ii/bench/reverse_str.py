# Benchmark for #541: Python mirror of the ★ arm (two pointers over the
# characters); see reverse_str.kara.


def reverse_str(s, k):
    chars = list(s)
    n = len(chars)
    start = 0
    while start < n:
        i, j = start, min(start + k, n) - 1
        while i < j:
            chars[i], chars[j] = chars[j], chars[i]
            i += 1
            j -= 1
        start += 2 * k
    return "".join(chars)


seed = 541


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 200 random words of 10,000 letters (the problem's longest) built
    # once. Then 100 times over every word is answered with a k from 1
    # to 500 picked by the round and the word, and one letter of the
    # answer, picked the same way, goes into the checksum.
    words = 200
    all_words = ["".join(chr(97 + next_random() % 26) for _ in range(10000)) for _ in range(words)]
    total = 0
    checksum = 0
    for r in range(100):
        for t in range(words):
            k = 1 + (r * 37 + t * 11) % 500
            answer = reverse_str(all_words[t], k)
            letter = ord(answer[(r * 7 + t * 13) % 10000])
            total += len(answer)
            checksum = (checksum * 31 + letter) % 1000000007
    print(f"{words} words, 100 times each: {total} letters, checksum {checksum}")


main()
