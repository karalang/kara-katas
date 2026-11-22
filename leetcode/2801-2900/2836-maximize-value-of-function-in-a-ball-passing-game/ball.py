# LeetCode #2836: Maximize Value of Function in a Ball Passing Game --
# the Python mirror of the ★ arm: binary lifting over 34 levels.


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


# ---- the harness: the same in every arm --------------------------------

seed = 2836


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    g = get_max_function_value
    print(f"{g([2, 0, 1], 4)} {g([1, 1, 1, 2, 3], 3)}")
    print(g([0], 10000000000))
    print(g(list(range(100000)), 10000000000))
    check = 0
    for _ in range(3000):
        n = next_random() % 8 + 1
        receiver = [next_random() % n for _ in range(n)]
        k = next_random() % 20 + 1
        check = (check * 31 + g(receiver, k)) % 1000000007
    print(f"3000 small games: checksum {check}")
    check = 0
    for _ in range(100):
        n = next_random() % 2000 + 1
        receiver = [next_random() % n for _ in range(n)]
        w = wide()
        k = (w * 10 + next_random()) % 10000000000 + 1
        check = (check * 31 + g(receiver, k)) % 1000000007
    print(f"100 large games: checksum {check}")


main()
