# LeetCode #629: K Inverse Pairs Array -- Python mirror of the ★ arm.
#
# Rolling DP over n, each row a sliding-window sum of the previous one.


def k_inverse_pairs(n, k):
    modulus = 1000000007
    row = [0] * (k + 1)
    row[0] = 1
    for i in range(2, n + 1):
        nxt = [0] * (k + 1)
        window = 0
        for j in range(k + 1):
            window = (window + row[j]) % modulus
            if j >= i:
                window = (window - row[j - i] + modulus) % modulus
            nxt[j] = window
        row = nxt
    return row[k]


seed = 629


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(n, k):
    print(f"n = {n}, k = {k} -> {k_inverse_pairs(n, k)}")


def main():
    show(3, 0)
    show(3, 1)
    show(1, 0)
    show(1, 1)
    show(2, 1)
    show(3, 3)
    show(3, 4)
    show(4, 2)
    show(5, 5)
    show(10, 20)
    show(20, 190)
    show(1000, 0)
    show(1000, 1)
    show(1000, 1000)
    total = 0
    checksum = 0
    for _ in range(200):
        n = 1 + next_random() % 60
        k = next_random() % 301
        c = k_inverse_pairs(n, k)
        total += c
        checksum = (checksum * 31 + c) % 1000000007
    print(f"200 random cases: total {total}, checksum {checksum}")
    every = 0
    for k in range(436):
        every = (every + k_inverse_pairs(30, k)) % 1000000007
    print(f"n = 30, every k: {every}")


main()
