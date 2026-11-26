# LeetCode #1403 bench, Python: the same sort and greedy take, workload
# and checksum as min_subsequence.kara.


def min_subsequence(nums):
    order = sorted(nums, reverse=True)
    rest = sum(order)
    taken = 0
    picked = []
    for x in order:
        picked.append(x)
        taken += x
        rest -= x
        if taken > rest:
            break
    return picked


def main():
    seed = 1403
    pool = []
    for _ in range(100000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        pool.append(seed // 65536 % 100 + 1)
    check = 0
    for r in range(20000):
        at = (check + r * 7919) % 99501
        window = pool[at:at + 500]
        picked = min_subsequence(window)
        check = (check * 131 + len(picked) * 101 + picked[-1]) % 1000000007
    print(f"20000 windows of 500 numbers: checksum {check}")


main()
