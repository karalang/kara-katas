# LeetCode #1663 bench: the ★ arm, from the back.
#
# 400 problems with n = 10^5, LeetCode's largest, and k drawn from n to
# 26n, all drawn first; then each string is built and every letter of it
# folded into a checksum.


def get_smallest_string(n, k):
    letters = bytearray(b"a" * n)
    left = k - n
    i = n - 1
    while left > 0:
        more = min(left, 25)
        letters[i] += more
        left -= more
        i -= 1
    return letters.decode()


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    count = 400
    n = 100000
    seed = 1663
    ks = []
    for _ in range(count):
        r = next_random() * 32768
        r += next_random()
        ks.append(n + r % (25 * n + 1))
    zs = 0
    check = 0
    for k in ks:
        for b in get_smallest_string(n, k).encode():
            if b == 122:
                zs += 1
            check = (check * 31 + b) % 1000000007
    print(f"{count} problems with n = {n}: {zs} z's, checksum {check}")


main()
