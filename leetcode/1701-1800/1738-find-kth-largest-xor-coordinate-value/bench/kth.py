# LeetCode #1738: Find Kth Largest XOR Coordinate Value -- the bench
# (kth.kara): a prefix XOR table, then a sort.


def kth_largest_value(matrix, k):
    m, n = len(matrix), len(matrix[0])
    prefix = [[0] * (n + 1) for _ in range(m + 1)]
    values = []
    for i in range(m):
        for j in range(n):
            prefix[i + 1][j + 1] = prefix[i][j + 1] ^ prefix[i + 1][j] ^ prefix[i][j] ^ matrix[i][j]
            values.append(prefix[i + 1][j + 1])
    values.sort()
    return values[len(values) - k]


seed = 1738


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


count = 4
rounds = 5
side = 1000
problems = []
for _ in range(count):
    matrix = [[wide() % 1000001 for _ in range(side)] for _ in range(side)]
    k = wide() % (side * side) + 1
    problems.append((matrix, k))
total = 0
check = 0
for r in range(rounds):
    for matrix, k in problems:
        answer = kth_largest_value(matrix, k)
        total += answer
        check = (check * 31 + answer + k + r) % 1000000007
print(f"{count} matrices of {side} by {side}, {rounds} rounds: answers sum to {total}, checksum {check}")
