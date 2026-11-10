# LeetCode #2094: Finding 3-Digit Even Numbers -- Python mirror of the ★
# arm's benchmark (even.kara): the same 100000 lists, each answered by the
# same counts and walk over the even numbers from 100 to 998.

seed = 2094


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def find_even_numbers(digits):
    have = [0] * 10
    for d in digits:
        have[d] += 1
    found = []
    for x in range(100, 1000, 2):
        need = [0] * 10
        need[x // 100] += 1
        need[x // 10 % 10] += 1
        need[x % 10] += 1
        if all(need[d] <= have[d] for d in range(10)):
            found.append(x)
    return found


def main():
    count = 0
    check = 0
    for _ in range(100000):
        n = next_random() % 98 + 3
        top = [10, 6, 4][next_random() % 3]
        digits = [next_random() % top for _ in range(n)]
        got = find_even_numbers(digits)
        count += len(got)
        for x in got:
            check = (check * 31 + x) % 1000000007
    print(f"100000 answers: {count} numbers, checksum {check}")


main()
