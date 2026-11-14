# LeetCode #1566: Detect Pattern of Length M Repeated K or More Times --
# bench: the ★ arm (a run of agreements m apart) over 20 arrays of 100000
# values of 1 to 100, built once, half with a pattern planted near the
# end, each asked for m from 1 to 50 with k of 3.
# Python mirror of pattern.kara.


def contains_pattern(arr, m, k):
    run = 0
    for i in range(len(arr) - m):
        if arr[i] == arr[i + m]:
            run += 1
            if run == m * (k - 1):
                return True
        else:
            run = 0
    return False


seed = 1566


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    n = 100000
    arrays = []
    for a in range(20):
        arr = [next_random() % 100 + 1 for _ in range(n)]
        if a % 2 == 1:
            m = 1 + a % 50
            start = n - 3 * m - next_random() % 100
            for i in range(m, 3 * m):
                arr[start + i] = arr[start + i % m]
        arrays.append(arr)
    check = 0
    found = 0
    for m in range(1, 51):
        for a, arr in enumerate(arrays):
            yes = contains_pattern(arr, m, 3)
            if yes:
                found += 1
            check = mix(check, m * 100 + a if yes else 0)
    print(f"m from 1 to 50 over 20 arrays of 100000 values: {found} with a pattern, checksum {check}")


main()
