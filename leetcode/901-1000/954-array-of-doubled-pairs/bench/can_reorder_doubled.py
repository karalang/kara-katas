# LeetCode #954: Array of Doubled Pairs -- Python mirror of the Kara
# bench program (counts, smallest first).


def can_reorder_doubled(arr):
    count = {}
    for x in arr:
        count[x] = count.get(x, 0) + 1
    values = sorted(count, key=abs)
    for x in values:
        c = count.get(x, 0)
        if c == 0:
            continue
        if x == 0:
            if c % 2 != 0:
                return False
            continue
        d = count.get(2 * x, 0)
        if d < c:
            return False
        count[2 * x] = d - c
    return True


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    rounds, count, n = 10, 20, 30000
    seed = [954]
    sets = []
    for s in range(count):
        arr = []
        for _ in range(n // 2):
            a = next_random(seed)
            x = (a * 32768 + next_random(seed)) % 100001 - 50000
            arr.append(x)
            arr.append(2 * x)
        for i in range(n):
            a = next_random(seed)
            j = i + (a * 32768 + next_random(seed)) % (n - i)
            arr[i], arr[j] = arr[j], arr[i]
        if s % 4 == 3:
            v = arr[s * 1000]
            arr[s * 1000] = 2 * int(v / 2) + 1
        sets.append(arr)
    yes = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            k = (r + i) % count
            ok = can_reorder_doubled(sets[k])
            if ok:
                yes += 1
            check = (check * 31 + (1 if ok else 2)) % 1000000007
    print(f"{rounds} rounds over {count} sets of {n} values: {yes} can be paired, checksum {check}")


main()
