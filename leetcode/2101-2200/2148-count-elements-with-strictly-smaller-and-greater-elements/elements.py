# LeetCode #2148: Count Elements With Strictly Smaller and Greater
# Elements -- the Python mirror of elements.kara's ★ arm.


def count_elements(nums):
    low = min(nums)
    high = max(nums)
    return sum(1 for x in nums if low < x < high)


seed = 2148


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"[{', '.join(map(str, nums))}] -> {count_elements(nums)}")


def main():
    show([11, 7, 2, 15])
    show([-3, 3, 3, 90])
    show([5])
    show([4, 4, 4])
    show([1, 2])
    show([3, 1, 2, 3, 1, 2])
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 12 + 1
        kind = rnd % 3
        if kind == 0:
            nums = [next_random() % 3 + 1 for _ in range(n)]
        elif kind == 1:
            nums = [next_random() % 5 + 1 for _ in range(n)]
        else:
            nums = [next_random() * 7 % 200001 - 100000 for _ in range(n)]
        count = count_elements(nums)
        total += count
        check = (check * 31 + count + n) % 1000000007
    print(f"2000 lists: {total} counted in all, checksum {check}")
    every = list(range(-50, 50))
    same = [-100000] * 100
    rand = [next_random() * 7 % 200001 - 100000 for _ in range(100)]
    print(f"100 numbers: {count_elements(every)} one of each, {count_elements(same)} all equal, {count_elements(rand)} at random")


main()
