# LeetCode #2149: Rearrange Array Elements by Sign -- the Python mirror of
# signs.kara's ★ arm.


def rearrange_array(nums):
    out = [0] * len(nums)
    positive = 0
    negative = 1
    for x in nums:
        if x > 0:
            out[positive] = x
            positive += 2
        else:
            out[negative] = x
            negative += 2
    return out


seed = 2149


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"{fmt(nums)} -> {fmt(rearrange_array(nums))}")


def fmt(nums):
    return "[" + ", ".join(map(str, nums)) + "]"


def draw(half, top):
    nums = []
    for i in range(2 * half):
        size = next_random() % top + 1
        nums.append(size if i < half else -size)
    for i in range(2 * half - 1, 0, -1):
        j = next_random() % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
    return nums


def main():
    show([3, 1, -2, -5, 2, -4])
    show([-1, 1])
    show([-5, -4, 3, 2])
    show([7, -7])
    show([1, 2, 3, -1, -2, -3])
    show([-100000, 100000, -1, 1])
    total = 0
    check = 0
    for rnd in range(2000):
        half = next_random() % 10 + 1
        nums = draw(half, [3, 100000][rnd % 2])
        out = rearrange_array(nums)
        for i, x in enumerate(out):
            total += x * (1 - i % 2 * 2)
            check = (check * 31 + x + 100000) % 1000000007
    print(f"2000 lists: {total} in all, checksum {check}")
    blocks = [i + 1 if i < 100000 else 99999 - i for i in range(200000)]
    turns = [i // 2 + 1 if i % 2 == 0 else -(i // 2 + 1) for i in range(200000)]
    rand = draw(100000, 100000)
    for name, nums in [("blocks", blocks), ("in turn", turns), ("at random", rand)]:
        out = rearrange_array(nums)
        s = 0
        for x in out:
            s = (s * 31 + x + 100000) % 1000000007
        print(f"200000 numbers {name}: {out[0]} {out[1]} .. {out[199998]} {out[199999]}, checksum {s}")


main()
