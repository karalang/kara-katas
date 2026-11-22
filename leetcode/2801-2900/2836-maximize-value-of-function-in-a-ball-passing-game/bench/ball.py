# LeetCode #2836: Maximize Value of Function in a Ball Passing Game --
# the bench, mirrored from ball.kara: binary lifting over 34 levels.


def get_max_function_value(receiver, k):
    n = len(receiver)
    levels = 34
    jump = [receiver[:]]
    gain = [receiver[:]]
    for j in range(1, levels):
        pj, pg = jump[j - 1], gain[j - 1]
        jump.append([pj[pj[i]] for i in range(n)])
        gain.append([pg[i] + pg[pj[i]] for i in range(n)])
    best = 0
    for start in range(n):
        at = start
        total = start
        for j in range(levels):
            if (k >> j) & 1:
                total += gain[j][at]
                at = jump[j][at]
        best = max(best, total)
    return best


seed = 2836


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    count, rounds, n = 10, 3, 100000
    games = []
    for _ in range(count):
        receiver = [wide() % n for _ in range(n)]
        w = wide()
        k = (w * 10 + next_random()) % 10000000000 + 1
        games.append((receiver, k))
    check = 0
    for r in range(rounds):
        for receiver, k in games:
            best = get_max_function_value(receiver, k)
            check = (check * 31 + best % 1000000007 + r) % 1000000007
    print(f"{count} games of {n}, {rounds} rounds: checksum {check}")


main()
