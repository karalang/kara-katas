# LeetCode #1639: Number of Ways to Form a Target String Given a
# Dictionary -- the bench's Python mirror: the ★ arm on 40 random
# dictionaries of 1000 words of 1000 letters and targets of 500 letters,
# all over the letters a to e and drawn first.

MODULUS = 1000000007


def num_ways(words, target):
    length = len(words[0])
    goal = target.encode()
    ways = [0] * (len(goal) + 1)
    ways[0] = 1
    for column in range(length):
        count = [0] * 26
        for word in words:
            count[word[column] - 97] += 1
        for i in range(min(column + 1, len(goal)) - 1, -1, -1):
            have = count[goal[i] - 97]
            ways[i + 1] = (ways[i + 1] + ways[i] * have) % MODULUS
    return ways[len(goal)]


seed = 1639


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length):
    return bytes(97 + next_random() % 5 for _ in range(length))


def main():
    cases = []
    for _ in range(40):
        words = [random_word(1000) for _ in range(1000)]
        target = random_word(500).decode()
        cases.append((words, target))
    check = 0
    for words, target in cases:
        ways = num_ways(words, target)
        check = (check * 31 + ways + 1) % 1000000007
    print(f"40 dictionaries of 1000 words: checksum {check}")


main()
