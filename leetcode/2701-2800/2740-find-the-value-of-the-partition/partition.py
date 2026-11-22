# LeetCode #2740: Find the Value of the Partition -- Python mirror of
# partition.kara (the ★ arm): sort, and the least gap between neighbours.


def find_value_of_partition(nums):
    nums = sorted(nums)
    return min(nums[i] - nums[i - 1] for i in range(1, len(nums)))


seed = 2740


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_numbers(n, most):
    out = []
    for _ in range(n):
        hi = next_random()
        lo = next_random()
        out.append((hi * 32768 + lo) % most + 1)
    return out


def main():
    print(find_value_of_partition([1, 3, 2, 4]))
    print(find_value_of_partition([100, 1, 10]))
    print(find_value_of_partition([5, 5]))
    print(find_value_of_partition([1, 1000000000]))
    print(find_value_of_partition([1000 - 7 * i for i in range(50)]))
    total = check = 0
    for c in range(2020):
        if c < 2000:
            n = next_random() % 19 + 2
            nums = random_numbers(n, 100)
        else:
            nums = random_numbers(2000, 1000000000)
        value = find_value_of_partition(nums)
        total += value
        check = (check * 31 + value) % 1000000007
        if c == 1999:
            print(f"2000 small arrays: values sum to {total}, checksum {check}")
            total = check = 0
    print(f"20 arrays of 2000 numbers: values sum to {total}, checksum {check}")


main()
