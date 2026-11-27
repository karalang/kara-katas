# LeetCode #1803: Count Pairs With XOR in a Range -- the ★ arm in Python: a
# binary trie over 15 bits, the pairs below `high + 1` less those below
# `low`.
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
    print(f"{count_pairs([1, 4, 2, 7], 2, 6)} {count_pairs([9, 8, 4, 2, 1], 5, 14)}")
    print(f"{count_pairs([5], 1, 5)} {count_pairs([3, 3], 1, 4)} {count_pairs([1, 2, 3, 20000], 1, 20000)} {count_pairs([6, 3, 5, 1], 5, 5)} {count_pairs([1, 2, 3], 4, 100)}")
    wide = [1 + next_random() % 20000 for _ in range(20000)]
    flat = [20000] * 20000
    print(f"the most: {count_pairs(wide, 1, 20000)} {count_pairs(wide, 4000, 5000)} {count_pairs(flat, 1, 20000)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 20
        top = 1 + next_random() % 64
        nums = [1 + next_random() % top for _ in range(n)]
        low = 1 + next_random() % 70
        high = low + next_random() % (71 - low)
        check = (check * 31 + count_pairs(nums, low, high)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
