# LeetCode 769 — Max Chunks To Make Sorted: the ★ arm in Python, same output.


def max_chunks_to_sorted(arr):
    chunks = 0
    largest = 0
    for i, x in enumerate(arr):
        largest = max(largest, x)
        if largest == i:
            chunks += 1
    return chunks


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(arr):
    print(f"{arr} -> {max_chunks_to_sorted(arr)}")


def main():
    global seed
    for arr in [[4, 3, 2, 1, 0], [1, 0, 2, 3, 4], [0], [0, 1, 2, 3], [1, 2, 0, 3],
                [0, 2, 1, 4, 3, 5], [2, 0, 1, 5, 3, 4, 9, 6, 7, 8]]:
        show(arr)
    seed = 769
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 10
        arr = list(range(n))
        swaps = next_random() % (n + 1)
        for _ in range(swaps):
            i = next_random() % n
            j = min(i + 1 + next_random() % 3, n - 1)
            arr[i], arr[j] = arr[j], arr[i]
        chunks = max_chunks_to_sorted(arr)
        total += chunks
        check = (check * 31 + chunks) % 1000000007
    print(f"300 random permutations: {total} chunks in all, checksum {check}")


main()
