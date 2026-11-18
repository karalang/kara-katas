# LeetCode #2295: Replace Elements in an Array -- the bench, the ★ arm in
# Python. A dict from each number to its index finds the one to replace
# at once; the replacement takes over the index.


def array_change(nums, operations):
    out = list(nums)
    at = {}
    for i in range(len(out)):
        at[out[i]] = i
    for frm, to in operations:
        i = at.pop(frm)
        out[i] = to
        at[to] = i
    return out


def main():
    seed = 2295

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def wide():
        hi = next_random()
        return (hi * 32768 + next_random()) % 1000000 + 1

    cases = []
    for _ in range(10):
        n = 100000
        present = [False] * 1000001
        nums = []
        while len(nums) < n:
            x = wide()
            if not present[x]:
                present[x] = True
                nums.append(x)
        now = list(nums)
        operations = []
        for _ in range(100000):
            i = next_random() % n
            to = wide()
            while present[to]:
                to = to % 1000000 + 1
            present[now[i]] = False
            present[to] = True
            operations.append((now[i], to))
            now[i] = to
        cases.append((nums, operations))
    check = 0
    for _ in range(3):
        for nums, operations in cases:
            for x in array_change(nums, operations):
                check = (check * 31 + x) % 1000000007
    print(f"3 passes over 10 arrays of 10^5 with 10^5 operations: checksum {check}")


main()
