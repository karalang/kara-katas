# Benchmark for #845: Longest Mountain in Array -- Python twin of the Kāra ★
# arm (one pass with two counters).


def longest_mountain(arr):
    best = 0
    up = 0
    down = 0
    for i in range(1, len(arr)):
        if (down > 0 and arr[i - 1] < arr[i]) or arr[i - 1] == arr[i]:
            up = 0
            down = 0
        if arr[i - 1] < arr[i]:
            up += 1
        elif arr[i - 1] > arr[i]:
            down += 1
        if up > 0 and down > 0:
            best = max(best, up + down + 1)
    return best


def main():
    count, rounds, n = 64, 20000, 10000
    seed = 845

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    arrays = []
    for g in range(count):
        arr = []
        if g % 3 == 0:
            for _ in range(n):
                arr.append(next_random() % 10001)
        elif g % 3 == 1:
            v = 5000
            for _ in range(n):
                arr.append(v)
                v += next_random() % 3 - 1
        else:
            while len(arr) < n:
                up = next_random() % 40
                down = next_random() % 40
                base = next_random() % 100
                for k in range(up + 1):
                    if len(arr) < n:
                        arr.append(base + k)
                for k in range(down):
                    if len(arr) < n:
                        arr.append(base + up - k - 1)
        arrays.append(arr)
    total = 0
    checksum = 0
    for rnd in range(rounds):
        m = longest_mountain(arrays[rnd % count])
        total += m
        checksum = (checksum * 31 + m) % 1000000007
    print(f"{rounds} rounds of {count} arrays: lengths sum to {total}, checksum {checksum}")


main()
