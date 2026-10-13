# Benchmark for #473: Python mirror of the ★ arm (backtracking, longest
# stick first); see matchsticks.kara.
import sys

sys.setrecursionlimit(10000)


def place(sticks, i, sides, side):
    if i == len(sticks):
        return True
    for s in range(4):
        if sides[s] + sticks[i] > side:
            continue
        repeat = False
        for t in range(s):
            if sides[t] == sides[s]:
                repeat = True
                break
        if repeat:
            continue
        sides[s] += sticks[i]
        if place(sticks, i + 1, sides, side):
            return True
        sides[s] -= sticks[i]
    return False


def makesquare(matchsticks):
    if len(matchsticks) < 4:
        return False
    total = 0
    for m in matchsticks:
        total += m
    if total % 4 != 0:
        return False
    side = total // 4
    sticks = sorted(matchsticks)
    sticks.reverse()
    if sticks[0] > side:
        return False
    return place(sticks, 0, [0] * 4, side)


seed = 473


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = 2000
    squares = 0
    checksum = 0
    for _ in range(cases):
        sticks = []
        total = 0
        for _ in range(15):
            v = 50 + next_random() % 50
            sticks.append(v)
            total += v
        sticks[14] += (4 - total % 4) % 4
        ok = makesquare(sticks)
        if ok:
            squares += 1
        checksum = (checksum * 3 + (1 if ok else 2)) % 1000000007
    print(f"{cases} sets of 15 sticks: {squares} squares, checksum {checksum}")


main()
