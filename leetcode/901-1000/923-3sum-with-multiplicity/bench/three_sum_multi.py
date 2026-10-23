# LeetCode #923: 3Sum With Multiplicity -- bench: counting the values.
# Mirrors three_sum_multi.kara.


def three_sum_multi(arr, target):
    modulus = 1000000007
    count = [0] * 101
    for v in arr:
        count[v] += 1
    total = 0
    for x in range(101):
        if 3 * x > target:
            break
        for y in range(x, 101):
            z = target - x - y
            if z < y:
                break
            if z > 100:
                continue
            if x == y and y == z:
                ways = count[x] * (count[x] - 1) * (count[x] - 2) // 6
            elif x == y:
                ways = count[x] * (count[x] - 1) // 2 * count[z]
            elif y == z:
                ways = count[x] * count[y] * (count[y] - 1) // 2
            else:
                ways = count[x] * count[y] * count[z]
            total = (total + ways) % modulus
    return total


seed = 923


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count, n = 500, 100, 3000
    # count arrays of n values from 0 to 100, built once
    arrays = [[next_random() % 101 for _ in range(n)] for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        # each round asks every array for a different target up to 300
        for i in range(count):
            a = three_sum_multi(arrays[i], (r * 7 + i) % 301)
            total += a
            check = (check * 1000003 + a) % 1000000007
    print(f"{rounds} rounds over {count} arrays of {n}: answers summing to {total}, checksum {check}")


main()
