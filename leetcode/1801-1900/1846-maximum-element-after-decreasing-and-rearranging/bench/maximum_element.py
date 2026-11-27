# LeetCode #1846: Maximum Element After Decreasing and Rearranging -- the
# bench in Python: the ★ arm over 200 calls on the first 50000 to 99999 of
# one list of 10^5 numbers from 1 to 60000, built once, each run's length
# drawn from the checksum so far. Each call is handed its own copy of its
# run, which the arm sorts.


def maximum_element_after_decrementing_and_rearranging(arr):
    arr.sort()
    top = 0
    for x in arr:
        top = min(top + 1, x)
    return top


def main():
    seed = 1846
    base = []
    for _ in range(100000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        hi = seed // 65536
        seed = (seed * 1103515245 + 12345) % 2147483648
        base.append(1 + (hi * 32768 + seed // 65536) % 60000)
    check = 0
    for call in range(200):
        n = 50000 + (check + call) % 50000
        check = (check * 31 + maximum_element_after_decrementing_and_rearranging(base[:n])) % 1000000007
    print(f"200 calls: checksum {check}")


main()
