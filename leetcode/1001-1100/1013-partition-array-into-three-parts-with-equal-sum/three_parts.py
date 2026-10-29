# LeetCode #1013: Partition Array Into Three Parts With Equal Sum -- two cuts
# Mirrors three_parts.kara line for line; the output is byte-identical.


def can_three_parts_equal_sum(arr):
    total = 0
    for x in arr:
        total += x
    if total % 3 != 0:
        return False
    target = total // 3
    prefix = 0
    cuts = 0
    for i in range(len(arr) - 1):
        prefix += arr[i]
        if cuts == 0 and prefix == target:
            cuts = 1
        elif cuts == 1 and prefix == 2 * target:
            return True
    return False


# ---- test harness ----------------------------------------------------------

seed = 1013


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_array(length, spread):
    return [next_random() % (2 * spread + 1) - spread for _ in range(length)]


def built_array(most, spread):
    share = next_random() % (2 * spread + 1) - spread
    arr = []
    for _ in range(3):
        length = 1 + next_random() % most
        s = 0
        for _ in range(length - 1):
            x = next_random() % (2 * spread + 1) - spread
            arr.append(x)
            s += x
        arr.append(share - s)
    return arr


def b(v):
    return "true" if v else "false"


def main():
    examples = [
        [0, 2, 1, -6, 6, -7, 9, 1, 2, 0, 1],
        [0, 2, 1, -6, 6, 7, 9, -1, 2, 0, 1],
        [3, 3, 6, 5, -2, 2, 5, 1, -9, 4],
        [0, 0, 0],
        [0, 0, 0, 0],
        [1, -1, 1, -1],
        [1, -1, 0, 0],
        [1, 1, 1],
        [1, 2, 3],
        [6, 0, 0],
        [2, 2, 2, -2, 2],
        [10000, -10000, 10000, -10000, 10000, -10000],
        [1, 2, -3, 3, 0, 0, 3, -6, 6],
    ]
    for arr in examples:
        s = "[" + ",".join(str(x) for x in arr) + "]"
        print(f"arr = {s} -> {b(can_three_parts_equal_sum(arr))}")
    groups = [(3000, 3, 2), (3000, 8, 3), (1000, 60, 5), (200, 1000, 20), (6, 50000, 10000), (6, 50000, 2)]
    for count, length, spread in groups:
        yes = 0
        check = 0
        for _ in range(count):
            arr = random_array(length, spread)
            answer = can_three_parts_equal_sum(arr)
            if answer:
                yes += 1
            check = (check * 2 + (1 if answer else 0)) % 1000000007
        print(f"{count} random arrays of {length} values within {spread}: {yes} split, checksum {check}")
    built = 0
    moved = 0
    for _ in range(1000):
        arr = built_array(100, 50)
        if can_three_parts_equal_sum(arr):
            built += 1
        at = next_random() % len(arr)
        arr[at] += 3
        if can_three_parts_equal_sum(arr):
            moved += 1
    print(f"1000 built arrays: {built} split; with one value moved by three: {moved} split")


main()
