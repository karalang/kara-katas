# LeetCode #2029: Stone Game IX -- the ★ arm in Python, the same algorithm
# and workload as stones.kara.


def stone_game_ix(stones):
    cnt = [0, 0, 0]
    for s in stones:
        cnt[s % 3] += 1
    if cnt[0] % 2 == 0:
        return cnt[1] >= 1 and cnt[2] >= 1
    return abs(cnt[1] - cnt[2]) > 2


seed = 2029


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    games = []
    for a in range(20):
        stones = []
        for _ in range(100000):
            base = 3 * (next_random() % 3333)
            if next_random() % 10 < a % 5:
                residue = 3
            elif next_random() % 10 < 3 * a % 11:
                residue = 1
            else:
                residue = 2
            stones.append(base + residue)
        games.append(stones)
    calls = wins = check = 0
    for rnd in range(100):
        for a in range(20):
            games[a][(rnd * 997 + a * 31) % 100000] += 1
            answer = stone_game_ix(games[a])
            calls += 1
            if answer:
                wins += 1
            check = (check * 31 + (1 if answer else 2)) % 1000000007
    print(f"{calls} calls: Alice wins {wins}, checksum {check}")


main()
