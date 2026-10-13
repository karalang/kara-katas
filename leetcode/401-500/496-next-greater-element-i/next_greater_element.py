# LeetCode #496: Next Greater Element I -- a stack and a map.
# Mirrors next_greater_element.kara (the ★ arm); output is byte-identical.


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


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(name, nums1, nums2):
    print(f"{name}: {fmt(nums1)} in {fmt(nums2)} -> {fmt(next_greater_element(nums1, nums2))}")


seed = 496


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show("example 1", [4, 1, 2], [1, 3, 4, 2])
    show("example 2", [2, 4], [1, 2, 3, 4])
    show("one number", [7], [7])
    show("falling", [1, 5, 3], [5, 4, 3, 2, 1])
    show("rising", [1, 5, 3], [1, 2, 3, 4, 5])
    show("valley", [9, 2, 8, 1], [9, 2, 8, 1, 10])
    show("all asked", [3, 1, 4, 0, 2], [2, 0, 4, 1, 3])
    show("largest", [0, 9999], [0, 9999, 10000])
    count = 300
    asked = 0
    found = 0
    checksum = 0
    for _ in range(count):
        size = 1 + next_random() % 30
        used = [False] * 100
        nums2 = []
        while len(nums2) < size:
            x = next_random() % 100
            if not used[x]:
                used[x] = True
                nums2.append(x)
        wanted = 1 + next_random() % size
        taken = [False] * len(nums2)
        nums1 = []
        while len(nums1) < wanted:
            j = next_random() % size
            if not taken[j]:
                taken[j] = True
                nums1.append(nums2[j])
        for a in next_greater_element(nums1, nums2):
            asked += 1
            if a >= 0:
                found += 1
            checksum = (checksum * 31 + a + 2) % 1000000007
    print(f"{count} random cases: {asked} asked, {found} with a greater number, checksum {checksum}")


main()
