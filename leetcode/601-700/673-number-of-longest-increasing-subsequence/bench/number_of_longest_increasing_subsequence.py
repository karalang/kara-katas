# Benchmark for #673: the length and count ending at each place, as the
# Kara ★ arm.


def find_number_of_lis(nums):
    n = len(nums)
    length = [1] * n
    count = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    length[i] = length[j] + 1
                    count[i] = count[j]
                elif length[j] + 1 == length[i]:
                    count[i] += count[j]
    best = 0
    for v in length:
        best = max(best, v)
    total = 0
    for i in range(n):
        if length[i] == best:
            total += count[i]
    return total


def main():
    rounds = 150
    size = 2000
    seed = 673
    s = 0
    for _ in range(rounds):
        nums = []
        for _ in range(size):
            seed = (seed * 1103515245 + 12345) % 2147483648
            nums.append(seed // 65536)
        s = (s * 31 + find_number_of_lis(nums)) % 1000000007
    print(f"{rounds} arrays of {size}: checksum {s}")


main()
