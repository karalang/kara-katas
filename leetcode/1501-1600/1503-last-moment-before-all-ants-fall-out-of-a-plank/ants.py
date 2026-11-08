# LeetCode #1503: Last Moment Before All Ants Fall Out of a Plank -- the
# Python mirror of the ★ arm: two ants that meet and turn round are, by
# their labels only, two ants that pass through each other, so the last
# fall is the longest walk: a left ant's position, a right ant's n - p.


def last_moment(n, left, right):
    best = 0
    for p in left:
        best = max(best, p)
    for p in right:
        best = max(best, n - p)
    return best


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


def batch(count, most):
    total = check = 0
    for _ in range(count):
        n, left, right = random_plank(most)
        answer = last_moment(n, left, right)
        total += answer
        check = mix(check, answer)
    print(f"{count} planks of 1 to {most} units: sum {total}, checksum {check}")


def main():
    examples = [(4, [4, 3], [0, 1]), (7, [], [0, 1, 2, 3, 4, 5, 6, 7]),
                (7, [0, 1, 2, 3, 4, 5, 6, 7], []), (1, [0], [1]), (1, [1], [0]),
                (20, [], []), (9, [5], [4]), (10, [2, 6], [3, 7])]
    for n, left, right in examples:
        print(f"n = {n}, left = {left}, right = {right} -> {last_moment(n, left, right)}")
    batch(3000, 12)
    batch(300, 100)
    batch(5, 600)


main()
