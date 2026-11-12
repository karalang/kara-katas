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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_array(n, top):
    return [next_random() % top + 1 for _ in range(n)]


def main():
    global seed
    print(f"example 1: {moves_to_make_zigzag([1, 2, 3])}")
    print(f"example 2: {moves_to_make_zigzag([9, 6, 1, 6, 2])}")
    print(f"one element: {moves_to_make_zigzag([5])}")
    print(f"two alike: {moves_to_make_zigzag([5, 5])}")
    print(f"a zigzag already: {moves_to_make_zigzag([1, 3, 1, 3, 2])}")
    print(f"seven alike: {moves_to_make_zigzag([4] * 7)}")
    print(f"rising 1 to 10: {moves_to_make_zigzag(list(range(1, 11)))}")
    seed = 1144
    total = 0
    check = 0
    for i in range(2000):
        n = next_random() % 50 + 1
        top = 10 if i % 3 == 2 else 1000
        answer = moves_to_make_zigzag(random_array(n, top))
        total += answer
        check = (check * 131 + answer + 1) % 1000000007
    print(f"2000 random arrays: answers total {total}, checksum {check}")
    print(f"1000 of 1000: {moves_to_make_zigzag([1000] * 1000)}")
    print(f"1 to 1000 rising: {moves_to_make_zigzag(list(range(1, 1001)))}")
    print(f"1000 random: {moves_to_make_zigzag(random_array(1000, 1000))}")


main()
