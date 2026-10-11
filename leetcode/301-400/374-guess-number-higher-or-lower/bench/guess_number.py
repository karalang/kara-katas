# Benchmark for #374 -- mirror of guess_number.kara.


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


def main():
    seed = 374
    checksum = 0
    guesses = 0
    for _ in range(2000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        high = seed // 65536
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = 1 + (high * 65536 + seed // 32768) % 2147483647
        seed = (seed * 1103515245 + 12345) % 2147483648
        high2 = seed // 65536
        seed = (seed * 1103515245 + 12345) % 2147483648
        pick = 1 + (high2 * 65536 + seed // 32768) % n
        game = Game(pick)
        got = guess_number(n, game)
        guesses += game.calls
        checksum = (checksum * 31 + got) % 1000000007
    print(f"{guesses} guesses, checksum {checksum}")


main()
