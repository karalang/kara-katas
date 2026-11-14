# LeetCode #1558: Minimum Numbers of Function Calls to Make Target Array --
# bench: the ★ arm (every value's 1 bits, and the widest value's length
# less one) over 20 arrays of 100000 values, built once, each asked 30
# times. Python mirror of calls.kara.


def min_operations(nums):
    increments = 0
    widest = 0
    for x in nums:
        increments += bin(x).count("1")
        if x > 0:
            widest = max(widest, x.bit_length())
    return increments + max(widest - 1, 0)


seed = 1558


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    arrays = []
    for _ in range(20):
        nums = []
        for _ in range(100000):
            bits = next_random() % 30 + 1
            draw = next_random() * 32768 + next_random()
            nums.append(draw % (1 << bits))
        arrays.append(nums)
    check = 0
    total = 0
    for _ in range(30):
        for nums in arrays:
            calls = min_operations(nums)
            total += calls
            check = mix(check, calls)
    print(f"30 passes over 20 arrays of 100000 values: {total} calls, checksum {check}")


main()
