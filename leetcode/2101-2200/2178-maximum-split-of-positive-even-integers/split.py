# LeetCode #2178: Maximum Split of Positive Even Integers -- the Python
# mirror of split.kara: 2, 4, 6, ... while what is left reaches the next,
# and the rest added to the last.


def maximum_even_split(final_sum):
    parts = []
    if final_sum % 2 != 0:
        return parts
    left = final_sum
    nxt = 2
    while left >= nxt:
        parts.append(nxt)
        left -= nxt
        nxt += 2
    parts[-1] += left
    return parts


# ---- test harness ---------------------------------------------------------

seed = 2178


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(final_sum):
    print(f"{final_sum} -> [{', '.join(map(str, maximum_even_split(final_sum)))}]")


def fold(check, parts):
    check = (check * 31 + len(parts)) % 1000000007
    for p in parts:
        check = (check * 31 + p % 1000000007) % 1000000007
    return check


def main():
    for s in [12, 7, 28, 2, 4, 1, 38]:
        show(s)
    parts_in_all = 0
    check = 0
    for rnd in range(2000):
        top = [100, 10000, 1000000][rnd % 3]
        a = next_random()
        b = next_random()
        final_sum = (a * 32768 + b) % top + 1
        parts = maximum_even_split(final_sum)
        parts_in_all += len(parts)
        check = fold(check, parts)
    print(f"2000 sums: {parts_in_all} parts in all, checksum {check}")
    for final_sum in [10000000000, 9999999998]:
        parts = maximum_even_split(final_sum)
        print(f"{final_sum}: {len(parts)} parts, the last {parts[-1]}, checksum {fold(0, parts)}")


main()
