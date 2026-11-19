# LeetCode #1652: Defuse the Bomb -- the Python mirror of the ★ arm: a
# window of |k| numbers sliding once round the circle.


def decrypt(code, k):
    n = len(code)
    answer = [0] * n
    if k == 0:
        return answer
    start, end = (1, k) if k > 0 else (n + k, n - 1)
    total = 0
    for j in range(start, end + 1):
        total += code[j % n]
    for i in range(n):
        answer[i] = total
        total -= code[start % n]
        start += 1
        end += 1
        total += code[end % n]
    return answer


# ---- the harness: the same as every arm's ---------------------------------

seed = 1652


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def batch(count, most):
    check = 0
    total = 0
    for _ in range(count):
        n = next_random() % most + 1
        code = [next_random() % 100 + 1 for _ in range(n)]
        k = next_random() % (2 * n - 1) - (n - 1)
        for x in decrypt(code, k):
            total += x
            check = (check * 31 + x + 1) % 1000000007
    print(f"{count} codes of up to {most} numbers: answers sum to {total}, checksum {check}")


print(show(decrypt([5, 7, 1, 4], 3)))
print(show(decrypt([1, 2, 3, 4], 0)))
print(show(decrypt([2, 4, 9, 3], -2)))
print(show(decrypt([42], 0)))
print(show(decrypt([1, 2, 3, 4, 5], 4)))
print(show(decrypt([1, 2, 3, 4, 5], -4)))
batch(3000, 8)
batch(3000, 100)
