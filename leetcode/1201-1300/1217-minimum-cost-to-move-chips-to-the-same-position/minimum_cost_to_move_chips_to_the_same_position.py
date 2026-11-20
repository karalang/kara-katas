# LeetCode #1217: Minimum Cost to Move Chips to The Same Position -- a
# Python mirror of the ★ arm: a move of two is free, so only a change of
# parity costs, and the answer is the lesser of the odd and even counts.


def min_cost_to_move_chips(position):
    odd = 0
    even = 0
    for p in position:
        if p % 2 == 1:
            odd += 1
        else:
            even += 1
    return min(odd, even)


seed = 1217


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    cases = [[1, 2, 3], [2, 2, 2, 3, 3], [1, 1000000000], [1], [5, 5, 5], [1, 2], [4, 1, 6, 3, 8, 5]]
    for position in cases:
        print(f"{show(position)}: {min_cost_to_move_chips(position)}")
    total = 0
    check = 0
    for _ in range(1000):
        n = next_random() % 10 + 1
        top = next_random() % 10 + 1
        position = [next_random() % top + 1 for _ in range(n)]
        answer = min_cost_to_move_chips(position)
        total += answer
        check = (check * 131 + answer + 1) % 1000000007
    print(f"1000 small cases: costs total {total}, checksum {check}")
    big = [(next_random() * 32768 + next_random()) % 1000000000 + 1 for _ in range(100)]
    print(f"100 random chips up to 10^9: {min_cost_to_move_chips(big)}")
    print(f"100 chips at 10^9: {min_cost_to_move_chips([1000000000] * 100)}")
    print(f"1 to 100: {min_cost_to_move_chips(list(range(1, 101)))}")
    lone = [2 * i + 1 for i in range(99)] + [1000000000]
    print(f"99 odd chips and one at 10^9: {min_cost_to_move_chips(lone)}")


main()
