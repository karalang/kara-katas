# LeetCode #2849: Determine if a Cell Is Reachable at a Given Time --
# the bench: the ★ arm over 10^6 random cases on LeetCode's grid, the
# finish within 3 of the start and t within 2 of the distance, all drawn
# first, then each answered 20 times.


def is_reachable_at_time(sx, sy, fx, fy, t):
    if sx == fx and sy == fy:
        return t != 1
    return max(abs(sx - fx), abs(sy - fy)) <= t


def main():
    count, rounds = 1000000, 20
    seed = 2849

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    cases = []
    for _ in range(count):
        sx = nr() * 30000 % 1000000000 + 1
        sy = nr() * 30000 % 1000000000 + 1
        fx = min(max(sx + nr() % 7 - 3, 1), 1000000000)
        fy = sy if nr() % 2 == 0 else min(max(sy + nr() % 7 - 3, 1), 1000000000)
        d = max(abs(sx - fx), abs(sy - fy))
        t = max(d + nr() % 5 - 2, 0)
        cases.append((sx, sy, fx, fy, t))
    yes = check = 0
    for r in range(rounds):
        for sx, sy, fx, fy, t in cases:
            ok = is_reachable_at_time(sx, sy, fx, fy, t)
            if ok:
                yes += 1
            check = (check * 3 + (2 if ok else 1) + r) % 1000000007
    print(f"{count} cases, {rounds} rounds: {yes} true, checksum {check}")


main()
