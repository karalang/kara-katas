# LeetCode #2744: Find Maximum Number of String Pairs -- Python mirror of
# pairs.kara (the ★ arm): each word whose reverse was already seen makes
# a pair.


def maximum_number_of_string_pairs(words):
    seen = set()
    pairs = 0
    for w in words:
        if w[::-1] in seen:
            pairs += 1
        seen.add(w)
    return pairs


seed = 2744


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_words(n, k):
    words = []
    while len(words) < n:
        a = chr(97 + next_random() % k)
        b = chr(97 + next_random() % k)
        w = a + b
        if w not in words:
            words.append(w)
    return words


def main():
    print(maximum_number_of_string_pairs(["cd", "ac", "dc", "ca", "zz"]))
    print(maximum_number_of_string_pairs(["ab", "ba", "cc"]))
    print(maximum_number_of_string_pairs(["aa", "ab"]))
    print(maximum_number_of_string_pairs(["xy"]))
    both = []
    for i in range(25):
        a, b = chr(97 + i), chr(98 + i)
        both += [a + b, b + a]
    print(maximum_number_of_string_pairs(both))
    total = check = 0
    for _ in range(5000):
        k = next_random() % 26 + 1
        n = next_random() % min(k * k, 50) + 1
        pairs = maximum_number_of_string_pairs(random_words(n, k))
        total += pairs
        check = (check * 31 + pairs) % 1000000007
    print(f"5000 lists: pairs sum to {total}, checksum {check}")


main()
