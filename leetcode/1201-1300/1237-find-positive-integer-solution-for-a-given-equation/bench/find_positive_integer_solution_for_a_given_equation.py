# LeetCode #1237 bench: the ★ arm in Python, over the same 9 functions, z
# from 1 to 100 and 30 passes as the Kāra bench.


class CustomFunction:
    def __init__(self, id):
        self.id = id

    def f(self, x, y):
        id = self.id
        if id == 1:
            return x + y
        if id == 2:
            return x * y
        if id == 3:
            return x * x + y
        if id == 4:
            return x + y * y
        if id == 5:
            return x * x + y * y
        if id == 6:
            return (x + y) * (x + y)
        if id == 7:
            return x * x * x + y * y * y
        if id == 8:
            return x * x * y
        return x * y * y


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


def main():
    check = 0
    for _ in range(30):
        for id in range(1, 10):
            for z in range(1, 101):
                for p in find_solution(CustomFunction(id), z):
                    check = (check * 131 + p[0] * 1001 + p[1]) % 1000000007
    print(f"9 functions, z from 1 to 100, 30 passes: checksum {check}")


main()
