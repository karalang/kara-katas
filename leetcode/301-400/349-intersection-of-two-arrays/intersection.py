# LeetCode #349 -- Intersection of Two Arrays. Python mirror of
# intersection.kara (the star arm): a set of the first array, walked by the
# second, each kept value removed so it is kept once; answer ascending.


def intersection(a, b):
    seen = set(a)
    out = []
    for y in b:
        if y in seen:
            seen.remove(y)
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
    print("[" + ", ".join(str(x) for x in v) + "]")


show(intersection([1, 2, 2, 1], [2, 2]))
show(intersection([4, 9, 5], [9, 4, 9, 8, 4]))
show(intersection([1, 2, 3], [4, 5, 6]))
show(intersection([7], [7, 7, 7]))
show(intersection([0, 1000, 500], [1000, 0]))
total = count = 0
for s in range(200):
    r = intersection(fill(1000, 1000, s), fill(1000, 1000, s + 7919))
    count += len(r)
    total += sum(r)
print(f"200 pairs at the bounds: {count} values, sum {total}")
