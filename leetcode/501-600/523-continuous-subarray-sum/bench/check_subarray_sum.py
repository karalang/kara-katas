# Benchmark for #523: Python mirror of the ★ arm (first index of each
# prefix remainder); see check_subarray_sum.kara.


def check_subarray_sum(nums, k):
    first = {0: -1}
    rem = 0
    for i in range(len(nums)):
        rem = (rem + nums[i]) % k
        if rem in first:
            if i - first[rem] >= 2:
                return True
        else:
            first[rem] = i
    return False


seed = 523


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20 random arrays of 100,000 numbers from 1 to 20,000 (the
    # problem's longest, summing under 2^31) made once; then each checked
    # in 10 rounds against a fresh k from 10,000 to 1,073,751,823.
    arrays = [[1 + next_random() % 20000 for _ in range(100000)] for _ in range(20)]
    yes = 0
    checksum = 0
    for rnd in range(10):
        for a in range(len(arrays)):
            high = next_random()
            k = 10000 + high * 32768 + next_random()
            if check_subarray_sum(arrays[a], k):
                yes += 1
                checksum = (checksum + (rnd + 1) * (a + 1)) % 1000000007
    print(f"20 arrays of 100000, 10 rounds: {yes} true, checksum {checksum}")


main()
