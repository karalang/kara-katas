# LeetCode 775 — Global and Local Inversions: Python mirror of the ★ arm
# (every value at most one place from its index), with the same harness.


def is_ideal_permutation(nums):
    for i in range(len(nums)):
        if abs(nums[i] - i) > 1:
            return False
    return True


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def ideal(seed, n):
    nums = list(range(n))
    i = 0
    while i + 1 < n:
        if next_random(seed) % 2 == 0:
            nums[i], nums[i + 1] = nums[i + 1], nums[i]
            i += 2
        else:
            i += 1
    return nums


def shuffled(seed, n):
    nums = list(range(n))
    i = n - 1
    while i > 0:
        j = next_random(seed) % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
        i -= 1
    return nums


def show(nums):
    answer = is_ideal_permutation(nums)
    print(f"[{', '.join(map(str, nums))}] -> {str(answer).lower()}")


def main():
    show([1, 0, 2])
    show([1, 2, 0])
    show([0])
    show([1, 0])
    show([0, 2, 1, 3])
    show([2, 0, 1])
    show([0, 1, 3, 2, 5, 4])
    show([1, 0, 3, 2, 4, 6, 5, 7, 9, 8])
    show([0, 1, 2, 4, 5, 3])
    seed = [775]
    big = ideal(seed, 100000)
    print(f"100000 values, ideal -> {str(is_ideal_permutation(big)).lower()}")
    big[99996], big[99999] = big[99999], big[99996]
    print(f"100000 values, a far swap at the end -> {str(is_ideal_permutation(big)).lower()}")
    ideals = 0
    check = 0
    for case in range(300):
        n = 1 + next_random(seed) % 60
        nums = shuffled(seed, n) if case % 3 == 0 else ideal(seed, n)
        if case % 3 == 2:
            i = next_random(seed) % n
            j = min(i + 1 + next_random(seed) % 3, n - 1)
            nums[i], nums[j] = nums[j], nums[i]
        answer = is_ideal_permutation(nums)
        if answer:
            ideals += 1
        check = (check * 31 + (n if answer else 1000 - n)) % 1000000007
    print(f"300 random permutations: {ideals} ideal, checksum {check}")


main()
