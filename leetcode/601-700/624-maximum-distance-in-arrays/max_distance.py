# LeetCode #624: Maximum Distance in Arrays -- Python mirror of
# max_distance.kara.
#
# The same one pass and the same harness, printing the same lines.


def max_distance(arrays):
    low = arrays[0][0]
    high = arrays[0][-1]
    best = 0
    for i in range(1, len(arrays)):
        first = arrays[i][0]
        last = arrays[i][-1]
        best = max(best, last - low, high - first)
        low = min(low, first)
        high = max(high, last)
    return best


seed = 624


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(arrays):
    text = "[" + ", ".join("[" + ", ".join(str(v) for v in a) + "]" for a in arrays) + "]"
    print(f"{text} -> {max_distance(arrays)}")


def random_arrays(count, longest, spread):
    arrays = []
    for _ in range(count):
        values = []
        for _ in range(1 + next_random() % longest):
            values.append(next_random() % (2 * spread + 1) - spread)
        values.sort()
        arrays.append(values)
    return arrays


def main():
    show([[1, 2, 3], [4, 5], [1, 2, 3]])
    show([[1], [1]])
    show([[4, 5], [1, 2, 3]])
    show([[-10, 10], [-5, 0], [2, 3]])
    show([[-10, 10], [-1, 0], [-8, 3]])
    show([[-9, -7], [-3, -2, -1], [-6]])
    show([[3], [-2], [7], [0]])
    show([[1, 2], [1, 2], [1, 2]])
    total = 0
    checksum = 0
    for _ in range(300):
        arrays = random_arrays(2 + next_random() % 19, 10, 10000)
        d = max_distance(arrays)
        total += d
        checksum = (checksum * 31 + d) % 1000000007
    print(f"300 random cases: total {total}, checksum {checksum}")
    wide = random_arrays(1000, 100, 10000)
    print(f"1000 arrays of up to 100: {max_distance(wide)}")
    shared = random_arrays(2000, 50, 9000)
    shared[1234] = [-10000, 0, 10000]
    print(f"2000 arrays of up to 50, both ends in one: {max_distance(shared)}")


main()
