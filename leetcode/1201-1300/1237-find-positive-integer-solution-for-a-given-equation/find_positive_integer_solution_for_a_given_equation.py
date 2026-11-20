# LeetCode #1237: Find Positive Integer Solution for a Given Equation --
# Python mirror of the ★ arm: two pointers, x rising from 1 and y falling
# from 1000.


class CustomFunction:
    def __init__(self, id):
        self.id = id

    def f(self, x, y):
        return [None, x + y, x * y, x * x + y, x + y * y, x * x + y * y, (x + y) ** 2,
                x ** 3 + y ** 3, x * x * y, x * y * y][self.id]


def find_solution(customfunction, z):
    out = []
    x, y = 1, 1000
    while x <= 1000 and y >= 1:
        v = customfunction.f(x, y)
        if v < z:
            x += 1
        elif v > z:
            y -= 1
        else:
            out.append([x, y])
            x += 1
            y -= 1
    return out


# ---- test harness ---------------------------------------------------------

def main():
    print(find_solution(CustomFunction(1), 5))
    print(find_solution(CustomFunction(2), 5))
    check = 0
    pairs = 0
    for id in range(1, 10):
        for z in range(1, 101):
            got = find_solution(CustomFunction(id), z)
            pairs += len(got)
            for p in got:
                check = (check * 131 + p[0] * 1001 + p[1]) % 1000000007
    print(f"9 functions, z from 1 to 100: {pairs} pairs, checksum {check}")


main()
