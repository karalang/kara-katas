# LeetCode #2744: Find Maximum Number of String Pairs -- the bench
# (pairs.kara in Python): a set of the words seen.


def maximum_number_of_string_pairs(words):
    seen = set()
    pairs = 0
    for w in words:
        if w[::-1] in seen:
            pairs += 1
        seen.add(w)
    return pairs


def main():
    count, rounds = 20000, 10
    seed = 2744
    lists = []
    for _ in range(count):
        words = []
        while len(words) < 50:
            seed = (seed * 1103515245 + 12345) % 2147483648
            a = chr(97 + seed // 65536 % 8)
            seed = (seed * 1103515245 + 12345) % 2147483648
            b = chr(97 + seed // 65536 % 8)
            if a + b not in words:
                words.append(a + b)
        lists.append(words)
    total = check = 0
    for r in range(rounds):
        for words in lists:
            pairs = maximum_number_of_string_pairs(words)
            total += pairs
            check = (check * 31 + pairs + r) % 1000000007
    print(f"{count} lists of 50 words, {rounds} rounds: pairs sum to {total}, checksum {check}")


main()
