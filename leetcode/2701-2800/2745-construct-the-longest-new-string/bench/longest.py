# LeetCode #2745: Construct the Longest New String -- the bench
# (longest.kara in Python): the table arm, bottom up over the pieces left
# and the last piece placed, flat in one list.


def longest_string(x, y, z):
    def at(a, b, c, last):
        return ((a * (y + 1) + b) * (z + 1) + c) * 4 + last

    more = [0] * ((x + 1) * (y + 1) * (z + 1) * 4)
    for a in range(x + 1):
        for b in range(y + 1):
            for c in range(z + 1):
                for last in range(4):
                    best = 0
                    if a > 0 and last != 0:
                        best = max(best, 2 + more[at(a - 1, b, c, 0)])
                    if b > 0 and (last == 0 or last == 3):
                        best = max(best, 2 + more[at(a, b - 1, c, 1)])
                    if c > 0 and last != 0:
                        best = max(best, 2 + more[at(a, b, c - 1, 2)])
                    more[at(a, b, c, last)] = best
    return more[at(x, y, z, 3)]


seed = 2745


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 1000, 3
    cases = []
    for _ in range(count):
        x = next_random() % 50 + 1
        y = next_random() % 50 + 1
        z = next_random() % 50 + 1
        cases.append((x, y, z))
    total = check = 0
    for r in range(rounds):
        for x, y, z in cases:
            length = longest_string(x, y, z)
            total += length
            check = (check * 31 + length + r) % 1000000007
    print(f"{count} counts, {rounds} rounds: lengths sum to {total}, checksum {check}")


main()
