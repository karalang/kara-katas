# LeetCode 768 — Max Chunks To Make Sorted II: the ★ arm in Python, same output.


def max_chunks_to_sorted(arr):
    maxima = []
    for x in arr:
        if maxima and x < maxima[-1]:
            largest = maxima[-1]
            while maxima and maxima[-1] > x:
                maxima.pop()
            maxima.append(largest)
        else:
            maxima.append(x)
    return len(maxima)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(arr):
    print(f"{arr} -> {max_chunks_to_sorted(arr)}")


def main():
    global seed
    for arr in [[5, 4, 3, 2, 1], [2, 1, 3, 4, 4], [7], [1, 2, 3, 4], [3, 3, 3],
                [1, 1, 0, 0, 1], [4, 2, 2, 1, 1, 5, 6, 6],
                [0, 100000000, 5, 100000000, 7]]:
        show(arr)
    seed = 768
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 60
        spread = 1 + next_random() % 20
        arr = [i // 3 + next_random() % spread for i in range(n)]
        chunks = max_chunks_to_sorted(arr)
        total += chunks
        check = (check * 31 + chunks) % 1000000007
    print(f"300 random arrays: {total} chunks in all, checksum {check}")


main()
