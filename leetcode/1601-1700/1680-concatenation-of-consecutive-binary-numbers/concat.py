# LeetCode #1680: Concatenation of Consecutive Binary Numbers -- the Python
# mirror of the ★ arm: one running value.


def concatenated_binary(n):
    modulus = 1000000007
    value = 0
    bits = 0
    for i in range(1, n + 1):
        if i & (i - 1) == 0:
            bits += 1
        value = ((value << bits) + i) % modulus
    return value


seed = 1680


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most):
    total = 0
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        answer = concatenated_binary(n)
        total += answer
        check = (check * 31 + answer + n) % 1000000007
    print(f"{count} values of n up to {most}: answers sum to {total}, checksum {check}")


print(concatenated_binary(1))
print(concatenated_binary(3))
print(concatenated_binary(12))
print(concatenated_binary(11))
print(concatenated_binary(100000))
batch(3000, 100)
batch(300, 10000)
batch(10, 100000)
