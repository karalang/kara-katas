# LeetCode 768 — Max Chunks To Make Sorted II: benchmark, the ★ arm in Python.
# Sixty-four random arrays of 2,000 values, built once; 40,000 rounds
# each count the next one's chunks.


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


seed = 768


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 40000
    pool = []
    for _ in range(64):
        noise = 1 + next_random() % 40
        pool.append([i * 50 + next_random() % noise * 50 for i in range(2000)])
    total = 0
    check = 0
    for rnd in range(rounds):
        chunks = max_chunks_to_sorted(pool[rnd % 64])
        total += chunks
        check = (check * 31 + chunks) % 1000000007
    print(f"{rounds} arrays of 2000 values: {total} chunks in all, checksum {check}")


main()
