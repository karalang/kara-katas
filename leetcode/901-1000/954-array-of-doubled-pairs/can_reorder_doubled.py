# LeetCode #954: Array of Doubled Pairs -- counts, smallest first.
#
# Count every value, then take the values in order of their size, the
# smallest absolute value first. The one taken can only be the smaller of
# its pair, since its half would have been taken already, so all its
# copies need a double: a value's double is 2x for a positive x and for
# a negative one alike. Zeros pair with zeros. O(n log n).


def can_reorder_doubled(arr):
    count = {}
    for x in arr:
        count[x] = count.get(x, 0) + 1
    values = sorted(count, key=abs)
    for x in values:
        c = count.get(x, 0)
        if c == 0:
            continue
        if x == 0:
            if c % 2 != 0:
                return False
            continue
        d = count.get(2 * x, 0)
        if d < c:
            return False
        count[2 * x] = d - c
    return True


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_case(seed, n, top):
    out = []
    for _ in range(n // 2):
        if next_random(seed) % 4 != 0:
            x = next_random(seed) % (top + 1) - top // 2
            out.append(x)
            out.append(2 * x)
        else:
            out.append(next_random(seed) % (2 * top + 1) - top)
            out.append(next_random(seed) % (2 * top + 1) - top)
    for i in range(len(out)):
        j = i + next_random(seed) % (len(out) - i)
        out[i], out[j] = out[j], out[i]
    return out


def show(arr):
    return "[" + ",".join(str(x) for x in arr) + "]"


def b(v):
    return "true" if v else "false"


def main():
    cases = [
        [3, 1, 3, 6],
        [2, 1, 2, 6],
        [4, -2, 2, -4],
        [0, 0],
        [0, 0, 0, 1],
        [2, -4],
        [-5, -10],
        [1, 2, 4, 16, 8, 4],
        [2, 4, 0, 0, 8, 1],
        [-8, -4, -2, -1],
        [1, 1, 2, 2],
        [-1, -2, 2, 4],
        [2, -2, -4, 4],
    ]
    for arr in cases:
        print(f"{show(arr)}: {b(can_reorder_doubled(list(arr)))}")
    seed = [954]
    count = 0
    yes = 0
    check = 0
    for _ in range(300):
        n = 2 + 2 * (next_random(seed) % 6)
        arr = random_case(seed, n, 40)
        ok = can_reorder_doubled(arr)
        count += n
        if ok:
            yes += 1
        check = (check * 31 + (1 if ok else 2)) % 1000000007
    print(f"300 random cases of {count} values: {yes} can be paired, checksum {check}")
    pairs = []
    for _ in range(15000):
        x = next_random(seed) % 100001 - 50000
        pairs.append(x)
        pairs.append(2 * x)
    for i in range(len(pairs)):
        j = i + next_random(seed) % (len(pairs) - i)
        pairs[i], pairs[j] = pairs[j], pairs[i]
    print(f"15000 random pairs: {b(can_reorder_doubled(list(pairs)))}")
    moved = list(pairs)
    moved[12345] = 99999
    print(f"the same with one value made 99999: {b(can_reorder_doubled(moved))}")
    print(f"30000 zeros: {b(can_reorder_doubled([0] * 30000))}")
    powers = [1 << (i % 16) for i in range(30000)]
    short = [-(1 << (i % 15)) for i in range(30000)]
    print(f"1 to 2^15, 1875 of each: {b(can_reorder_doubled(powers))}")
    print(f"-1 to -2^14, 2000 of each: {b(can_reorder_doubled(short))}")
    both = []
    for x in range(1, 7501):
        both += [x, 2 * x, -x, -2 * x]
    print(f"x, 2x, -x and -2x for x from 1 to 7500: {b(can_reorder_doubled(both))}")


main()
