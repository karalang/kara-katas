# Benchmark for #557: Python mirror of the ★ arm (split, reverse, join);
# see reverse_words_in_a_string_iii.kara.

seed = 557


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def reverse_words(s):
    return " ".join(w[::-1] for w in s.split(" "))


def main():
    count = 100
    texts = []
    words = 0
    for _ in range(count):
        parts = []
        size = 0
        while size < 49980:
            if size > 0:
                size += 1
            length = 1 + next_random() % 12
            parts.append("".join(chr(33 + next_random() % 94) for _ in range(length)))
            size += length
            words += 1
        texts.append(" ".join(parts))
    checksum = 0
    for rnd in range(50):
        for g in range(count):
            b = reverse_words(texts[(rnd * 7 + g) % count]).encode()
            checksum = (checksum * 31 + len(b) + b[0] * 7 + b[len(b) // 2]) % 1000000007
    print(f"{count} texts, {words} words, 50 rounds each: checksum {checksum}")


main()
