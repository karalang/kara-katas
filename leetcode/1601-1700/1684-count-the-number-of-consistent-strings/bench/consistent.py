# LeetCode #1684: Count the Number of Consistent Strings -- the bench's
# Python mirror: the ★ arm on 100 random problems of 10000 words, all
# drawn first, each answered 20 times.


def count_consistent(allowed, words):
    ok = [False] * 26
    for b in allowed.encode():
        ok[b - 97] = True
    count = 0
    for word in words:
        if all(ok[b - 97] for b in word.encode()):
            count += 1
    return count


seed = 1684


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, size, rounds = 100, 10000, 20
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    problems = []
    for _ in range(count):
        allowed = "".join(c for c in alphabet if next_random() % 8 != 0) or "a"
        words = []
        for _ in range(size):
            length = next_random() % 10 + 1
            words.append("".join(alphabet[next_random() % 26] for _ in range(length)))
        problems.append((allowed, words))
    total = 0
    check = 0
    for r in range(rounds):
        for allowed, words in problems:
            answer = count_consistent(allowed, words)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} problems of {size} words, {rounds} rounds: {total} consistent, checksum {check}")


main()
