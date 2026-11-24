# LeetCode #1295 bench: the ★ arm over 200 arrays of 500 numbers up to 10^5,
# built once; then 500 passes, each setting one number of every array from
# the checksum so far and answering it.


def find_numbers(nums):
    even = 0
    for x in nums:
        digits = 0
        rest = x
        while rest > 0:
            digits += 1
            rest //= 10
        if digits % 2 == 0:
            even += 1
    return even


def main():
    seed = 1295

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    arrays = []
    for _ in range(200):
        nums = []
        for _ in range(500):
            digits = next_random() % 6 + 1
            low = 10 ** (digits - 1)
            if digits == 6:
                nums.append(100000)
            else:
                a = next_random()
                nums.append(low + (a * 32768 + next_random()) % (9 * low))
        arrays.append(nums)
    check = 0
    for p in range(500):
        for a in range(len(arrays)):
            arrays[a][check % 500] = 1 + check % 100000
            check = (check * 31 + find_numbers(arrays[a]) + p) % 1000000007
    print(f"500 passes over 200 arrays of 500: checksum {check}")


main()
