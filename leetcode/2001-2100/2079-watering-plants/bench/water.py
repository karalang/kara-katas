# LeetCode #2079: Watering Plants -- Python mirror of the ★ arm's
# benchmark (water.kara): 2000 gardens of 1000 plants built first, then
# every garden answered for 500 cans, from 1000 up by 97 a can.


def watering_plants(plants, capacity):
    steps = 0
    can = capacity
    for i, need in enumerate(plants):
        if can < need:
            steps += 2 * i
            can = capacity
        steps += 1
        can -= need
    return steps


seed = 2079


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


gardens = [[next_random() % 1000 + 1 for _ in range(1000)] for _ in range(2000)]
total = 0
check = 0
for plants in gardens:
    for k in range(500):
        a = watering_plants(plants, 1000 + 97 * k)
        total += a
        check = (check * 31 + a) % 1000000007
print(f"1000000 answers: sum {total}, checksum {check}")
