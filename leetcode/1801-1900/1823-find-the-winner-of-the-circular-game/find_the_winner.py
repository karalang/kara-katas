# LeetCode #1823: Find the Winner of the Circular Game -- the ★ arm in Python


def find_the_winner(n, k):
    winner = 0
    for i in range(2, n + 1):
        winner = (winner + k) % i
    return winner + 1


seed = 1823


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


f = find_the_winner
print(f(5, 2), f(6, 5))
print(f(1, 1), f(7, 1), f(2, 2), f(7, 7))
print(f"the most: {f(500, 500)} {f(500, 1)} {f(500, 2)}")
check = 0
for _ in range(3000):
    n = 1 + next_random() % 40
    k = 1 + next_random() % n
    check = (check * 41 + f(n, k)) % 1000000007
print(f"3000 random circles: checksum {check}")
