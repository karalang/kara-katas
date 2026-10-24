# LeetCode #941: Valid Mountain Array -- a walk up and a walk down.
# Mirrors valid_mountain_array.kara (the ★ arm) and prints the same output.


def valid_mountain_array(arr):
    n = len(arr)
    i = 0
    while i + 1 < n and arr[i] < arr[i + 1]:
        i += 1
    if i == 0 or i == n - 1:
        return False
    while i + 1 < n and arr[i] > arr[i + 1]:
        i += 1
    return i == n - 1


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_case(n, step):
    top = next_random() % n
    out = [0]
    v = least = most = 0
    for i in range(1, n):
        if i <= top:
            v += 1 + next_random() % step
        else:
            v -= 1 + next_random() % step
        out.append(v)
        least = min(least, v)
        most = max(most, v)
    out = [x - least for x in out]
    if next_random() % 2 == 0:
        j = next_random() % n
        out[j] = next_random() % (most - least + 1)
    return out


def show(arr):
    return "[" + ",".join(str(x) for x in arr) + "]"


def b(x):
    return "true" if x else "false"


def main():
    global seed
    examples = [
        [2, 1],
        [3, 5, 5],
        [0, 3, 2, 1],
        [1],
        [1, 3, 2],
        [0, 1, 2],
        [2, 1, 0],
        [0, 2, 3, 3, 5, 2, 1],
        [0, 1, 0, 1, 0],
        [1, 2, 3, 4, 5, 4, 3, 2, 1, 1],
    ]
    for e in examples:
        print(f"{show(e)}: {b(valid_mountain_array(e))}")
    seed = 941
    count = mountains = check = 0
    for _ in range(300):
        n = 1 + next_random() % 50
        arr = random_case(n, 3)
        a = valid_mountain_array(arr)
        count += n
        if a:
            mountains += 1
        check = (check * 1000003 + (n if a else 0)) % 1000000007
    print(f"300 random cases of {count} values: {mountains} mountains, checksum {check}")
    middle = [i if i <= 5000 else 10000 - i for i in range(10000)]
    print(f"up to 5000 and down: {b(valid_mountain_array(middle))}")
    flat = middle[:]
    flat[3000] = flat[2999]
    print(f"the same with one flat step: {b(valid_mountain_array(flat))}")
    print(f"0 to 9999: {b(valid_mountain_array(list(range(10000))))}")
    early = [0] + [10000 - i for i in range(1, 10000)]
    print(f"0, then 9999 down to 1: {b(valid_mountain_array(early))}")
    print(f"10000 sevens: {b(valid_mountain_array([7] * 10000))}")
    noise = [next_random() % 10001 for _ in range(10000)]
    print(f"10000 random values: {b(valid_mountain_array(noise))}")


main()
