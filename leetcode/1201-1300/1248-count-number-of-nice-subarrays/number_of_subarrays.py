# LeetCode #1248: Count Number of Nice Subarrays -- mirrors
# number_of_subarrays.kara.


def number_of_subarrays(nums, k):
    prefixes = [0] * (len(nums) + 1)
    prefixes[0] = 1
    odd = 0
    nice = 0
    for v in nums:
        odd += v % 2
        if odd >= k:
            nice += prefixes[odd - k]
        prefixes[odd] += 1
    return nice


seed = 1248


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    a = number_of_subarrays([1, 1, 2, 1, 1], 3)
    b = number_of_subarrays([2, 4, 6], 1)
    c = number_of_subarrays([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2)
    print(f"{a} {b} {c}")
    total = 0
    check = 0
    for _ in range(1000):
        n = next_random() % 2000 + 1
        percent = next_random() % 101
        nums = []
        for _ in range(n):
            v = next_random() % 50000 + 1
            nums.append(2 * v - 1 if next_random() % 100 < percent else 2 * v)
        odd = sum(1 for v in nums if v % 2 == 1)
        k = next_random() % (odd + 2) + 1
        nice = number_of_subarrays(nums, k)
        total += nice
        check = (check * 131 + nice) % 1000000007
    print(f"1000 random arrays: total {total}, checksum {check}")
    odd = [2 * i + 1 for i in range(50000)]
    one = [1 if i == 25000 else 2 for i in range(50000)]
    x = number_of_subarrays(odd, 1)
    y = number_of_subarrays(odd, 25000)
    z = number_of_subarrays(one, 1)
    print(f"50000 values: all odd, k = 1 {x}, k = 25000 {y}; one odd {z}")


main()
