# Benchmark for #605: Python mirror of the ★ arm (plant greedily); see
# can_place_flowers.kara.


def can_place_flowers(flowerbed, n):
    bed = list(flowerbed)
    planted = 0
    for i in range(len(bed)):
        if bed[i] == 0 and (i == 0 or bed[i - 1] == 0) and (i == len(bed) - 1 or bed[i + 1] == 0):
            bed[i] = 1
            planted += 1
    return planted >= n


def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    count = 100
    rounds = 50
    size = 20000
    seed = [605]
    beds = []
    for _ in range(count):
        spread = 2 + step(seed) % 5
        bed = []
        for i in range(size):
            if step(seed) % spread == 0 and (i == 0 or bed[i - 1] == 0):
                bed.append(1)
            else:
                bed.append(0)
        beds.append(bed)
    yes = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            n = (rnd * 397 + g * 113) % 8000
            fits = can_place_flowers(beds[(rnd * 7 + g) % count], n)
            if fits:
                yes += 1
            checksum = (checksum * 31 + n * 2 + (1 if fits else 0)) % 1000000007
    print(f"{count} beds, {rounds} rounds: {yes} fit, checksum {checksum}")


main()
