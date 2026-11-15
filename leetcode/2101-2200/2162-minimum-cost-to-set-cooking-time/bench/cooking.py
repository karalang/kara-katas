# LeetCode #2162: Minimum Cost to Set Cooking Time -- the benchmark's
# Python mirror of cooking.kara.


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


def main():
    total = 0
    check = 0
    for p in range(30):
        move_cost = p % 10 + 1
        push_cost = p * 3 % 10 + 1
        for start_at in range(10):
            for target_seconds in range(1, 6040):
                c = min_cost_set_time(start_at, move_cost, push_cost, target_seconds)
                total += c
                check = (check * 31 + c + p) % 1000000007
    print(f"1811700 solves: {total} in all, checksum {check}")


main()
