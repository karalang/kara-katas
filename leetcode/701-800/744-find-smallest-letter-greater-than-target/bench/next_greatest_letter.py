# LeetCode 744 — Find Smallest Letter Greater Than Target, bench: the ★
# arm (binary search) on lists of 10000 sorted letters, many random
# targets each. Mirrors next_greatest_letter.kara.


def next_greatest_letter(letters, target):
    lo = 0
    hi = len(letters)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if letters[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return letters[0] if lo == len(letters) else letters[lo]


seed = 744


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 60
    n = 10000
    queries = 100000
    a = ord('a')
    z = ord('z')
    total = 0
    for _ in range(rounds):
        letters = []
        c = a + next_random() % 6
        for _ in range(n):
            if next_random() % 500 == 0 and c < z:
                c += 1
            letters.append(chr(c))
        if letters[0] == letters[n - 1]:
            letters[n - 1] = chr(ord(letters[0]) + 1)
        for _ in range(queries):
            target = chr(a + next_random() % 26)
            total += ord(next_greatest_letter(letters, target))
    print(f"{rounds} rounds of 100000 queries on 10000 letters: answers sum to {total}")


main()
