# LeetCode #2164: Sort Even and Odd Indices Independently -- the
# benchmark's Python mirror of parity.kara.


def sort_even_odd(nums):
    even = sorted(nums[0::2])
    odd = sorted(nums[1::2], reverse=True)
    out = []
    for i in range(len(nums)):
        out.append(even[i // 2] if i % 2 == 0 else odd[i // 2])
    return out


seed = 2164


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = [[next_random() % 100 + 1 for _ in range(100)] for _ in range(1000)]
    check = 0
    for rnd in range(200):
        for k in range(1000):
            at = next_random() % 100
            lists[k][at] = next_random() % 100 + 1
            out = sort_even_odd(list(lists[k]))
            check = (check * 31 + out[rnd % 100] + out[(k * 7) % 100]) % 1000000007
    print(f"200000 solves: checksum {check}")


main()
