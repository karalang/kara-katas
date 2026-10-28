# LeetCode #1007: Minimum Domino Rotations For Equal Row -- two candidates
#
# Mirrors min_rotations.kara, the ★ arm, and its test harness; its output
# is byte-identical.


def rotations(tops, bottoms, v):
    to_top = 0
    to_bottom = 0
    for i in range(len(tops)):
        if tops[i] != v and bottoms[i] != v:
            return -1
        if tops[i] != v:
            to_top += 1
        elif bottoms[i] != v:
            to_bottom += 1
    return min(to_top, to_bottom)


def min_domino_rotations(tops, bottoms):
    a = rotations(tops, bottoms, tops[0])
    b = rotations(tops, bottoms, bottoms[0])
    if a == -1:
        return b
    if b == -1:
        return a
    return min(a, b)


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_row(n, faces, target, forced, seed):
    tops = []
    bottoms = []
    for _ in range(n):
        t = 1 + next_random(seed) % faces
        b = 1 + next_random(seed) % faces
        if next_random(seed) % 8 < forced:
            if next_random(seed) % 2 == 0:
                t = target
            else:
                b = target
        tops.append(t)
        bottoms.append(b)
    return tops, bottoms


def show(nums):
    return "[" + ",".join(str(x) for x in nums) + "]"


def main():
    examples = [
        ([2, 1, 2, 4, 2, 2], [5, 2, 6, 2, 3, 2]),
        ([3, 5, 1, 2, 3], [3, 6, 3, 3, 4]),
        ([1, 1], [1, 1]),
        ([1, 2], [2, 1]),
        ([1, 2], [3, 4]),
        ([1, 2, 1, 1], [2, 1, 2, 2]),
        ([6, 6, 6, 5], [5, 5, 5, 6]),
        ([1, 2, 3, 4, 6], [6, 6, 6, 6, 5]),
        ([2, 3, 2, 3], [3, 2, 3, 2]),
        ([4, 4, 1, 4], [1, 1, 4, 1]),
    ]
    for tops, bottoms in examples:
        print(f"tops = {show(tops)}, bottoms = {show(bottoms)} -> {min_domino_rotations(tops, bottoms)}")
    n = 20000
    half_tops = [3 if i % 2 == 0 else 1 + i % 6 for i in range(n)]
    half_bottoms = [1 + i % 5 if i % 2 == 0 else 3 for i in range(n)]
    late_tops = [5] * n
    late_bottoms = [2 if i == n - 1 else 5 for i in range(n)]
    late_tops[n - 1] = 4
    large = [
        ("20000 of 6 over 6", [6] * n, [6] * n),
        ("3 on alternate halves", half_tops, half_bottoms),
        ("5 everywhere but the last domino", late_tops, late_bottoms),
    ]
    for name, tops, bottoms in large:
        print(f"{name} -> {min_domino_rotations(tops, bottoms)}")
    seed = [1007]
    for count, most in [(3000, 8), (1000, 100), (100, 2000), (3, 20000)]:
        total = 0
        possible = 0
        acc = 0
        check = 0
        for _ in range(count):
            size = 2 + next_random(seed) % (most - 1)
            faces = 1 + next_random(seed) % 6
            target = 1 + next_random(seed) % faces
            forced = 8 if next_random(seed) % 2 == 0 else next_random(seed) % 9
            tops, bottoms = random_row(size, faces, target, forced, seed)
            got = min_domino_rotations(tops, bottoms)
            total += size
            if got >= 0:
                possible += 1
                acc += got
            check = (check * 31 + got + 2) % 1000000007
        print(f"{count} random rows of {total} dominoes: {possible} possible, rotations sum to {acc}, checksum {check}")


main()
