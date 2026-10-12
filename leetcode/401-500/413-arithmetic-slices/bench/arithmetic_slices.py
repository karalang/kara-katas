# Benchmark for #413: mirror of arithmetic_slices.kara (slices ending
# here).
import sys


def number_of_arithmetic_slices(nums):
    ending = 0
    total = 0
    for i in range(2, len(nums)):
        if nums[i] - nums[i - 1] == nums[i - 1] - nums[i - 2]:
            ending += 1
            total += ending
        else:
            ending = 0
    return total


seed = 413


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 60000
    n = 5000
    nums = [0]
    while len(nums) < n:
        diff = step() % 7 - 3
        run = 1 + step() % 30
        for _ in range(run):
            if len(nums) < n:
                last = nums[-1]
                if last + diff > 1000 or last + diff < -1000:
                    diff = -diff
                nums.append(last + diff)
    total = 0
    checksum = 0
    for r in range(rounds):
        nums[r * 7919 % n] += r % 3 - 1
        answer = number_of_arithmetic_slices(nums)
        total += answer
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"{rounds} rounds on {n} numbers: total {total}, checksum {checksum}")


main()
