# LeetCode #2155: All Divisions With the Highest Score of a Binary Array --
# the Python mirror of divisions.kara's ★ arm.


def max_score_indices(nums):
    right_ones = sum(1 for x in nums if x == 1)
    left_zeros = 0
    top = right_ones
    found = [0]
    for i, x in enumerate(nums):
        if x == 0:
            left_zeros += 1
        else:
            right_ones -= 1
        score = left_zeros + right_ones
        if score > top:
            top = score
            found = []
        if score == top:
            found.append(i + 1)
    return found


seed = 2155


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def best(nums):
    return sorted(max_score_indices(nums))


def fmt(v):
    return "[" + ", ".join(map(str, v)) + "]"


def show(nums):
    print(f"{fmt(nums)} -> {fmt(best(nums))}")


def main():
    show([0, 0, 1, 0])
    show([0, 0, 0])
    show([1, 1])
    show([0])
    show([1])
    show([1, 0])
    show([0, 1, 0, 1])
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 16 + 1
        one_in = [2, 3, 4][rnd % 3]
        nums = [1 if next_random() % one_in == 0 else 0 for _ in range(n)]
        out = best(nums)
        total += len(out)
        for i in out:
            check = (check * 31 + i + 1) % 1000000007
        check = (check * 31 + n) % 1000000007
    print(f"2000 lists: {total} divisions in all, checksum {check}")
    turns = [i % 2 for i in range(100000)]
    zeros = [0] * 100000
    rand = [next_random() % 2 for _ in range(100000)]
    for name, nums in [("in turn", turns), ("all 0", zeros), ("at random", rand)]:
        out = best(nums)
        s = 0
        for i in out:
            s = (s * 31 + i + 1) % 1000000007
        print(f"100000 bits {name}: {len(out)} divisions, first {out[0]}, last {out[-1]}, checksum {s}")


main()
