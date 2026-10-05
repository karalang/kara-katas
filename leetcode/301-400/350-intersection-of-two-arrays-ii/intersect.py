# LeetCode #350 -- Intersection of Two Arrays II. Mirrors intersect.kara.


def intersect(a, b):
    counts = {}
    for x in a:
        counts[x] = counts.get(x, 0) + 1
    out = []
    for y in b:
        left = counts.get(y, 0)
        if left > 0:
            counts[y] = left - 1
            out.append(y)
    out.sort()
    return out


def fill(n, hi, seed):
    out = []
    x = seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(x // 16 % (hi + 1))
    return out


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    print(show(intersect([1, 2, 2, 1], [2, 2])))
    print(show(intersect([4, 9, 5], [9, 4, 9, 8, 4])))
    print(show(intersect([1, 2, 3], [4, 5, 6])))
    print(show(intersect([7], [7, 7, 7])))
    print(show(intersect([7, 7, 3, 7], [7, 3, 3, 7])))
    print(show(intersect([0, 1000, 1000, 500], [1000, 0, 1000, 1000])))
    total = 0
    count = 0
    for s in range(200):
        r = intersect(fill(1000, 1000, s), fill(1000, 1000, s + 7919))
        count += len(r)
        total += sum(r)
    print(f"200 pairs at the bounds: {count} values, sum {total}")


main()
