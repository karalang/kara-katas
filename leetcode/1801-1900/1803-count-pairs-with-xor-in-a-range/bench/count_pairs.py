# LeetCode #1803: Count Pairs With XOR in a Range -- the bench in Python: the
# ★ arm over 40 random lists of 20000 numbers built once, 100 calls.
BITS = 15


def count_below(nums, limit):
    children = [0, 0]
    counts = [0]
    pairs = 0
    for x in nums:
        node = 0
        for b in range(BITS - 1, -1, -1):
            xb = x >> b & 1
            if limit >> b & 1:
                same = children[2 * node + xb]
                if same:
                    pairs += counts[same]
                node = children[2 * node + 1 - xb]
            else:
                node = children[2 * node + xb]
            if node == 0:
                break
        at = 0
        counts[0] += 1
        for b in range(BITS - 1, -1, -1):
            xb = x >> b & 1
            if children[2 * at + xb] == 0:
                children[2 * at + xb] = len(counts)
                counts.append(0)
                children += [0, 0]
            at = children[2 * at + xb]
            counts[at] += 1
    return pairs


def count_pairs(nums, low, high):
    return count_below(nums, high + 1) - count_below(nums, low)


seed = 1803


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = [[1 + next_random() % 20000 for _ in range(20000)] for _ in range(40)]
    check = 0
    for call in range(100):
        low = 1 + next_random() % 20000
        high = low + next_random() % (20001 - low)
        nums = lists[(check + call) % 40]
        check = (check * 31 + count_pairs(nums, low, high)) % 1000000007
    print(f"100 calls over 40 lists of 20000 numbers: checksum {check}")


main()
