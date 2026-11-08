# LeetCode #1503: Last Moment Before All Ants Fall Out of a Plank -- the
# benchmark, the same algorithm as ants_sim.kara: the statement simulated
# with doubled positions and half-unit ticks.


def last_moment(n, left, right):
    pos = [2 * p for p in left] + [2 * p for p in right]
    dirs = [-1] * len(left) + [1] * len(right)
    on = [True] * len(pos)
    alive = len(pos)
    at = [-1] * (2 * n + 1)
    tick = last = 0
    while alive > 0:
        for i in range(len(pos)):
            if on[i] and ((pos[i] == 0 and dirs[i] == -1) or (pos[i] == 2 * n and dirs[i] == 1)):
                on[i] = False
                alive -= 1
                last = tick
        for i in range(len(pos)):
            if on[i]:
                other = at[pos[i]]
                if other >= 0:
                    dirs[i] = -dirs[i]
                    dirs[other] = -dirs[other]
                else:
                    at[pos[i]] = i
        for i in range(len(pos)):
            if on[i]:
                at[pos[i]] = -1
                pos[i] += dirs[i]
        tick += 1
    return last // 2


seed = 1503


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


# A plank of 1 to `most` units; each position 0..=n holds a left ant, a
# right ant or none, with chance `fill` in 100 of holding one.
def random_plank(most):
    n = next_random() % most + 1
    fill = next_random() % 100 + 1
    left, right = [], []
    for p in range(n + 1):
        if next_random() % 100 < fill:
            if next_random() % 2 == 0:
                left.append(p)
            else:
                right.append(p)
    return n, left, right


def main():
    planks = [random_plank(1000) for _ in range(300)]
    total = check = 0
    for n, left, right in planks:
        answer = last_moment(n, list(left), list(right))
        total += answer
        check = mix(check, answer)
    print(f"300 planks of 1 to 1000 units simulated: sum {total}, checksum {check}")


main()
