# LeetCode #1518: Water Bottles -- the Python mirror of the ★ arm
# (bottles.kara): drink, trade the empties in whole lots, repeat.


def num_water_bottles(num_bottles, num_exchange):
    drunk = 0
    full = num_bottles
    empty = 0
    while full > 0:
        drunk += full
        empty += full
        full = empty // num_exchange
        empty %= num_exchange
    return drunk


seed = 1518


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    print(f"example 1, 9 bottles, 3 for 1 -> {num_water_bottles(9, 3)}")
    print(f"example 2, 15 bottles, 4 for 1 -> {num_water_bottles(15, 4)}")
    print(f"one bottle, 2 for 1 -> {num_water_bottles(1, 2)}")
    print(f"100 bottles, 2 for 1 -> {num_water_bottles(100, 2)}")
    check = 0
    for bottles in range(1, 101):
        for exchange in range(2, 101):
            check = mix(check, num_water_bottles(bottles, exchange))
    print(f"every pair, 1 to 100 bottles and 2 to 100 for 1: checksum {check}")
    big = 0
    for _ in range(1000):
        bottles = (next_random() * 32768 + next_random()) % 1000000 + 1
        exchange = next_random() % 20 + 2
        big = mix(big, num_water_bottles(bottles, exchange))
    print(f"1000 pairs up to 1000000 bottles and 2 to 21 for 1: checksum {big}")


main()
