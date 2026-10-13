# LeetCode #476: Number Complement -- Python mirror of the ★ arm
# (number_complement.kara): a mask of the number's own width.


def find_complement(num):
    mask = 1
    while mask < num:
        mask = (mask << 1) | 1
    return num ^ mask


# ---- test harness ---------------------------------------------------------

def show(num):
    print(f"{num} ({num:b}) -> {find_complement(num)}")


seed = 476


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for num in [5, 1, 2, 7, 8, 10, 1023, 1024, 2147483647, 1073741824, 1431655765]:
        show(num)
    count = 1000
    checksum = 0
    zeros = 0
    for _ in range(count):
        bits = 1 + next_random() % 31
        num = (1 << (bits - 1)) | ((next_random() * 32768 + next_random()) % (1 << (bits - 1)))
        got = find_complement(num)
        if got == 0:
            zeros += 1
        checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} random numbers: {zeros} complements are 0, checksum {checksum}")


main()
