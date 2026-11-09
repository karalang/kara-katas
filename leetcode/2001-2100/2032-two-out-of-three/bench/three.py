# LeetCode #2032: Two Out of Three -- the ★ arm in Python, the same
# algorithm and workload as three.kara.


def two_out_of_three(nums1, nums2, nums3):
    mask = [0] * 101
    for x in nums1:
        mask[x] |= 1
    for x in nums2:
        mask[x] |= 2
    for x in nums3:
        mask[x] |= 4
    out = []
    for v in range(1, 101):
        if bin(mask[v]).count("1") >= 2:
            out.append(v)
    return out


seed = 2032


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    problems = []
    for p in range(100):
        arrays = []
        for _ in range(3):
            arrays.append([next_random() % (p % 90 + 11) + 1 for _ in range(100)])
        problems.append(arrays)
    calls = 0
    kept = 0
    check = 0
    for rnd in range(4000):
        for p in range(100):
            k = (rnd + p) % 3
            at = (rnd * 7 + p * 13) % 100
            problems[p][k][at] = (problems[p][k][at] + rnd) % 100 + 1
            answer = two_out_of_three(problems[p][0], problems[p][1], problems[p][2])
            calls += 1
            kept += len(answer)
            for v in answer:
                check = (check * 31 + v) % 1000000007
    print(f"{calls} calls: {kept} values kept, checksum {check}")


main()
