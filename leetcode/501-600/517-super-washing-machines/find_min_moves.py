# LeetCode #517: Super Washing Machines -- the flow across each gap.
# Mirrors find_min_moves.kara (the star arm) and its harness.


def find_min_moves(machines):
    n = len(machines)
    total = sum(machines)
    if total % n != 0:
        return -1
    average = total // n
    moves = 0
    surplus = 0
    for m in machines:
        extra = m - average
        surplus += extra
        moves = max(moves, abs(surplus), extra)
    return moves


# ---- test harness ---------------------------------------------------------

seed = 517


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(machines):
    print(f"[{', '.join(str(m) for m in machines)}]: {find_min_moves(machines)}")


def main():
    show([1, 0, 5])
    show([0, 3, 0])
    show([0, 2, 0])
    show([7])
    show([0, 0, 11, 5])
    show([4, 0, 0, 4])
    show([100000, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    count = 300
    solvable = 0
    checksum = 0
    for t in range(count):
        most = 3 if t % 3 == 0 else 100 if t % 3 == 1 else 100000
        n = 1 + next_random() % 40
        machines = []
        total = 0
        for _ in range(n):
            a = next_random()
            b = next_random()
            m = (a * 32768 + b) % (most + 1)
            machines.append(m)
            total += m
        if t % 2 == 0:
            machines[n - 1] += (n - total % n) % n
        v = find_min_moves(machines)
        if v >= 0:
            solvable += 1
        checksum = (checksum * 31 + v + 1) % 1000000007
    print(f"{count} random rows: {solvable} can be evened out, checksum {checksum}")


main()
