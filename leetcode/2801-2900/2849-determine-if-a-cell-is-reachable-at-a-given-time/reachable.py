# LeetCode #2849: Determine if a Cell Is Reachable at a Given Time -- the
# Python mirror of the ★ arm: the larger of the two distances, and the
# start itself unreachable at t = 1.


def is_reachable_at_time(sx, sy, fx, fy, t):
    if sx == fx and sy == fy:
        return t != 1
    return max(abs(sx - fx), abs(sy - fy)) <= t


def b(r):
    return "true" if r else "false"


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    print(f"{b(is_reachable_at_time(2, 4, 7, 7, 6))} {b(is_reachable_at_time(3, 1, 7, 3, 3))}")
    print(f"{b(is_reachable_at_time(5, 5, 5, 5, 0))} {b(is_reachable_at_time(5, 5, 5, 5, 1))} {b(is_reachable_at_time(5, 5, 5, 5, 2))}")
    print(f"{b(is_reachable_at_time(1, 1, 10**9, 10**9, 999999999))} {b(is_reachable_at_time(1, 1, 10**9, 10**9, 999999998))}")
    yes = check = 0
    for sx in range(1, 5):
        for sy in range(1, 5):
            for fx in range(1, 5):
                for fy in range(1, 5):
                    for t in range(5):
                        r = is_reachable_at_time(sx, sy, fx, fy, t)
                        yes += r
                        check = (check * 3 + (2 if r else 1)) % 1000000007
    print(f"1280 small cases: {yes} true, checksum {check}")
    rng = Rng(2849)
    yes = check = 0
    for _ in range(20000):
        sx = rng.next() * 30000 % 1000000000 + 1
        sy = rng.next() * 30000 % 1000000000 + 1
        fx = min(max(sx + rng.next() % 2001 - 1000, 1), 1000000000)
        fy = sy if rng.next() % 2 == 0 else min(max(sy + rng.next() % 2001 - 1000, 1), 1000000000)
        d = max(abs(sx - fx), abs(sy - fy))
        t = max(d + rng.next() % 7 - 3, 0)
        r = is_reachable_at_time(sx, sy, fx, fy, t)
        yes += r
        check = (check * 3 + (2 if r else 1)) % 1000000007
    print(f"20000 random cases: {yes} true, checksum {check}")


main()
