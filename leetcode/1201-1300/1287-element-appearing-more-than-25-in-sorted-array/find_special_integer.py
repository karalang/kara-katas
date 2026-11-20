# LeetCode #1287: Element Appearing More Than 25% In Sorted Array -- Python
# mirror of the ★ arm: the first i where arr[i] == arr[i + n // 4].


def find_special_integer(arr):
    quarter = len(arr) // 4
    for i in range(len(arr) - quarter):
        if arr[i] == arr[i + quarter]:
            return arr[i]
    return -1


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def problem(n):
    planted = next_random() % 100001
    times = n if n < 4 else n // 4 + 1 + next_random() % (n - n // 4)
    arr = [planted] * times
    drawn = {planted: times}
    while len(arr) < n:
        if next_random() % 2 == 0:
            x = planted + next_random() % 5 - 2
        else:
            x = next_random() % 100001
        c = drawn.get(x, 0)
        if x >= 0 and x != planted and (c + 1) * 4 <= n:
            drawn[x] = c + 1
            arr.append(x)
    arr.sort()
    return arr


def main():
    global seed
    print(f"{find_special_integer([1, 2, 2, 6, 6, 6, 6, 7, 10])} {find_special_integer([1, 1])} {find_special_integer([5])} {find_special_integer([1, 2, 3, 3])} {find_special_integer([1, 2, 3, 4, 4, 4])}")
    seed = 1287
    total = check = 0
    for case in range(1020):
        n = next_random() % 400 + 1 if case < 1000 else 10000
        x = find_special_integer(problem(n))
        total += x
        check = (check * 131 + x) % 1000000007
    print(f"1020 random problems: total {total}, checksum {check}")


if __name__ == "__main__":
    main()
