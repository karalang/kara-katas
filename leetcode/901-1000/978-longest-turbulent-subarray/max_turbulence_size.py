# LeetCode #978: Longest Turbulent Subarray -- mirror of the ★ arm
# (max_turbulence_size.kara), two running lengths.


def max_turbulence_size(arr):
    best = up = down = 1
    for i in range(1, len(arr)):
        if arr[i - 1] < arr[i]:
            up = down + 1
            down = 1
        elif arr[i - 1] > arr[i]:
            down = up + 1
            up = 1
        else:
            up = down = 1
        best = max(best, up, down)
    return best


seed = 978


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_values(n, top):
    arr = []
    for _ in range(n):
        hi = next_random()
        arr.append((hi * 32768 + next_random()) % top)
    return arr


def main():
    cases = [
        [9, 4, 2, 10, 7, 8, 8, 1, 9],
        [4, 8, 12, 16],
        [100],
        [7, 7, 7],
        [1, 2],
        [2, 1, 2, 1, 2, 1],
        [0, 1000000000, 0, 1000000000],
        [1, 2, 1, 1, 2, 1, 2],
        [3, 3, 1, 2],
        [5, 4, 3, 4, 3, 4, 4, 5, 4],
    ]
    for arr in cases:
        print(f"{arr}: {max_turbulence_size(arr)}")
    for count, most, top in [(300, 12, 3), (3000, 60, 10), (4, 40000, 1000000001)]:
        total = check = 0
        for _ in range(count):
            n = most if most == 40000 else 1 + next_random() % most
            k = max_turbulence_size(random_values(n, top))
            total += k
            check = (check * 31 + k) % 1000000007
        print(f"{count} random arrays of up to {most} values: lengths total {total}, checksum {check}")


main()
