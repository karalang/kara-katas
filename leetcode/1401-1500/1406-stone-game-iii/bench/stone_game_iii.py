# LeetCode #1406 bench, Python: the same lead from the last stone back,
# workload and checksum as stone_game_iii.kara.


def stone_game_iii(stone_value):
    n = len(stone_value)
    best = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        taken = 0
        b = -2**31
        for k in range(1, 4):
            if i + k > n:
                break
            taken += stone_value[i + k - 1]
            lead = taken - best[i + k]
            if lead > b:
                b = lead
        best[i] = b
    return "Alice" if best[0] > 0 else "Bob" if best[0] < 0 else "Tie"


def main():
    seed = 1406
    pool = []
    for _ in range(100000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        pool.append(seed // 65536 % 41 - 20)
    check = 0
    for r in range(1000):
        at = (check + r * 7919) % 50001
        winner = stone_game_iii(pool[at:at + 50000])
        code = {"Alice": 1, "Bob": 2, "Tie": 3}[winner]
        check = (check * 131 + code) % 1000000007
    print(f"1000 rows of 5 * 10^4 stones: checksum {check}")


main()
