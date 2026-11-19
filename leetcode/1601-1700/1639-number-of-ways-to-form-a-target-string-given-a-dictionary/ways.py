# LeetCode #1639: Number of Ways to Form a Target String Given a
# Dictionary -- the Python mirror of the ★ arm: per column, the letters'
# counts, and ways[i] updated from the top down.

MODULUS = 1000000007


def num_ways(words, target):
    length = len(words[0])
    goal = target.encode()
    ways = [0] * (len(goal) + 1)
    ways[0] = 1
    for column in range(length):
        count = [0] * 26
        for word in words:
            count[ord(word[column]) - ord("a")] += 1
        for i in range(min(column + 1, len(goal)) - 1, -1, -1):
            have = count[goal[i] - ord("a")]
            ways[i + 1] = (ways[i + 1] + ways[i] * have) % MODULUS
    return ways[len(goal)]


# ---- the harness: the same as every arm's ---------------------------------

seed = 1639


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, letters):
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(length))


def batch(count, most, long, letters):
    check = 0
    total = 0
    for _ in range(count):
        n = next_random() % most + 1
        length = next_random() % long + 1
        words = [random_word(length, letters) for _ in range(n)]
        target = random_word(next_random() % (length + 1) + 1, letters)
        ways = num_ways(words, target)
        total += ways
        check = (check * 31 + ways + 1) % 1000000007
    print(f"{count} dictionaries of up to {most} words: ways sum to {total}, checksum {check}")


print(num_ways(["acca", "bbbb", "caca"], "aba"))
print(num_ways(["abba", "baab"], "bab"))
print(num_ways(["ab", "ba"], "aba"))
print(num_ways(["abc", "abc"], "ad"))
print(num_ways(["xyz"], "xyz"))
batch(3000, 4, 5, 2)
batch(100, 50, 60, 3)
batch(3, 1000, 1000, 26)
