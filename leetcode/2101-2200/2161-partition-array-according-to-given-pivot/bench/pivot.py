# LeetCode #2161: Partition Array According to Given Pivot -- the
# benchmark's Python mirror of pivot.kara.


def pivot_array(nums, pivot):
    out = [x for x in nums if x < pivot]
    out.extend(x for x in nums if x == pivot)
    out.extend(x for x in nums if x > pivot)
    return out


seed = 2161


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    a = next_random()
    return a * 32768 + next_random()


def main():
    lists = [[wide_random() % 2000001 - 1000000 for _ in range(100000)] for _ in range(4)]
    check = 0
    for rnd in range(25):
        for l in range(4):
            at = wide_random() % 100000
            lists[l][at] = wide_random() % 2000001 - 1000000
            pivot = lists[l][wide_random() % 100000]
            out = pivot_array(lists[l], pivot)
            for k in range(10):
                check = (check * 31 + out[k * 9999] + 1000001 + rnd) % 1000000007
    print(f"100 solves: checksum {check}")


main()
