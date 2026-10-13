# Benchmark for #496: Python mirror of the ★ arm (a stack and a map);
# see next_greater_element.kara.


def next_greater_element(nums1, nums2):
    nxt = {}
    waiting = []
    for x in nums2:
        while waiting:
            top = waiting[-1]
            if top >= x:
                break
            nxt[top] = x
            waiting.pop()
        waiting.append(x)
    out = []
    for x in nums1:
        out.append(nxt[x] if x in nxt else -1)
    return out


seed = 496


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 10,000 cases, built once: nums2 is 1,000 distinct numbers from 0
    # to 10,000 (the problem's most), drawn by shuffling the front of a
    # pool of all of them, and nums1 is every other one of them from the
    # end. Then each case is solved once.
    cases = 10000
    pool = list(range(10001))
    all1 = []
    all2 = []
    for _ in range(cases):
        for i in range(1000):
            j = i + next_random() % (10001 - i)
            pool[i], pool[j] = pool[j], pool[i]
        nums2 = pool[:1000]
        nums1 = []
        k = 999
        while k >= 0:
            nums1.append(nums2[k])
            k -= 2
        all1.append(nums1)
        all2.append(nums2)
    found = 0
    checksum = 0
    for c in range(cases):
        for a in next_greater_element(all1[c], all2[c]):
            if a >= 0:
                found += 1
            checksum = (checksum * 31 + a + 2) % 1000000007
    print(f"{cases} cases of 1000 and 500: {found} with a greater number, checksum {checksum}")


main()
