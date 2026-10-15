# Benchmark for #674: one pass with a running length, as the Kara ★ arm.


def find_length_of_lcis(nums):
    best = 0
    run = 0
    for i in range(len(nums)):
        if i > 0 and nums[i - 1] < nums[i]:
            run += 1
        else:
            run = 1
        best = max(best, run)
    return best


def main():
    arrays = 100
    size = 10000
    rounds = 20000
    seed = 674
    all_ = []
    for _ in range(arrays):
        nums = []
        for _ in range(size):
            seed = (seed * 1103515245 + 12345) % 2147483648
            nums.append(seed // 65536 % 1000)
        all_.append(nums)
    s = 0
    for r in range(rounds):
        a = r % arrays
        all_[a][r * 7919 % size] = r % 1000
        s = (s * 31 + find_length_of_lcis(all_[a])) % 1000000007
    print(f"{rounds} rounds over {arrays} arrays of {size}: checksum {s}")


main()
