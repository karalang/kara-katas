# LeetCode #1753: Maximum Score From Removing Stones -- the bench
# (stones.kara in Python): a closed form.


def maximum_score(a, b, c):
    total = a + b + c
    largest = max(a, max(b, c))
    return min(total // 2, total - largest)


seed = 1753


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    high = next_random()
    return high * 32768 + next_random()


count, rounds = 2000000, 5
piles = []
for _ in range(count):
    a = wide() % 100000 + 1
    b = wide() % 100000 + 1
    c = wide() % 100000 + 1
    piles.append((a, b, c))
total = 0
check = 0
for r in range(rounds):
    for a, b, c in piles:
        answer = maximum_score(a, b, c)
        total += answer
        check = (check * 31 + answer + r) % 1000000007
print(f"{count} sets of piles, {rounds} rounds: scores add to {total}, checksum {check}")
