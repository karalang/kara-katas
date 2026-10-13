# LeetCode #473: Matchsticks to Square -- Python mirror of the ★ arm
# (matchsticks.kara): backtracking, longest stick first.


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
    total = sum(matchsticks)
    if total % 4 != 0:
        return False
    side = total // 4
    sticks = sorted(matchsticks, reverse=True)
    if sticks[0] > side:
        return False
    return place(sticks, 0, [0] * 4, side)


# ---- test harness ---------------------------------------------------------

def show(matchsticks):
    line = ", ".join(str(m) for m in matchsticks)
    print(f"[{line}] -> {'true' if makesquare(matchsticks) else 'false'}")


seed = 473


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def square_sticks(n):
    count = [1] * 4
    for _ in range(4, n):
        count[next_random() % 4] += 1
    side = max(count) + next_random() % 8
    sticks = []
    for s in range(4):
        c = count[s]
        cut = [False] * side
        made = 1
        while made < c:
            p = 1 + next_random() % (side - 1)
            if not cut[p]:
                cut[p] = True
                made += 1
        last = 0
        for p in range(1, side):
            if cut[p]:
                sticks.append(p - last)
                last = p
        sticks.append(side - last)
    for i in range(len(sticks) - 1, 0, -1):
        j = next_random() % (i + 1)
        sticks[i], sticks[j] = sticks[j], sticks[i]
    return sticks


def random_case():
    n = 1 + next_random() % 12
    kind = next_random() % 3
    if kind == 2 or n < 4:
        return [1 + next_random() % 8 for _ in range(n)]
    sticks = square_sticks(n)
    if kind == 1:
        frm = next_random() % n
        to = next_random() % n
        if sticks[frm] > 1 and frm != to:
            sticks[frm] -= 1
            sticks[to] += 1
    return sticks


def main():
    show([1, 1, 2, 2, 2])
    show([3, 3, 3, 3, 4])
    show([1, 1, 1, 1])
    show([1, 2, 3])
    show([5, 5, 5, 5, 4, 4, 4, 4, 3, 3, 3, 3])
    show([10, 6, 5, 5, 5, 3, 3, 3, 2, 2, 2, 2])
    show([100000000, 100000000, 100000000, 100000000])
    show([6, 6, 6, 6, 4, 2, 2])
    show([2, 2, 2, 2, 2, 6])
    show([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4])
    show([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2])
    show([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8])
    show([12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12])
    show([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 5, 4, 3, 2, 1])
    count = 400
    sticks_total = 0
    squares = 0
    checksum = 0
    for _ in range(count):
        sticks = random_case()
        ok = makesquare(sticks)
        sticks_total += len(sticks)
        if ok:
            squares += 1
        checksum = (checksum * 3 + (1 if ok else 2)) % 1000000007
    print(f"{count} random cases, {sticks_total} sticks: {squares} squares, checksum {checksum}")


main()
