# LeetCode #923: 3Sum With Multiplicity -- counting the values (Python mirror).

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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(arr, target):
    print(f"[{','.join(str(v) for v in arr)}], target {target}: {three_sum_multi(arr, target)}")


def main():
    global seed
    show([1, 1, 2, 2, 3, 3, 4, 4, 5, 5], 8)
    show([1, 1, 2, 2, 2, 2], 5)
    show([2, 1, 3], 6)
    show([1, 2, 3], 7)
    show([0, 0, 0, 0], 0)
    show([100, 100, 100, 100, 100], 300)
    show([0, 100, 50, 50, 25, 75], 150)
    show([3, 3, 3], 10)
    seed = 923
    total = 0
    check = 0
    for r in range(200):
        n = 3 + next_random() % 298
        top = 101 if r % 2 == 0 else 11
        arr = [next_random() % top for _ in range(n)]
        target = next_random() % (3 * (top - 1) + 1)
        a = three_sum_multi(arr, target)
        total += a
        check = (check * 1000003 + a) % 1000000007
    print(f"200 random arrays: answers summing to {total}, checksum {check}")
    ones, spread, few = [], [], []
    for i in range(3000):
        ones.append(1)
        spread.append(next_random() % 101)
        few.append(i % 3)
    print(f"3000 values: all 1 for 3 gives {three_sum_multi(ones, 3)}, random for 150 gives {three_sum_multi(spread, 150)}, 0, 1 and 2 for 3 gives {three_sum_multi(few, 3)}")


main()
