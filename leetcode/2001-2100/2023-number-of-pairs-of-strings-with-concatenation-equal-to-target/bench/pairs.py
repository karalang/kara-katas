# LeetCode #2023: Number of Pairs of Strings With Concatenation Equal to
# Target -- the ★ arm in Python, the same algorithm and workload as
# pairs.kara.


def num_of_pairs(nums, target):
    count = {}
    for s in nums:
        count[s] = count.get(s, 0) + 1
    pairs = 0
    for k in range(1, len(target)):
        a = target[:k]
        b = target[k:]
        ca = count.get(a, 0)
        if a == b:
            pairs += ca * (ca - 1)
        else:
            pairs += ca * count.get(b, 0)
    return pairs


seed = 2023


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = []
    targets = []
    for _ in range(300):
        block_len = next_random() % 3 + 1
        block = "".join(chr(ord("1") + next_random() % 2) for _ in range(block_len))
        lists.append([block * (next_random() % (100 // block_len) + 1) for _ in range(100)])
        targets.append(block * (next_random() % (100 // block_len - 1) + 2))
    calls = total = check = 0
    for _ in range(20):
        for p in range(300):
            pairs = num_of_pairs(lists[p], targets[p])
            calls += 1
            total += pairs
            check = (check * 31 + pairs) % 1000000007
    print(f"{calls} calls: {total} pairs, checksum {check}")


main()
