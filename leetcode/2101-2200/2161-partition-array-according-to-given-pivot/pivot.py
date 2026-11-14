# LeetCode #2161: Partition Array According to Given Pivot -- the Python
# mirror of pivot.kara, the ★ arm: three passes in order, below, equal,
# above.


def pivot_array(nums, pivot):
    out = [x for x in nums if x < pivot]
    out.extend(x for x in nums if x == pivot)
    out.extend(x for x in nums if x > pivot)
    return out


seed = 2161


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    a = next_random()
    return a * 32768 + next_random()


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(nums, pivot):
    print(f"{fmt(nums)}, {pivot} -> {fmt(pivot_array(nums, pivot))}")


def fold(out, check):
    for x in out:
        check = (check * 31 + x + 1000001) % 1000000007
    return check


def main():
    show([9, 12, 5, 10, 14, 3, 10], 10)
    show([-3, 4, 3, 2], 2)
    show([7], 7)
    show([4, 4, 4], 4)
    show([3, 1, 2, 9], 9)
    show([5, 8, 1, 5], 5)
    check = 0
    for rnd in range(2000):
        n = next_random() % 12 + 1
        reach = [5, 50, 1000000][rnd % 3]
        nums = [wide_random() % (2 * reach + 1) - reach for _ in range(n)]
        pivot = nums[next_random() % n]
        check = fold(pivot_array(nums, pivot), check)
    print(f"2000 lists: checksum {check}")
    rand = [wide_random() % 2000001 - 1000000 for _ in range(100000)]
    pivot = rand[wide_random() % 100000]
    out = pivot_array(rand, pivot)
    print(f"100000 at random, pivot {pivot}: first {out[0]}, last {out[99999]}, checksum {fold(out, 0)}")
    same = [-1000000] * 100000
    out = pivot_array(same, -1000000)
    print(f"100000 the same: first {out[0]}, last {out[99999]}, checksum {fold(out, 0)}")


main()
