# Benchmark: LeetCode #977 Squares of a Sorted Array -- the ★ arm, two
# pointers from the ends, on 20 sorted arrays of 10000 numbers. Mirrors
# sorted_squares.kara, .rs, .c and go-seq/.


def sorted_squares(nums):
    n = len(nums)
    out = [0] * n
    lo, hi, at = 0, n - 1, n - 1
    while lo <= hi:
        a = nums[lo] * nums[lo]
        b = nums[hi] * nums[hi]
        if a > b:
            out[at] = a
            lo += 1
        else:
            out[at] = b
            hi -= 1
        at -= 1
    return out


seed = 977


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count, n = 500, 20, 10000
    arrays = []
    for _ in range(count):
        nums = sorted(next_random() % 20001 - 10000 for _ in range(n))
        arrays.append(nums)
    total = check = 0
    for r in range(rounds):
        for i in range(count):
            out = sorted_squares(arrays[(r + i) % count])
            total += out[0] + out[n - 1]
            check = (check * 31 + out[(r * 13 + i * 7) % n]) % 1000000007
    print(f"{rounds} rounds over {count} arrays of 10000 numbers: "
          f"squares total {total}, checksum {check}")


main()
