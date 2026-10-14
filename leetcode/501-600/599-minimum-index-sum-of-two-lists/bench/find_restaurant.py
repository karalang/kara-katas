# Benchmark for #599: Python mirror of the ★ arm (index the first list in
# a dict, then walk the second); see find_restaurant.kara.


def find_restaurant(list1, list2):
    index = {}
    for i, s in enumerate(list1):
        index[s] = i
    best = len(list1) + len(list2)
    answer = []
    for j, s in enumerate(list2):
        i = index.get(s)
        if i is not None:
            total = i + j
            if total < best:
                best = total
                answer.clear()
            if total == best:
                answer.append(s)
    return answer


# ---- benchmark ----------------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def spell(k):
    letters = []
    while True:
        letters.append(chr(97 + k % 26))
        k //= 26
        if k == 0:
            break
    return "".join(reversed(letters))


def main():
    count = 100
    rounds = 100
    seed = [599]
    pool = []
    for k in range(3000):
        number = step(seed) * 32768
        number += step(seed)
        pool.append(f"restaurant {spell(k)} at {spell(number)}")
    order = list(range(len(pool)))
    pairs = []
    for _ in range(count):
        lists = []
        for _ in range(2):
            lst = []
            for k in range(1000):
                j = k + step(seed) % (len(pool) - k)
                order[k], order[j] = order[j], order[k]
                lst.append(pool[order[k]])
            lists.append(lst)
        pairs.append((lists[0], lists[1]))
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            pair = pairs[(rnd * 7 + g) % count]
            got = find_restaurant(pair[0], pair[1])
            total += len(got)
            for s in got:
                checksum = (checksum * 31 + len(s)) % 1000000007
                checksum = (checksum * 31 + ord(s[-1])) % 1000000007
    print(f"{count} pairs, {rounds} rounds: total {total}, checksum {checksum}")


main()
