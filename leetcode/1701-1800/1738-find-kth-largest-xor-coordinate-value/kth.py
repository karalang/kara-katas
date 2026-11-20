# LeetCode #1738: Find Kth Largest XOR Coordinate Value -- mirrors kth.kara
# (the ★ arm).


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


def batch(count, most, top):
    total = 0
    check = 0
    for _ in range(count):
        m = next_random() % most + 1
        n = next_random() % most + 1
        matrix = [[wide() % top for _ in range(n)] for _ in range(m)]
        k = wide() % (m * n) + 1
        answer = kth_largest_value(matrix, k)
        total += answer
        check = (check * 31 + answer + k) % 1000000007
    print(f"{count} matrices of up to {most} by {most} values below {top}: answers sum to {total}, checksum {check}")


print(kth_largest_value([[5, 2], [1, 6]], 1))
print(kth_largest_value([[5, 2], [1, 6]], 2))
print(kth_largest_value([[5, 2], [1, 6]], 3))
print(kth_largest_value([[0]], 1))
print(kth_largest_value([[1000000, 1000000], [1000000, 0]], 4))
print(kth_largest_value([[1000000, 1], [2, 3]], 1))
batch(3000, 4, 8)
batch(300, 40, 1000001)
batch(3, 1000, 1000001)
