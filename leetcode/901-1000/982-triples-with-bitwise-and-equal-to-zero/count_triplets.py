# LeetCode #982: Triples with Bitwise AND Equal To Zero -- mirror of the
# ★ arm (count_triplets.kara), pair counts, then the free bits' submasks.


def count_triplets(nums):
    all_bits = 0
    for x in nums:
        all_bits |= x
    size = 1
    while size <= all_bits:
        size *= 2
    full = size - 1
    pairs = [0] * size
    for a in nums:
        for b in nums:
            pairs[a & b] += 1
    triples = 0
    for x in nums:
        free = full ^ x
        s = free
        while True:
            triples += pairs[s]
            if s == 0:
                break
            s = (s - 1) & free
    return triples


# ---- test harness ---------------------------------------------------------

seed = 982


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"[{', '.join(str(x) for x in nums)}] -> {count_triplets(nums)}")


def main():
    show([2, 1, 3])
    show([0, 0, 0])
    show([0])
    show([1])
    show([1, 2])
    show([1, 2, 4])
    show([3, 5, 6])
    show([65535, 0])
    show([65535, 65535, 65535])
    show([32768, 32767])
    for count, longest, below in [(300, 12, 8), (3000, 30, 256), (2, 1000, 65536)]:
        total = 0
        check = 0
        for _ in range(count):
            n = longest if count == 2 else 1 + next_random() % longest
            nums = [next_random() % below for _ in range(n)]
            t = count_triplets(nums)
            total += t
            check = (check * 31 + t) % 1000000007
        size = f"{longest}" if count == 2 else f"up to {longest}"
        print(f"{count} random lists of {size} values below {below}: triples {total}, checksum {check}")


main()
