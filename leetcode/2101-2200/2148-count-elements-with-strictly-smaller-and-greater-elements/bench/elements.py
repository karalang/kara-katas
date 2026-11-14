# LeetCode #2148: Count Elements With Strictly Smaller and Greater
# Elements -- the benchmark's Python mirror of elements.kara.


def count_elements(nums):
    low = min(nums)
    high = max(nums)
    return sum(1 for x in nums if low < x < high)


seed = 2148


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    pool = [next_random() * 7 % 200001 - 100000 for _ in range(100000)]
    total = 0
    check = 0
    for rnd in range(200000):
        at = next_random() % 100000
        pool[at] = next_random() % 21 - 10
        start = next_random() % (100000 - 100)
        nums = pool[start:start + 100]
        count = count_elements(nums)
        total += count
        check = (check * 31 + count + rnd) % 1000000007
    print(f"200000 counts: {total} counted in all, checksum {check}")


main()
