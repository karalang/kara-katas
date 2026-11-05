# LeetCode #1048: Longest String Chain -- Python mirror of
# bench/longest_chain.kara: the words sorted by length, and a dict from
# word to the longest chain ending there.

seed = 1048


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def longest_str_chain(words):
    chain = {}
    best = 0
    for w in sorted(words, key=len):
        here = 1
        for i in range(len(w)):
            pred = w[:i] + w[i + 1:]
            if pred in chain and chain[pred] + 1 > here:
                here = chain[pred] + 1
        chain[w] = here
        best = max(best, here)
    return best


def main():
    lists, count, rounds = 100, 2000, 5
    all_lists = []
    for _ in range(lists):
        words = []
        for _ in range(count):
            n = next_random() % 16 + 1
            words.append("".join(chr(ord("a") + next_random() % 3) for _ in range(n)))
        all_lists.append(words)
    total = check = 0
    for _ in range(rounds):
        for words in all_lists:
            answer = longest_str_chain(words)
            total += answer
            check = (check * 131 + answer) % 1000000007
    print(f"{lists} lists of {count} words, {rounds} rounds: total {total}, checksum {check}")


main()
