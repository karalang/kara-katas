# LeetCode #2433: Find The Original Array of Prefix Xor -- the Python
# mirror of the ★ arm: every value its prefix XOR the prefix before, the
# first its own prefix.

seed = 2433


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def find_array(pref):
    arr = []
    before = 0
    for p in pref:
        arr.append(p ^ before)
        before = p
    return arr


def fold(values):
    check = 0
    for v in values:
        check = (check * 31 + v) % 1000000007
    return check


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    cases = [[5, 2, 0, 3, 1], [13], [0], [7, 7, 7, 7], [1000000, 0, 1000000, 0]]
    for pref in cases:
        print(f"{show(pref)}: {show(find_array(pref))}")
    random = []
    for _ in range(10000):
        r = next_random()
        random.append((r * 32768 + next_random()) % 1000001)
    print(f"10^4 random: checksum {fold(find_array(random))}")
    print(f"10^4 rising: checksum {fold(find_array(list(range(10000))))}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 12
        top = 1 + next_random() % 63
        pref = [next_random() % (top + 1) for _ in range(n)]
        check = (check * 31 + fold(find_array(pref))) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
