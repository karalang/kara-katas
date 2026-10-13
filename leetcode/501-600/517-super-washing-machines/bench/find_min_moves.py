# Benchmark for #517: Python mirror of the ★ arm (the flow across each
# gap); see find_min_moves.kara.


def find_min_moves(machines):
    n = len(machines)
    total = 0
    for m in machines:
        total += m
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


seed = 517


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 100 random rows of 10,000 machines (the problem's most) holding up
    # to 100,000 dresses each, every other row topped up so the dresses
    # share out evenly, built once. Then each is solved 300 times.
    rows = 100
    all_rows = []
    for t in range(rows):
        machines = []
        total = 0
        for _ in range(10000):
            a = next_random()
            b = next_random()
            m = (a * 32768 + b) % 100001
            machines.append(m)
            total += m
        if t % 2 == 0:
            machines[9999] += (10000 - total % 10000) % 10000
        all_rows.append(machines)
    checksum = 0
    for _ in range(300):
        for t in range(rows):
            checksum = (checksum * 31 + find_min_moves(all_rows[t]) + 1) % 1000000007
    print(f"{rows} rows of 10000 machines, 300 times each: checksum {checksum}")


main()
