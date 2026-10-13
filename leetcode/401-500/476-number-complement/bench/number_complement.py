# Benchmark for #476: Python mirror of the ★ arm (a mask of the number's
# own width); see number_complement.kara.


def find_complement(num):
    mask = 1
    while mask < num:
        mask = (mask << 1) | 1
    return num ^ mask


seed = 476


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 30000000
    total = 0
    checksum = 0
    for _ in range(count):
        bits = 1 + next_random() % 31
        high = 1 << (bits - 1)
        num = high | ((next_random() * 32768 + next_random()) % high)
        got = find_complement(num)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} numbers: complements add up to {total}, checksum {checksum}")


main()
