# Benchmark for #781: Rabbits in Forest -- mirror of the ★ arm (groups
# counted by answer), with the same workload as the Kāra program.


def num_rabbits(answers):
    count = {}
    for a in answers:
        count[a] = count.get(a, 0) + 1
    total = 0
    for v, c in count.items():
        size = v + 1
        total += (c + size - 1) // size * size
    return total


seed = 781


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 64
    forests = []
    for g in range(count):
        top = 10 if g % 3 == 0 else 100 if g % 3 == 1 else 1000
        forests.append([next_random() % top for _ in range(1000)])
    total = 0
    checksum = 0
    for rnd in range(50000):
        g = (rnd * 7) % count
        rabbits = num_rabbits(forests[g])
        total += rabbits
        checksum = (checksum * 31 + rabbits + g) % 1000000007
    print(f"50000 rounds of 1000 answers: {total} rabbits, checksum {checksum}")


main()
