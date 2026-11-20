# LeetCode #1663: Smallest String With A Given Numeric Value -- the
# Python mirror of the ★ arm (from the back).


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


# ---- the harness: the same in every arm --------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, longest):
    zs = 0
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % longest + 1
        k = n + (next_random() * 32768 + next_random()) % (25 * n + 1)
        for b in get_smallest_string(n, k).encode():
            if b == ord("z"):
                zs += 1
            check = (check * 31 + b) % 1000000007
    print(f"{count} problems with n up to {longest}: {zs} z's, checksum {check}")


print(get_smallest_string(3, 27))
print(get_smallest_string(5, 73))
print(get_smallest_string(1, 1))
print(get_smallest_string(1, 26))
print(get_smallest_string(4, 104))
print(get_smallest_string(6, 30))
seed = 1663
batch(3000, 10)
batch(300, 1000)
batch(10, 100000)
