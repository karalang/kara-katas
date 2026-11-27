# LeetCode #1846: Maximum Element After Decreasing and Rearranging -- the ★
# arm in Python


def maximum_element_after_decrementing_and_rearranging(arr):
    arr = sorted(arr)
    top = 0
    for x in arr:
        top = min(top + 1, x)
    return top


seed = 1846


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    f = maximum_element_after_decrementing_and_rearranging
    print(f"{f([2, 2, 1, 2, 1])} {f([100, 1, 1000])} {f([1, 2, 3, 4, 5])}")
    print(f"{f([1])} {f([1000000000])} {f([5, 5, 5, 5, 5])} {f([5, 4, 3, 2, 1])} {f([1, 1, 9, 9, 9])} {f([1, 1, 1, 100])}")
    every = [1000000000] * 100000
    wide = []
    narrow = []
    for _ in range(100000):
        a = next_random()
        b = next_random()
        wide.append(1 + (a * 32768 + b) % 1000000000)
        c = next_random()
        d = next_random()
        narrow.append(1 + (c * 32768 + d) % 50000)
    print(f"the most: {f(every)} {f(wide)} {f(narrow)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 20
        arr = [1 + next_random() % 25 for _ in range(n)]
        check = (check * 31 + f(arr)) % 1000000007
    print(f"3000 random lists: checksum {check}")


main()
