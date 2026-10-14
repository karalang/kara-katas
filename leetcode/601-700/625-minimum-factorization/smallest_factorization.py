# LeetCode #625: Minimum Factorization -- Python mirror of
# smallest_factorization.kara.
#
# The same greedy from the largest digit and the same harness, printing
# the same lines.


def smallest_factorization(num):
    if num < 10:
        return num
    rest = num
    answer = 0
    place = 1
    d = 9
    while d >= 2:
        while rest % d == 0:
            rest //= d
            answer += d * place
            place *= 10
            if answer > 2147483647:
                return 0
        d -= 1
    return answer if rest == 1 else 0


seed = 625


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(num):
    print(f"{num} -> {smallest_factorization(num)}")


def main():
    for num in [48, 15, 1, 7, 10, 11, 12, 36, 54, 1440, 1959552, 387420489, 774840978, 1073741824, 2147483647]:
        show(num)
    total = 0
    checksum = 0
    found = 0
    for i in range(600):
        num = 1
        if i < 300:
            for _ in range(1 + next_random() % 12):
                d = 1 + next_random() % 9
                if num * d <= 2147483647:
                    num *= d
        else:
            hi = next_random()
            lo = next_random()
            num = 1 + (hi * 65536 + lo) % 2147483647
        answer = smallest_factorization(num)
        if answer > 0:
            found += 1
        total += answer
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"600 random numbers: {found} with an answer, total {total}, checksum {checksum}")
    total = 0
    checksum = 0
    found = 0
    for num in range(1, 20001):
        answer = smallest_factorization(num)
        if answer > 0:
            found += 1
        total += answer
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"1 to 20000: {found} with an answer, total {total}, checksum {checksum}")


main()
