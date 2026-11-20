# LeetCode #2381: Shifting Letters II -- the bench, the ★ arm in Python: a
# difference array of the shifts, its running sum each letter's step.


def shifting_letters(s, shifts):
    n = len(s)
    diff = [0] * (n + 1)
    for start, end, direction in shifts:
        step = 1 if direction == 1 else -1
        diff[start] += step
        diff[end + 1] -= step
    out = []
    total = 0
    for i in range(n):
        total += diff[i]
        out.append(chr(97 + (ord(s[i]) - 97 + total) % 26))
    return "".join(out)


seed = 2381


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # a string of 5 * 10^4 letters and 10 lists of 5 * 10^4 shifts, list
    # l's shifts up to 10^l letters long, capped at the string; pass p
    # applies list p % 10
    n = 50000
    s = "".join(chr(97 + next_random() % 26) for _ in range(n))
    lists = []
    for l in range(10):
        reach = 1
        for _ in range(l):
            reach = min(reach * 10, n)
        shifts = []
        for _ in range(n):
            start = next_random() % n
            end = min(start + next_random() % reach, n - 1)
            shifts.append((start, end, next_random() % 2))
        lists.append(shifts)
    check = 0
    for p in range(200):
        t = shifting_letters(s, lists[p % 10])
        for c in t:
            check = (check * 31 + ord(c) - 97 + p) % 1000000007
    print(f"200 passes over 5 * 10^4 letters: checksum {check}")


main()
