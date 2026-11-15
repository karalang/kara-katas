# LeetCode #2162: Minimum Cost to Set Cooking Time -- the Python mirror of
# cooking.kara, the ★ arm: each of the two ways of writing the time that
# fits, its digits walked from the start digit.


def cost(digits, start_at, move_cost, push_cost):
    at = start_at
    total = 0
    for c in digits:
        d = int(c)
        if d != at:
            total += move_cost
            at = d
        total += push_cost
    return total


def min_cost_set_time(start_at, move_cost, push_cost, target_seconds):
    minutes = target_seconds // 60
    seconds = target_seconds % 60
    best = 2**63 - 1
    for m, s in [(minutes, seconds), (minutes - 1, seconds + 60)]:
        if 0 <= m <= 99 and s <= 99:
            best = min(best, cost(str(m * 100 + s), start_at, move_cost, push_cost))
    return best


seed = 2162


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(start_at, move_cost, push_cost, target_seconds):
    print(f"start {start_at}, move {move_cost}, push {push_cost}, {target_seconds} s -> "
          f"{min_cost_set_time(start_at, move_cost, push_cost, target_seconds)}")


def main():
    show(1, 2, 1, 600)
    show(0, 1, 2, 76)
    show(5, 1, 1, 1)
    show(9, 3, 1, 6039)
    show(0, 10, 1, 6000)
    show(9, 100, 1, 599)
    total = 0
    check = 0
    for rnd in range(2000):
        most = [10, 1000, 100000][rnd % 3]
        start_at = next_random() % 10
        move_cost = next_random() % most + 1
        push_cost = next_random() % most + 1
        target_seconds = next_random() % 6039 + 1
        c = min_cost_set_time(start_at, move_cost, push_cost, target_seconds)
        total += c
        check = (check * 31 + c + 1) % 1000000007
    print(f"2000 settings: {total} in all, checksum {check}")
    for move_cost, push_cost in [(100000, 1), (1, 100000)]:
        every = 0
        h = 0
        for start_at in range(10):
            for target_seconds in range(1, 6040):
                c = min_cost_set_time(start_at, move_cost, push_cost, target_seconds)
                every += c
                h = (h * 31 + c + 1) % 1000000007
        print(f"all 60390, move {move_cost}, push {push_cost}: {every} in all, checksum {h}")


main()
