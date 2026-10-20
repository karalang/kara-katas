# LeetCode 810 -- Chalkboard XOR Game: the bench, with the ★ arm's XOR and
# count.


def xor_game(nums):
    x = 0
    for v in nums:
        x ^= v
    return x == 0 or len(nums) % 2 == 0


seed = 810


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# 64 boards of 999 numbers are made once. Each round writes a new number
# into one place of the next board and asks who wins it.
def main():
    boards = [[next_random() for _ in range(999)] for _ in range(64)]
    rounds = 10000000
    wins = 0
    check = 0
    for r in range(rounds):
        k = r % 64
        boards[k][r // 64 % 999] = next_random()
        win = 1 if xor_game(boards[k]) else 0
        wins += win
        check = (check * 131 + win + r % 1000) % 1000000007
    print(f"{rounds} rounds of 999 numbers: {wins} won by Alice, checksum {check}")


main()
