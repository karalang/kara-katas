# Benchmark for #507 in Python: the ★ arm (divisors in pairs up to the
# square root); see ../check_perfect_number.kara.


def check_perfect_number(num):
    if num == 1:
        return False
    total = 1
    i = 2
    while i * i <= num:
        if num % i == 0:
            total += i
            if i * i != num:
                total += num // i
        i += 1
    return total == num


seed = 507


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 100,000 numbers from 1 to 10^8 (the problem's most), one in ten of
    # them one of the five perfect numbers in range, built once. Then
    # each is checked once.
    count = 100000
    known = [6, 28, 496, 8128, 33550336]
    nums = []
    for c in range(count):
        if c % 10 == 0:
            nums.append(known[next_random() % 5])
        else:
            hi = next_random()
            nums.append(1 + (hi * 32768 + next_random()) % 100000000)
    perfect = 0
    checksum = 0
    for num in nums:
        answer = check_perfect_number(num)
        if answer:
            perfect += 1
        checksum = (checksum * 31 + num % 1000 * 2 + int(answer)) % 1000000007
    print(f"{count} numbers: {perfect} perfect, checksum {checksum}")


main()
