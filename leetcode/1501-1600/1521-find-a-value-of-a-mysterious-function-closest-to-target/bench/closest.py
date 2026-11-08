# LeetCode #1521: Find a Value of a Mysterious Function Closest to Target
# -- bench: the ★ arm over 2000 random arrays of 1 to 4000 numbers, built
# once and answered 3 times.


def closest_to_target(arr, target):
    best = abs(arr[0] - target)
    ends = []
    for x in arr:
        nxt = [x]
        for v in ends:
            w = v & x
            if w != nxt[-1]:
                nxt.append(w)
        for v in nxt:
            best = min(best, abs(v - target))
        ends = nxt
    return best


seed = 1521


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    count = 2000
    arrays = []
    targets = []
    for _ in range(count):
        n = next_random() % 4000 + 1
        base = next_random() % 1000000 + 1
        arr = []
        for _ in range(n):
            if next_random() % 2 == 0:
                x = base & (next_random() * 32768 + next_random())
            else:
                x = next_random() * 32 % 1000000
            arr.append(max(x, 1))
        targets.append((next_random() * 32768 + next_random()) % 1000001)
        arrays.append(arr)
    check = 0
    total = 0
    for _ in range(3):
        for i in range(count):
            answer = closest_to_target(arrays[i], targets[i])
            total += answer
            check = mix(check, answer)
    print(f"3 passes over 2000 arrays of up to 4000 numbers: distances sum to {total}, checksum {check}")


main()
