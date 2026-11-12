# LeetCode #1144: Decrease Elements To Make Array Zigzag -- the Python
# mirror of moves_to_make_zigzag.kara: one pass for each choice of which
# places are lowered, each lowered place brought to one below its smaller
# neighbour; the cheaper choice is the answer.

INF = 2**63 - 1


def moves_to_make_zigzag(nums):
    n = len(nums)
    best = INF
    for low in range(2):
        moves = 0
        for i in range(low, n, 2):
            least = INF
            if i > 0:
                least = min(least, nums[i - 1])
            if i + 1 < n:
                least = min(least, nums[i + 1])
            if nums[i] >= least:
                moves += nums[i] - least + 1
        best = min(best, moves)
    return best


seed = 1144


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20 arrays of 1000 values from 1 to 1000, built once. Each of 5000
    # rounds draws one value of every array again and answers every array.
    arrays = [[next_random() % 1000 + 1 for _ in range(1000)] for _ in range(20)]
    total = 0
    check = 0
    for _ in range(5000):
        for a in range(20):
            at = next_random() % 1000
            arrays[a][at] = next_random() % 1000 + 1
            answer = moves_to_make_zigzag(arrays[a])
            total += answer
            check = (check * 131 + answer + 1) % 1000000007
    print(f"5000 rounds over 20 arrays of 1000 values: answers total {total}, checksum {check}")


main()
