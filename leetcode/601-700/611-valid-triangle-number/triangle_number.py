# LeetCode #611: Valid Triangle Number -- Python mirror of the ★ arm
# (sort, then two pointers); see triangle_number.kara.


def triangle_number(nums):
    a = sorted(nums)
    count = 0
    for k in range(2, len(a)):
        i = 0
        j = k - 1
        while i < j:
            if a[i] + a[j] > a[k]:
                count += j - i
                j -= 1
            else:
                i += 1
    return count


# ---- test harness ---------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(nums):
    print(f"{fmt(nums)} -> {triangle_number(nums)}")


def main():
    show([2, 2, 3, 4])
    show([4, 2, 3, 4])
    show([])
    show([5, 5])
    show([0, 0, 0])
    show([0, 1, 1, 1])
    show([1, 2, 3])
    show([7, 7, 7])
    show([1, 1, 1, 1, 100])
    show([10, 3, 7, 3, 10, 6, 1, 7])
    print(f"200 lengths of 1000 -> {triangle_number([1000] * 200)}")
    print(f"lengths 1 to 200 -> {triangle_number(list(range(1, 201)))}")
    seed = [611]
    total = 0
    checksum = 0
    for _ in range(300):
        size = step(seed) % 61
        bound = 1 + step(seed) % 1000
        nums = [step(seed) % (bound + 1) for _ in range(size)]
        got = triangle_number(nums)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"300 random arrays: {total} triangles, checksum {checksum}")
    big = [step(seed) % 1001 for _ in range(200)]
    print(f"200 random lengths -> {triangle_number(big)}")


main()
