# LeetCode #1295: Find Numbers with Even Number of Digits -- Python mirror of
# the ★ arm: each number's digits counted by dividing by 10.


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

    edges = [1, 9, 10, 99, 100, 999, 1000, 9999, 10000, 99999, 100000]
    print(f"{find_numbers([12, 345, 2, 6, 7896])} {find_numbers([555, 901, 482, 1771])} {find_numbers(edges)} {find_numbers([100000])} {find_numbers([10])}")
    total = 0
    check = 0
    for _ in range(3000):
        length = next_random() % 500 + 1
        nums = []
        for _ in range(length):
            digits = next_random() % 6 + 1
            low = 10 ** (digits - 1)
            if digits == 6:
                x = 100000
            else:
                a = next_random()
                x = low + (a * 32768 + next_random()) % (9 * low)
            nums.append(x)
        even = find_numbers(nums)
        total += even
        check = (check * 131 + even) % 1000000007
    print(f"3000 random arrays: {total} with an even number of digits, checksum {check}")


main()
