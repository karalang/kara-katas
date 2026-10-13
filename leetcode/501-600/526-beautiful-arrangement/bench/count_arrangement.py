# Benchmark for #526: Python mirror of the ★ arm (place positions from
# the front); see count_arrangement.kara.


def place(n, pos, used):
    if pos > n:
        return 1
    count = 0
    for x in range(1, n + 1):
        if not used[x] and (x % pos == 0 or pos % x == 0):
            used[x] = True
            count += place(n, pos + 1, used)
            used[x] = False
    return count


def count_arrangement(n):
    return place(n, 1, [False] * (n + 1))


def main():
    total = 0
    checksum = 0
    for round_ in range(20):
        for n in range(1, 16):
            count = count_arrangement(n)
            total += count
            checksum = (checksum * 31 + count + round_) % 1000000007
    print(f"n from 1 to 15, 20 rounds: total {total}, checksum {checksum}")


main()
