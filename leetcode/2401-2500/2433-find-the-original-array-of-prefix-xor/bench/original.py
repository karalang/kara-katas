# LeetCode #2433: Find The Original Array of Prefix Xor -- the bench, the
# ★ arm: every value its prefix XOR the prefix before, the first its own
# prefix, gathered into a new list.


def find_array(pref):
    arr = []
    before = 0
    for p in pref:
        arr.append(p ^ before)
        before = p
    return arr


seed = 2433


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    pref = []
    for _ in range(100000):
        r = next_random()
        pref.append((r * 32768 + next_random()) % 1000001)
    check = 0
    for p in range(1000):
        pref[(p * 7919) % 100000] = p
        arr = find_array(pref)
        for v in arr:
            check = (check * 31 + v) % 1000000007
    print(f"1000 passes over 10^5 prefixes: checksum {check}")


main()
