# LeetCode 769 — Max Chunks To Make Sorted: benchmark, the ★ arm in Python.
# Sixty-four near-sorted permutations of 2,000, built once; 150,000
# rounds each count the next one's chunks.


def max_chunks_to_sorted(arr):
    chunks = 0
    largest = 0
    for i, x in enumerate(arr):
        if x > largest:
            largest = x
        if largest == i:
            chunks += 1
    return chunks


seed = 769


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 150000
    n = 2000
    pool = []
    for _ in range(64):
        arr = list(range(n))
        swaps = next_random() % n
        for _ in range(swaps):
            i = next_random() % n
            j = min(i + 1 + next_random() % 4, n - 1)
            arr[i], arr[j] = arr[j], arr[i]
        pool.append(arr)
    total = 0
    check = 0
    for rnd in range(rounds):
        chunks = max_chunks_to_sorted(pool[rnd % 64])
        total += chunks
        check = (check * 31 + chunks) % 1000000007
    print(f"{rounds} permutations of 2000: {total} chunks in all, checksum {check}")


main()
