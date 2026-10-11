# LeetCode #370: Range Addition -- mirror of range_addition.kara.


def get_modified_array(length, updates):
    diff = [0] * (length + 1)
    for start, end, inc in updates:
        diff[start] += inc
        diff[end + 1] -= inc
    out = [0] * length
    running = 0
    for i in range(length):
        running += diff[i]
        out[i] = running
    return out


def show(label, length, updates):
    print(f"{label}: {get_modified_array(length, updates)}")


def main():
    show("example 1", 5, [(1, 3, 2), (2, 4, 3), (0, 2, -2)])
    show("example 2", 10, [(2, 4, 6), (5, 6, 8), (1, 9, -4)])
    show("no updates", 4, [])
    show("one cell", 1, [(0, 0, 7), (0, 0, -3)])
    show("the whole array", 4, [(0, 3, 5)])
    show("updates that cancel", 6, [(1, 4, 9), (1, 4, -9)])
    show("single cells", 5, [(0, 0, 1), (2, 2, 2), (4, 4, 3)])
    show("nested ranges", 7, [(0, 6, 1), (1, 5, 1), (2, 4, 1), (3, 3, 1)])
    show("large increments", 3, [(0, 2, 1000), (1, 1, -1000)])
    seed = 370
    checksum = 0
    cells = 0
    for _ in range(300):
        seed = (seed * 1103515245 + 12345) % 2147483648
        length = 1 + (seed // 65536) % 200
        seed = (seed * 1103515245 + 12345) % 2147483648
        count = (seed // 65536) % 301
        updates = []
        for _ in range(count):
            seed = (seed * 1103515245 + 12345) % 2147483648
            a = (seed // 65536) % length
            seed = (seed * 1103515245 + 12345) % 2147483648
            b = (seed // 65536) % length
            seed = (seed * 1103515245 + 12345) % 2147483648
            inc = (seed // 65536) % 2001 - 1000
            updates.append((min(a, b), max(a, b), inc))
        out = get_modified_array(length, updates)
        cells += len(out)
        for v in out:
            checksum = (checksum * 31 + v + 1000000) % 1000000007
    print(f"300 random arrays: {cells} cells, checksum {checksum}")


main()
