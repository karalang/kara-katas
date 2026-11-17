# Python mirror of collisions.kara (LeetCode #2211, the ★ arm): skip the
# leading 'L's and the trailing 'R's and count the cars between that are
# not 'S'.


def count_collisions(directions):
    lo = 0
    while lo < len(directions) and directions[lo] == "L":
        lo += 1
    hi = len(directions)
    while hi > lo and directions[hi - 1] == "R":
        hi -= 1
    return sum(1 for c in directions[lo:hi] if c != "S")


# ---- test harness ---------------------------------------------------------

seed = 2211


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_road(n):
    return "".join("LRS"[next_random() % 3] for _ in range(n))


def show(directions):
    print(f'"{directions}" -> {count_collisions(directions)}')


def main():
    # LeetCode's two examples, then four more: one car, every car still,
    # two cars head on, and a column of cars running into a still one
    show("RLRSLL")
    show("LLRR")
    show("S")
    show("SSSS")
    show("RL")
    show("RRRRS")
    # 3000 random roads of 1 to 30 cars
    check = 0
    for _ in range(3000):
        n = next_random() % 30 + 1
        check = (check * 31 + count_collisions(random_road(n))) % 1000000007
    print(f"3000 roads: checksum {check}")
    # the constraints' longest: 10^5 random cars, then 10^5 cars all
    # driving right into one still car at the end
    wide = random_road(100000)
    column = "R" * 99999 + "S"
    print(f"10^5 random -> {count_collisions(wide)}, 10^5 into a still car -> {count_collisions(column)}")


main()
