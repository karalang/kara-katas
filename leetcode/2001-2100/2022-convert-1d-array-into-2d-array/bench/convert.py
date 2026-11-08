# LeetCode #2022: Convert 1D Array Into 2D Array -- the ★ arm in Python, the
# same algorithm and workload as convert.kara.


def construct_2d_array(original, m, n):
    if len(original) != m * n:
        return []
    return [original[i * n:(i + 1) * n] for i in range(m)]


seed = 2022


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rows_of = [1, 2, 4, 5, 8, 10, 16, 20, 25, 40, 50, 80, 100, 125, 200, 250, 400, 500, 1000, 20000]
    arrays = [[next_random() % 100000 + 1 for _ in range(20000)] for _ in range(20)]
    calls = rows = check = 0
    for _ in range(200):
        for a in range(20):
            m = rows_of[a]
            n = 20000 // m + 1 if a % 5 == 4 else 20000 // m
            grid = construct_2d_array(arrays[a], m, n)
            calls += 1
            if not grid:
                check = (check * 31 + 1000000006) % 1000000007
            for row in grid:
                rows += 1
                check = (check * 31 + row[0] + row[-1]) % 1000000007
    print(f"{calls} calls: {rows} rows, checksum {check}")


main()
