# LeetCode #2029: Stone Game IX -- Python mirror of the ★ arm (stones.kara).
# Only each stone's value mod 3 matters; a 0 only passes the turn, so only
# the parity of their count matters. With an even count of 0s Alice wins
# when she has both a 1 and a 2; with an odd count she needs one side to
# outnumber the other by more than 2. O(n).


def stone_game_ix(stones):
    cnt = [0, 0, 0]
    for s in stones:
        cnt[s % 3] += 1
    if cnt[0] % 2 == 0:
        return cnt[1] >= 1 and cnt[2] >= 1
    return abs(cnt[1] - cnt[2]) > 2


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, answer):
    return (check * 31 + (1 if answer else 0)) % 1000000007


def draw(n, top, zeros, ones):
    stones = []
    for _ in range(n):
        base = 3 * (next_random() % (top // 3))
        pick = next_random() % 10
        if pick < zeros:
            residue = 3
        elif next_random() % 10 < ones:
            residue = 1
        else:
            residue = 2
        stones.append(base + residue)
    return stones


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    examples = [
        [2, 1],
        [2],
        [5, 1, 2, 4, 3],
        [3, 6, 9],
        [1, 1, 1, 1, 2],
        [3, 1, 1, 1, 1, 2],
        [1, 2, 3],
        [7, 4, 1, 10, 3, 2],
    ]
    for stones in examples:
        print(f"{show(stones)} -> {str(stone_game_ix(stones)).lower()}")
    seed = 2029
    wins = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 20 + 1
        zeros = next_random() % 5
        ones = next_random() % 11
        stones = draw(n, 30, zeros, ones)
        answer = stone_game_ix(stones)
        if answer:
            wins += 1
        check = mix(check, answer)
    print(f"3000 games of up to 20 stones: Alice wins {wins}, checksum {check}")
    wins = 0
    check = 0
    for a in range(8):
        stones = draw(100000, 10000, [0, 1, 3, 5, 2, 4, 0, 1][a], [5, 5, 0, 10, 1, 9, 10, 0][a])
        answer = stone_game_ix(stones)
        if answer:
            wins += 1
        check = mix(check, answer)
    print(f"8 games of 100000 stones: Alice wins {wins}, checksum {check}")


main()
