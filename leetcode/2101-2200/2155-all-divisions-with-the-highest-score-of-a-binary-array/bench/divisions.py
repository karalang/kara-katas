# LeetCode #2155: All Divisions With the Highest Score of a Binary Array
# -- the benchmark's Python mirror of divisions.kara.


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
            found.clear()
        if score == top:
            found.append(i + 1)
    return found


seed = 2155


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = [[next_random() % 2 for _ in range(100000)] for _ in range(4)]
    total = 0
    check = 0
    for rnd in range(50):
        for s in range(4):
            at = next_random() % 100000
            lists[s][at] = 1 - lists[s][at]
            out = max_score_indices(lists[s])
            total += len(out)
            check = (check * 31 + len(out) + out[0] + out[-1] + rnd) % 1000000007
    print(f"200 solves: {total} divisions in all, checksum {check}")


main()
