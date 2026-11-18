# LeetCode #2295: Replace Elements in an Array -- the ★ arm's Python
# mirror. A dict from each number to its index.


def array_change(nums, operations):
    out = list(nums)
    at = {x: i for i, x in enumerate(out)}
    for frm, to in operations:
        i = at.pop(frm)
        out[i] = to
        at[to] = i
    return out


# ---- test harness ---------------------------------------------------------

seed = 2295


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [
        ([1, 2, 4, 6], [(1, 3), (4, 7), (6, 1)]),
        ([1, 2], [(1, 3), (2, 1), (3, 2)]),
        ([5, 9], []),
        ([10, 20, 30], [(20, 25), (25, 20)]),
        ([1], [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1000000)]),
    ]
    for nums, operations in cases:
        print("[" + ", ".join(str(x) for x in array_change(nums, operations)) + "]")
    check = 0
    total = 0
    for _ in range(2000):
        n = next_random() % 50 + 1
        present = [False] * 201
        nums = []
        while len(nums) < n:
            x = next_random() % 200 + 1
            if not present[x]:
                present[x] = True
                nums.append(x)
        now = list(nums)
        operations = []
        for _ in range(next_random() % 61):
            i = next_random() % n
            to = next_random() % 200 + 1
            while present[to]:
                to = to % 200 + 1
            present[now[i]] = False
            present[to] = True
            operations.append((now[i], to))
            now[i] = to
        out = array_change(nums, operations)
        for x in out:
            check = (check * 31 + x) % 1000000007
            total += x
    print(f"2000 arrays: checksum {check}, sum {total}")


main()
