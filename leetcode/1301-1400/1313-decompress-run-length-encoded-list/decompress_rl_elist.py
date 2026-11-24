# LeetCode #1313: Decompress Run-Length Encoded List -- Python mirror of the
# ★ arm: the list read two numbers at a time, each pair's value pushed as
# many times as its count.


def decompress_rl_elist(nums):
    out = []
    for i in range(0, len(nums), 2):
        for _ in range(nums[i]):
            out.append(nums[i + 1])
    return out


seed = 1313


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return ",".join(str(x) for x in v)


def main():
    e1 = decompress_rl_elist([1, 2, 3, 4])
    e2 = decompress_rl_elist([1, 1, 2, 3])
    one = decompress_rl_elist([3, 7])
    again = decompress_rl_elist([2, 5, 1, 5, 1, 6])
    big = decompress_rl_elist([100, 100])
    print(f"{show(e1)} {show(e2)} {show(one)} {show(again)} {len(big)}:{sum(big)}")
    total = 0
    check = 0
    for t in range(1000):
        pairs = 1 + next_random() % 50
        most = 1 if t % 3 == 0 else 5 if t % 3 == 1 else 100
        nums = []
        for _ in range(pairs):
            nums.append(1 + next_random() % most)
            nums.append(1 + next_random() % 100)
        got = decompress_rl_elist(nums)
        total += len(got)
        for x in got:
            check = (check * 31 + x) % 1000000007
    print(f"1000 random lists: {total} numbers, checksum {check}")


main()
