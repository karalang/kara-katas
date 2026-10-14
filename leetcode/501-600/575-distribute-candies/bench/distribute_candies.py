# Benchmark for #575: Python mirror of the ★ arm (a set of the types);
# see distribute_candies.kara.


def distribute_candies(candy_type):
    kinds = set()
    for c in candy_type:
        kinds.add(c)
    return min(len(kinds), len(candy_type) // 2)


# ---- benchmark ----------------------------------------------------------------

seed = 575


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 100
    rounds = 200
    cases = []
    for _ in range(count):
        types = 1 + next_random() % 10000
        pool = []
        for _ in range(types):
            high = next_random() * 32768
            pool.append((high + next_random()) % 200001 - 100000)
        candies = [pool[next_random() % types] for _ in range(10000)]
        cases.append(candies)
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            p = (rnd * 7 + g) % count
            got = distribute_candies(cases[p])
            total += got
            checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} cases of 10000 candies, {rounds} rounds: {total} types eaten, checksum {checksum}")


main()
