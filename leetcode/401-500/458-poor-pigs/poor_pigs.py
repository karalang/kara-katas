# LeetCode #458: Poor Pigs -- Python mirror of poor_pigs.kara (the star arm).
#
# With T = minutes_to_test // minutes_to_die rounds, one pig ends in one
# of T + 1 states, so p pigs tell apart (T + 1)^p buckets; grow the
# number of outcomes until it covers the buckets.


def poor_pigs(buckets, minutes_to_die, minutes_to_test):
    states = minutes_to_test // minutes_to_die + 1
    pigs = 0
    covered = 1
    while covered < buckets:
        covered *= states
        pigs += 1
    return pigs


def show(buckets, minutes_to_die, minutes_to_test):
    pigs = poor_pigs(buckets, minutes_to_die, minutes_to_test)
    print(f"buckets {buckets}, minutes_to_die {minutes_to_die}, minutes_to_test {minutes_to_test} -> {pigs}")


seed = 458


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show(4, 15, 15)
    show(4, 15, 30)
    show(1000, 15, 60)
    show(1, 1, 1)
    show(2, 1, 1)
    show(1000, 1, 1)
    show(1000, 1, 9)
    show(1001, 1, 9)
    show(1000, 100, 100)
    show(1000, 1, 100)
    show(1000000000000, 7, 20)
    count = 300
    total = 0
    checksum = 0
    for _ in range(count):
        digits = next_random() % 13
        top = 10 ** digits
        a = next_random()
        b = next_random()
        c = next_random()
        r = (a * 65536 + b) * 65536 + c
        buckets = 1 + r % top
        die = 1 + next_random() % 100
        test = die + next_random() % (101 - die)
        pigs = poor_pigs(buckets, die, test)
        total += pigs
        checksum = (checksum * 31 + pigs * 1000003 + buckets % 1000) % 1000000007
    print(f"{count} random cases: {total} pigs, checksum {checksum}")


main()
