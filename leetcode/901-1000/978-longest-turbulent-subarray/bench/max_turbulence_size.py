# Benchmark: LeetCode #978 Longest Turbulent Subarray -- the ★ arm, two
# running lengths, on 20 arrays of 40000 values. Mirrors
# max_turbulence_size.kara, .rs, .c and go-seq/.


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


def main():
    rounds, count = 150, 20
    arrays = [[next_random() % 100 for _ in range(40000)] for _ in range(count)]
    total = check = 0
    for r in range(rounds):
        for i in range(count):
            k = max_turbulence_size(arrays[(r + i) % count])
            total += k
            check = (check * 31 + k) % 1000000007
    print(f"{rounds} rounds over {count} arrays of 40000 values: "
          f"lengths total {total}, checksum {check}")


main()
