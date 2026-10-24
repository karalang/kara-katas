# Benchmark: LeetCode #982 Triples with Bitwise AND Equal To Zero -- the
# ★ arm, pair counts and the free bits' submasks, on lists of LeetCode's
# largest size. Mirrors count_triplets.kara, .rs, .c and go-seq/.


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


seed = 982


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 15
    lists = [[next_random() % 65536 for _ in range(1000)] for _ in range(20)]
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            t = count_triplets(lists[(r + i) % 20])
            total += t
            check = (check * 31 + t) % 1000000007
    print(f"{rounds} rounds over 20 lists of 1000 values: triples {total}, checksum {check}")


main()
