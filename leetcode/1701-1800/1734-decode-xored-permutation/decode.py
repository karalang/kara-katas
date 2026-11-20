# LeetCode #1734: Decode XORed Permutation -- mirrors decode.kara (the ★ arm).


def decode(encoded):
    n = len(encoded) + 1
    all_ = 0
    for v in range(1, n + 1):
        all_ ^= v
    rest = 0
    i = 1
    while i < n - 1:
        rest ^= encoded[i]
        i += 2
    perm = [all_ ^ rest]
    for code in encoded:
        perm.append(perm[-1] ^ code)
    return perm


seed = 1734


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


def batch(count, most):
    total = 0
    check = 0
    for _ in range(count):
        n = 2 * (wide() % ((most - 1) // 2)) + 3
        perm = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            j = wide() % (i + 1)
            perm[i], perm[j] = perm[j], perm[i]
        encoded = [perm[i] ^ perm[i + 1] for i in range(n - 1)]
        decoded = decode(encoded)
        if decoded != perm:
            print("wrong")
        for v in decoded:
            total += v
            check = (check * 31 + v) % 1000000007
        check = (check * 31 + n) % 1000000007
    print(f"{count} permutations of up to {most}: values sum to {total}, checksum {check}")


print(show(decode([3, 1])))
print(show(decode([6, 5, 4, 6])))
print(show(decode([1, 3])))
print(show(decode([3, 1, 7, 1, 3, 1, 15, 1])))
batch(3000, 9)
batch(300, 1001)
batch(10, 99999)
