# LeetCode #374: Guess Number Higher or Lower -- mirror of guess_number.kara.


class Game:
    def __init__(self, pick):
        self.pick = pick
        self.calls = 0

    def guess(self, num):
        self.calls += 1
        if self.pick < num:
            return -1
        if self.pick > num:
            return 1
        return 0


def guess_number(n, game):
    lo, hi = 1, n
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        answer = game.guess(mid)
        if answer == 0:
            return mid
        if answer < 0:
            hi = mid - 1
        else:
            lo = mid + 1
    return -1


def play(n, pick):
    return guess_number(n, Game(pick))


def show(label, n, pick):
    print(f"{label}: {play(n, pick)}")


def main():
    show("example 1", 10, 6)
    show("example 2", 1, 1)
    show("example 3", 2, 1)
    show("the top of two", 2, 2)
    show("1 of 2^31 - 1", 2147483647, 1)
    show("2^31 - 1 of 2^31 - 1", 2147483647, 2147483647)
    show("2^30 of 2^31 - 1", 2147483647, 1073741824)
    show("the middle of three", 3, 2)
    show("a power of two minus one", 1000000, 65535)
    seed = 374
    checksum = 0
    for _ in range(1000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        high = seed // 65536
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = 1 + (high * 65536 + seed // 32768) % 2147483647
        seed = (seed * 1103515245 + 12345) % 2147483648
        high2 = seed // 65536
        seed = (seed * 1103515245 + 12345) % 2147483648
        pick = 1 + (high2 * 65536 + seed // 32768) % n
        checksum = (checksum * 31 + play(n, pick)) % 1000000007
    print(f"1000 random games: checksum {checksum}")


main()
