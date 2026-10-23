# LeetCode #898 bench: the table arm (the ★ arm with a hash table of its
# own) on 12 arrays of 50,000 numbers, LeetCode's largest, each a random
# number below 2^30 AND-ed with a second, so that about a quarter of the
# bits are set. The ORs ending at each place are kept in a short list,
# and every one is gathered into an open-addressing hash table written
# here, with no library set, map or sort. The same algorithm as
# subarray_bitwise_ors.kara.


class Table:
    def __init__(self):
        self.slots = [-1] * 64
        self.count = 0


def insert(t, v):
    mask = len(t.slots) - 1
    i = ((v * 2654435761) % 4294967296) & mask
    while t.slots[i] != -1:
        if t.slots[i] == v:
            return
        i = (i + 1) & mask
    t.slots[i] = v
    t.count += 1
    if t.count * 2 > len(t.slots):
        old = t.slots
        t.slots = [-1] * (len(old) * 2)
        t.count = 0
        for w in old:
            if w != -1:
                insert(t, w)


def subarray_bitwise_ors(arr):
    table = Table()
    ending = []
    for x in arr:
        nxt = [x]
        for y in ending:
            v = y | x
            if v != nxt[-1]:
                nxt.append(v)
        for v in nxt:
            insert(table, v)
        ending = nxt
    return table.count


seed = 898


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    total = 0
    check = 0
    for _ in range(12):
        arr = []
        for _ in range(50000):
            a = next_random() * 32768
            a += next_random()
            b = next_random() * 32768
            b += next_random()
            arr.append(a & b)
        got = subarray_bitwise_ors(arr)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"12 arrays of 50000 numbers: {total} ORs in all, checksum {check}")


main()
