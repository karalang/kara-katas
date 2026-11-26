def dest_city(paths):
    starts = {path[0] for path in paths}
    return next(path[1] for path in paths if path[1] not in starts)


def main():
    seed = 1436
    trips = []
    for _ in range(1000):
        cities = []
        for c in range(101):
            name = []
            for _ in range(8):
                seed = (seed * 1103515245 + 12345) % 2147483648
                name.append(chr(97 + seed // 65536 % 26))
            name.append(chr(97 + c // 26))
            name.append(chr(97 + c % 26))
            cities.append("".join(name))
        seed = (seed * 1103515245 + 12345) % 2147483648
        turn = seed // 65536 % 100
        trips.append([[cities[(i + turn) % 100], cities[(i + turn) % 100 + 1]] for i in range(100)])
    check = 0
    for _ in range(100):
        for paths in trips:
            city = dest_city(paths)
            h = 0
            for b in city.encode():
                h = (h * 31 + b) % 1000000007
            check = (check * 131 + h) % 1000000007
    print(f"10^5 trips of 100 paths: checksum {check}")


main()
