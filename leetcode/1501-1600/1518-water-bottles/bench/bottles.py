# LeetCode #1518 bench: the ★ arm (whole lots a round), as bottles.kara.


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


check = 0
for i in range(20000000):
    bottles = i * 7919 % 1000000000 + 1
    exchange = i % 99 + 2
    check = (check * 31 + num_water_bottles(bottles, exchange) + 1) % 1000000007
print(f"20000000 questions up to 10^9 bottles and 2 to 100 for 1: checksum {check}")
