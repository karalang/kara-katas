# LeetCode #1558: Minimum Numbers of Function Calls to Make Target Array --
# the Python mirror of calls.kara, the ★ arm: every value's 1 bits, and
# the widest value's length less one. Prints byte-identical output.


def min_operations(nums):
    increments = 0
    widest = 0
    for x in nums:
        increments += bin(x).count("1")
        if x > 0:
            widest = max(widest, x.bit_length())
    return increments + max(widest - 1, 0)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, longest, most):
    check = 0
    total = 0
    for _ in range(count):
        length = (next_random() * 32768 + next_random()) % longest + 1
        nums = []
        for _ in range(length):
            wide = (next_random() * 32768 + next_random()) * 32768 + next_random()
            nums.append(wide % (most + 1))
        calls = min_operations(nums)
        total += calls
        check = mix(check, calls)
    print(f"{count} arrays of up to {longest} values up to {most}: {total} calls, checksum {check}")


def main():
    global seed
    examples = [
        [1, 5],
        [2, 2],
        [4, 2, 5],
        [3, 2, 2, 4],
        [2, 4, 8, 16],
        [0],
        [0, 0, 1],
        [1000000000],
        [1000000000, 999999999, 1],
    ]
    for nums in examples:
        print(f"[{', '.join(map(str, nums))}] -> {min_operations(nums)}")
    seed = 1558
    batch(3000, 8, 30)
    batch(300, 1000, 1000000000)
    batch(30, 100000, 1000000000)


main()
